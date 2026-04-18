# =============================================================================
# Archivo: catalog/migrations/0006_catalogo_imagenes_por_modelo_commons.py
# Carpeta: backend/catalog/migrations/
# Propósito:
#   Sustituye `imagen_url` por enlaces directos a `upload.wikimedia.org`
#   obtenidos vía API de Commons (no nombres de archivo inventados).
#
# Notas (honestidad del catálogo):
#   - SKUs “demo” (p. ej. iPhone 17, Galaxy S25/S26) usan la línea real más
#     cercana disponible en Commons, alineado con las descripciones en 0004.
#   - Algunos modelos no tienen foto clara en Commons: se usa la referencia más
#     cercana de la misma familia (p. ej. Redmi Note 12 trasera para Note 13+).
# =============================================================================
from __future__ import annotations

from django.db import migrations


# URLs resueltas desde `action=query&prop=imageinfo` en commons.wikimedia.org.
IMAGEN_POR_NOMBRE: dict[str, str] = {
    "iPhone 16": "https://upload.wikimedia.org/wikipedia/commons/a/a0/IPhone_16_Ultramarine_Rear.png",
    "iPhone 16 Pro": "https://upload.wikimedia.org/wikipedia/commons/7/7f/Back_view_of_iPhone_16_Pro_White_Titanium.jpg",
    "iPhone 16 Pro Max": "https://upload.wikimedia.org/wikipedia/commons/e/e2/IPhone_16_Pro_Max_Desert_Titanium_Rear.png",
    "iPhone 17": "https://upload.wikimedia.org/wikipedia/commons/b/bf/Back_view_of_iPhone_16_Ultramarine.jpg",
    "iPhone 17 Pro": "https://upload.wikimedia.org/wikipedia/commons/7/7f/Back_view_of_iPhone_16_Pro_White_Titanium.jpg",
    "iPhone 17 Pro Max": "https://upload.wikimedia.org/wikipedia/commons/e/e2/IPhone_16_Pro_Max_Desert_Titanium_Rear.png",
    "Samsung Galaxy S20": "https://upload.wikimedia.org/wikipedia/commons/3/39/Samsung_Galaxy_S20.jpg",
    "Samsung Galaxy S23": "https://upload.wikimedia.org/wikipedia/commons/a/a8/Back_of_the_Samsung_Galaxy_S23.jpg",
    "Samsung Galaxy S24": "https://upload.wikimedia.org/wikipedia/commons/f/fe/Samsung_Galaxy_s24_series.jpg",
    "Samsung Galaxy S25": "https://upload.wikimedia.org/wikipedia/commons/b/b7/Samsung_Galaxy_S24_Ultra_Backside.jpg",
    "Samsung Galaxy S26": "https://upload.wikimedia.org/wikipedia/commons/b/b3/Samsung_Galaxy_S23_Ultra%2C_512_GB%2C_Lavender_20230416_HOF00318_RAW-Export_cens.png",
    "Xiaomi 14 Ultra": "https://upload.wikimedia.org/wikipedia/commons/e/e8/HK_%E4%B8%AD%E7%92%B0_Central_%E7%9A%87%E5%90%8E%E5%A4%A7%E9%81%93%E4%B8%AD_33_Queen%27s_Road_Central_shop_%E8%B1%90%E6%BE%A4%E9%9B%BB%E5%99%A8_Fortress_Store_%E6%89%8B%E6%A9%9F_smartphone_XiaoMi_14_Ultra_watch_May_2024_R12S_01.jpg",
    # Commons no devuelve un archivo estable “Note 13 Pro+”: misma línea Redmi Note (12).
    "Xiaomi Redmi Note 13 Pro+ 5G": "https://upload.wikimedia.org/wikipedia/commons/f/f4/Redmi_Note_12_back.jpg",
    "Honor Magic6 Pro": "https://upload.wikimedia.org/wikipedia/commons/c/c1/Honor_Magic_6_Pro_white_Back.jpg",
    "Honor 200 Pro": "https://upload.wikimedia.org/wikipedia/commons/7/79/Back_view_of_Honor_200_Pro_Black.jpg",
    # Sin “GT 5 Pro” claro en Commons: misma marca, línea GT (Neo3).
    "realme GT 5 Pro": "https://upload.wikimedia.org/wikipedia/commons/0/0f/Realme_GT_Neo3_back.jpg",
    "realme 12 Pro+ 5G": "https://upload.wikimedia.org/wikipedia/commons/7/71/Realme_12_back.jpg",
    "Tecno Phantom X2 Pro": "https://upload.wikimedia.org/wikipedia/commons/7/77/Back_of_Tecno_Phantom_X2_Pro.png",
    # Alineado con 0004 (ya citaba Camon 20); Premier de la serie Camon.
    "Tecno Camon 30 Premier 5G": "https://upload.wikimedia.org/wikipedia/commons/d/d2/Camon_20_Premier_5G.png",
    # Sin “Zero 30” en Commons: familia Zero con foto verificada.
    "Infinix Zero 30 5G": "https://upload.wikimedia.org/wikipedia/commons/3/32/Infinix_Zero_X_pro.jpg",
    # Sin “Note 40” estable: serie Note reciente con foto de producto.
    "Infinix Note 40 Pro 5G": "https://upload.wikimedia.org/wikipedia/commons/8/81/Infinix_Note_50_Pro_4G.jpg",
    'iPad Pro 11" (M4)': "https://upload.wikimedia.org/wikipedia/commons/8/87/About_iPad_Pro_11-inch_%28M4%29.jpg",
    # Tab S9 real; “Ultra” suele aparecer en collages — se evita composición multi-dispositivo.
    "Samsung Galaxy Tab S9 Ultra": "https://upload.wikimedia.org/wikipedia/commons/5/59/20230729_%EC%82%BC%EC%84%B1_%EA%B0%A4%EB%9F%AD%EC%8B%9C_%ED%83%AD_S9.jpg",
    "Xiaomi Pad 6S Pro": "https://upload.wikimedia.org/wikipedia/commons/1/1e/Xiaomi_Pad_6S_Pro.jpg",
    "Honor MagicPad 2": "https://upload.wikimedia.org/wikipedia/commons/5/5f/Wikipedia_on_HONOR_pad.jpg",
    'MacBook Air 15" (M3)': "https://upload.wikimedia.org/wikipedia/commons/d/db/Macbook_Air_15_inch_-_2.jpg",
    # Chasis 16" Pro reciente; Commons tiene M2 Max como foto de producto estable.
    'MacBook Pro 16" (M3 Max)': "https://upload.wikimedia.org/wikipedia/commons/2/21/Apple_MacBook_Pro_16%22_M2_Max.jpg",
    "Samsung Galaxy Book3 Ultra": "https://upload.wikimedia.org/wikipedia/commons/5/5b/20230729_%EC%82%BC%EC%84%B1_%EA%B0%A4%EB%9F%AD%EC%8B%9C_%EB%B6%81_%ED%94%84%EB%A1%9C_360.jpg",
    # Gen 12: foto clásica X1 Carbon (Commons no indexa bien “Gen 12”).
    "Lenovo ThinkPad X1 Carbon Gen 12": "https://upload.wikimedia.org/wikipedia/commons/4/48/Lenovo_ThinkPad_X1_Carbon_Ultrabook.jpg",
    "Apple Watch Series 10": "https://upload.wikimedia.org/wikipedia/commons/5/55/Apple_Watch_Series_10.JPG",
    "Apple Watch Ultra 2": "https://upload.wikimedia.org/wikipedia/commons/3/33/Apple_Watch_Ultra_2.jpg",
    "Samsung Galaxy Watch7": "https://upload.wikimedia.org/wikipedia/commons/8/8b/SAMSUNG_Galaxy_Watch_%287%29.jpg",
    "Xiaomi Watch 2 Pro": "https://upload.wikimedia.org/wikipedia/commons/9/9e/Xiaomi_Watch_Pro_2.jpg",
}


def _forwards(apps, schema_editor) -> None:
    Producto = apps.get_model("catalog", "Producto")
    for nombre, url in IMAGEN_POR_NOMBRE.items():
        Producto.objects.filter(nombre=nombre).update(imagen_url=url)


def _backwards(apps, schema_editor) -> None:
    """No revertimos (no reconstruimos el reparto Unsplash de 0005)."""
    return


class Migration(migrations.Migration):
    """Imágenes del catálogo enlazadas a archivos reales en Wikimedia Commons."""

    dependencies = [
        ("catalog", "0005_fix_imagen_urls_confiables"),
    ]

    operations = [
        migrations.RunPython(_forwards, _backwards),
    ]
