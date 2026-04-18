# =============================================================================
# Script auxiliar (NO se ejecuta en producción automáticamente):
# Consulta Wikimedia Commons y genera un diccionario nombre -> URL directa.
#
# Uso (desde la carpeta backend/):
#   python scripts/build_wikimedia_urls.py
# =============================================================================
from __future__ import annotations

import json
import re
import sys
import time
import urllib.parse
import urllib.request

USER_AGENT = "CalidadAmbienteSchool/1.0 (Django demo; educational use)"

# Cada entrada: nombre en BD, búsqueda Commons, subcadenas que deben aparecer
# todas en el título del archivo (minúsculas) para evitar resultados irrelevantes.
# Si no hay foto del modelo exacto en Commons, la query apunta al modelo real
# más cercano (p. ej. iPhone 17 → línea 16) y el título debe reflejar esa línea.
ENTRADAS: list[dict[str, object]] = [
    {
        "nombre": "iPhone 16",
        "query": "IPhone 16 rear filetype:bitmap",
        "require": ("iphone", "16"),
    },
    {
        "nombre": "iPhone 16 Pro",
        "query": "IPhone 16 Pro back filetype:bitmap",
        "require": ("iphone", "16", "pro"),
    },
    {
        "nombre": "iPhone 16 Pro Max",
        "query": "IPhone 16 Pro Max rear filetype:bitmap",
        "require": ("iphone", "16", "pro", "max"),
        "forbid": ("screen",),
    },
    {
        "nombre": "iPhone 17",
        "query": "IPhone 16 back ultramarine filetype:bitmap",
        "require": ("iphone", "16"),
    },
    {
        "nombre": "iPhone 17 Pro",
        "query": "IPhone 16 Pro back filetype:bitmap",
        "require": ("iphone", "16", "pro"),
    },
    {
        "nombre": "iPhone 17 Pro Max",
        "query": "IPhone 16 Pro Max rear filetype:bitmap",
        "require": ("iphone", "16", "pro", "max"),
        "forbid": ("screen",),
    },
    {
        "nombre": "Samsung Galaxy S20",
        "query": "Samsung Galaxy S20 filetype:bitmap",
        "require": ("galaxy", "s20"),
        "forbid": ("fe", "plus", "ultra"),  # catálogo = S20 base
    },
    {
        "nombre": "Samsung Galaxy S23",
        "query": "Samsung Galaxy S23 back filetype:bitmap",
        "require": ("galaxy", "s23"),
    },
    {
        "nombre": "Samsung Galaxy S24",
        "query": "Samsung Galaxy S24 back filetype:bitmap",
        "require": ("galaxy", "s24"),
        "forbid": ("ultra",),  # SKU catálogo = S24 (no Ultra)
    },
    {
        "nombre": "Samsung Galaxy S25",
        "query": "Samsung Galaxy S24 Ultra filetype:bitmap",
        "require": ("galaxy", "s24"),
    },
    {
        "nombre": "Samsung Galaxy S26",
        "query": "Samsung Galaxy S23 Ultra lavender filetype:bitmap",
        "require": ("galaxy", "s23"),
    },
    {
        "nombre": "Xiaomi 14 Ultra",
        "query": "Xiaomi 14 Ultra smartphone filetype:bitmap",
        "require": ("xiaomi", "14"),
    },
    {
        "nombre": "Xiaomi Redmi Note 13 Pro+ 5G",
        "query": "Redmi Note 13 Pro 5G filetype:bitmap",
        "require": ("redmi", "13"),
        "forbid": ("note 14", "note14", "redmi 14"),
    },
    {
        "nombre": "Honor Magic6 Pro",
        "query": "Honor Magic6 Pro back filetype:bitmap",
        "require": ("honor", "magic"),
        "forbid": ("magic3", "magic4", "magic5"),
    },
    {
        "nombre": "Honor 200 Pro",
        "query": "Honor 200 Pro back filetype:bitmap",
        "require": ("honor", "200"),
    },
    {
        "nombre": "realme GT 5 Pro",
        "query": "Realme GT5 Pro filetype:bitmap",
        "require": ("realme",),
        "forbid": ("c35", "c55", "narzo"),
    },
    {
        "nombre": "realme 12 Pro+ 5G",
        "query": "Realme 12 Pro plus filetype:bitmap",
        "require": ("realme", "12"),
        "forbid": ("c35", "c53", "narzo"),
    },
    {
        "nombre": "Tecno Phantom X2 Pro",
        "query": "Tecno Phantom X2 Pro filetype:bitmap",
        "require": ("tecno", "phantom"),
    },
    {
        "nombre": "Tecno Camon 30 Premier 5G",
        "query": "Tecno Camon 30 Premier filetype:bitmap",
        "require": ("tecno", "30"),
    },
    {
        "nombre": "Infinix Zero 30 5G",
        "query": "Infinix Zero 30 5G filetype:bitmap",
        "require": ("infinix", "30"),
    },
    {
        "nombre": "Infinix Note 40 Pro 5G",
        "query": "Infinix Note 40 Pro filetype:bitmap",
        "require": ("infinix", "40"),
    },
    {
        "nombre": 'iPad Pro 11" (M4)',
        "query": "iPad Pro 11 M4 filetype:bitmap",
        "require": ("ipad", "m4"),
    },
    {
        "nombre": "Samsung Galaxy Tab S9 Ultra",
        "query": "Samsung Galaxy Tab S9 filetype:bitmap",
        "require": ("tab", "s9"),
        "forbid": ("fold", "flip", "watch", "z fold"),
    },
    {
        "nombre": "Xiaomi Pad 6S Pro",
        "query": "Xiaomi Pad 6S Pro tablet filetype:bitmap",
        "require": ("xiaomi", "pad"),
    },
    {
        "nombre": "Honor MagicPad 2",
        "query": "Honor MagicPad 2 tablet filetype:bitmap",
        "require": ("honor", "magicpad"),
    },
    {
        "nombre": 'MacBook Air 15" (M3)',
        "query": "Macbook Air 15 inch filetype:bitmap",
        "require": ("macbook", "air", "15"),
        "forbid": ("blurred",),
    },
    {
        "nombre": 'MacBook Pro 16" (M3 Max)',
        "query": "MacBook Pro 16 inch M3 filetype:bitmap",
        "require": ("macbook", "16", "m3"),
    },
    {
        "nombre": "Samsung Galaxy Book3 Ultra",
        "query": "Galaxy Book3 Ultra filetype:bitmap",
        "require": ("galaxy", "book3"),
    },
    {
        "nombre": "Lenovo ThinkPad X1 Carbon Gen 12",
        "query": "ThinkPad X1 Carbon 2024 filetype:bitmap",
        "require": ("thinkpad", "x1", "carbon"),
    },
    {
        "nombre": "Apple Watch Series 10",
        "query": "Apple Watch Series 10 filetype:bitmap",
        "require": ("watch", "series"),
    },
    {
        "nombre": "Apple Watch Ultra 2",
        "query": "Apple Watch Ultra 2 filetype:bitmap",
        "require": ("watch", "ultra"),
    },
    {
        "nombre": "Samsung Galaxy Watch7",
        "query": "Galaxy Watch 7 filetype:bitmap",
        "require": ("galaxy", "watch"),
    },
    {
        "nombre": "Xiaomi Watch 2 Pro",
        "query": "Xiaomi Watch 2 Pro filetype:bitmap",
        "require": ("xiaomi", "watch"),
        "forbid": ("band", "strap"),
    },
]


def _http_json(url: str) -> dict:
    req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    with urllib.request.urlopen(req, timeout=45) as resp:
        return json.load(resp)


def _search_titles(query: str, limit: int = 20) -> list[str]:
    qs = urllib.parse.urlencode(
        {
            "action": "query",
            "list": "search",
            "srsearch": query,
            "srnamespace": 6,
            "srlimit": str(limit),
            "format": "json",
        }
    )
    data = _http_json("https://commons.wikimedia.org/w/api.php?" + qs)
    return [hit["title"] for hit in data.get("query", {}).get("search", [])]


def _image_url(title: str) -> tuple[str | None, str | None]:
    qs = urllib.parse.urlencode(
        {
            "action": "query",
            "titles": title,
            "prop": "imageinfo",
            "iiprop": "url|mime",
            "format": "json",
        }
    )
    data = _http_json("https://commons.wikimedia.org/w/api.php?" + qs)
    for page in data.get("query", {}).get("pages", {}).values():
        if page.get("missing") or int(page.get("pageid", -1)) < 0:
            continue
        ii = page.get("imageinfo", [{}])[0]
        mime = str(ii.get("mime", ""))
        if mime.startswith("image"):
            return ii.get("url"), mime
    return None, None


def _norm_title(title: str) -> str:
    t = title.lower().replace("_", " ")
    t = re.sub(r"^file:\s*", "", t)
    return t


def _score_candidate(title: str, require: tuple[str, ...], forbid: tuple[str, ...]) -> int:
    nt = _norm_title(title)
    for f in forbid:
        if f in nt:
            return -1
    for r in require:
        if r not in nt:
            return 0
    score = 100
    low = nt
    if "diagram" in low or "vector" in low or "logo" in low:
        return 0
    if low.endswith(".svg") or "svg" in low.split()[-1:]:
        return 0
    if "jpeg" in low or ".jpg" in low:
        score += 15
    if any(x in low for x in ("back", "rear", "front", "side")):
        score += 8
    if "compare" in low:
        score -= 5
    if "blurred" in low:
        score -= 40
    return score


def _pick_best_url(
    query: str, require: tuple[str, ...], forbid: tuple[str, ...] = ()
) -> tuple[str | None, str | None, str | None]:
    """Devuelve (url, mime, title_elegido)."""
    best: tuple[int, str, str, str] | None = None
    for title in _search_titles(query):
        sc = _score_candidate(title, require, forbid)
        if sc <= 0:
            continue
        url, mime = _image_url(title)
        if not url or not mime:
            continue
        if mime not in {"image/jpeg", "image/jpg", "image/png", "image/webp"}:
            continue
        if best is None or sc > best[0]:
            best = (sc, title, url, mime)
    if not best:
        return None, None, None
    _, title, url, mime = best
    return url, mime, title


def main() -> None:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    if hasattr(sys.stderr, "reconfigure"):
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")

    resultados: dict[str, dict[str, str]] = {}
    for entry in ENTRADAS:
        nombre = str(entry["nombre"])
        query = str(entry["query"])
        require = tuple(str(x).lower() for x in entry["require"])  # type: ignore[arg-type]
        forbid = tuple(str(x).lower() for x in entry.get("forbid", ()))  # type: ignore[arg-type]
        url, mime, title = _pick_best_url(query, require, forbid)
        resultados[nombre] = {"url": url or "", "mime": mime or "", "title": title or ""}
        print(f"# {nombre}\n# query={query}\n# title={title}\n# mime={mime}\n# url={url}\n")
        time.sleep(0.35)

    print("PYTHON_DICT = {")
    for nombre, meta in resultados.items():
        print(f"    {json.dumps(nombre, ensure_ascii=False)}: {json.dumps(meta['url'], ensure_ascii=False)},")
    print("}")


if __name__ == "__main__":
    main()
