# =============================================================================
# Archivo: catalog/migrations/0005_fix_imagen_urls_confiables.py
# Carpeta: backend/catalog/migrations/
# Propósito:
#   Corrige `imagen_url` de todos los productos.
#
# Contexto (por qué “no cargaban” las fotos):
#   En `0004_expand_catalogo_premium` se usaron muchas URLs de Wikimedia Commons
#   construidas con `Special:FilePath/...` y nombres de archivo “probables”.
#   Varios nombres NO existen en Commons (HTTP 404) o devuelven HTML en lugar de
#   imagen, y el navegador muestra el ícono de imagen rota.
#
# Solución aplicada aquí:
#   Reasignar imágenes a URLs públicas **verificadas** (Unsplash) con parámetros
#   de optimización (`auto=format`, `w`, `q`). Son fotos reales de tecnología;
#   no coinciden 1:1 con cada SKU, pero el catálogo vuelve a verse correctamente.
#
# Si más adelante hospedas tus propias fotos:
#   Sube archivos a `MEDIA`/`STATIC` y guarda esas URLs en `imagen_url`.
# =============================================================================
from __future__ import annotations

from django.db import migrations


def _urls_confiables() -> list[str]:
    """Lista de URLs que devuelven 200 (verificadas en el entorno de desarrollo)."""
    base = "https://images.unsplash.com/photo-{id}?auto=format&fit=crop&w=1200&q=80"
    ids = [
        "1511707171634-5f897ff02aa9",
        "1601784551446-20c9e07cdbdb",
        "1544244015-0df4b3ffc6b0",
        "1585790050230-5dd28404ccb9",
        "1523275335684-37898b6baf30",
        "1434493789847-2f02dc6ca35d",
        "1496181133206-80ce9b88a853",
        "1525547719571-a2d4ac8945e2",
        "1556656793-08538906a9f8",
        "1574944985070-8f3ebc6b79d2",
        "1572635196237-14b3f281503f",
        "1585060544812-6b45742d762f",
        "1512941937669-90a1b58e7e9c",
    ]
    return [base.format(id=photo_id) for photo_id in ids]


def _forwards(apps, schema_editor) -> None:
    Producto = apps.get_model("catalog", "Producto")
    urls = _urls_confiables()
    productos = list(Producto.objects.all().order_by("id"))
    for idx, producto in enumerate(productos):
        producto.imagen_url = urls[idx % len(urls)]
        producto.save(update_fields=["imagen_url"])


def _backwards(apps, schema_editor) -> None:
    """No revertimos (no hay forma segura de reconstruir las URLs previas)."""
    return


class Migration(migrations.Migration):
    """Corrige URLs de imágenes rotas del catálogo."""

    dependencies = [
        ("catalog", "0004_expand_catalogo_premium"),
    ]

    operations = [
        migrations.RunPython(_forwards, _backwards),
    ]
