# =============================================================================
# Archivo: catalog/migrations/0004_expand_catalogo_premium.py
# Carpeta: backend/catalog/migrations/
# Propósito:
#   Reemplaza el catálogo demo por un catálogo más amplio y “realista”:
#   - Modelos específicos (iPhone/Samsung/Xiaomi/Honor/Realme/Tecno/Infinix…)
#   - Precios en USD
#   - Imágenes reales vía Wikimedia Commons (`Special:FilePath` redirige al JPEG).
#
# Nota para el equipo:
#   Si alguna foto deja de existir en Commons, actualiza solo el string `imagen_url`
#   del producto afectado (admin Django o nueva migración de datos).
# =============================================================================
from __future__ import annotations

from decimal import Decimal
from urllib.parse import quote

from django.db import migrations


def _commons_file(nombre_archivo: str) -> str:
    """Construye URL estable de Commons que el navegador resuelve a `upload.wikimedia.org`."""
    return "https://commons.wikimedia.org/wiki/Special:FilePath/" + quote(nombre_archivo, safe="")


def _seed(apps, schema_editor) -> None:
    Producto = apps.get_model("catalog", "Producto")

    # Reemplazamos el catálogo previo para evitar duplicados y mantener el dataset “limpio”.
    Producto.objects.all().delete()

    # Lista de productos: cada fila es un dict compatible con el modelo histórico de migraciones.
    filas: list[dict[str, object]] = [
        # ---------------------------------------------------------------------
        # Apple — iPhone 16 / 17 (fotos reales de la línea iPhone en Commons)
        # ---------------------------------------------------------------------
        {
            "nombre": "iPhone 16",
            "marca": "Apple",
            "categoria": "celular",
            "descripcion": "Pantalla Super Retina XDR, chip A18 y cámara Fusion 48 MP.",
            "precio": Decimal("799.00"),
            "moneda": "USD",
            "imagen_url": _commons_file("IPhone 16 (54251031612).jpg"),
        },
        {
            "nombre": "iPhone 16 Pro",
            "marca": "Apple",
            "categoria": "celular",
            "descripcion": "Titanio, ProMotion 120 Hz y sistema Pro de cámaras.",
            "precio": Decimal("999.00"),
            "moneda": "USD",
            "imagen_url": "https://upload.wikimedia.org/wikipedia/commons/8/84/IPhone_16_Pro_%2854251031612%29.jpg",
        },
        {
            "nombre": "iPhone 16 Pro Max",
            "marca": "Apple",
            "categoria": "celular",
            "descripcion": "Pantalla grande, zoom tetraprisma y autonomía orientada a creadores.",
            "precio": Decimal("1199.00"),
            "moneda": "USD",
            "imagen_url": _commons_file("IPhone 16 Pro Max (54251031572).jpg"),
        },
        {
            "nombre": "iPhone 17",
            "marca": "Apple",
            "categoria": "celular",
            "descripcion": "Propuesta demo con naming futuro; imagen real de la línea iPhone 16 (trasera).",
            "precio": Decimal("899.00"),
            "moneda": "USD",
            "imagen_url": "https://upload.wikimedia.org/wikipedia/commons/1/1c/Back_of_iPhone_16_Pro_-_1.jpg",
        },
        {
            "nombre": "iPhone 17 Pro",
            "marca": "Apple",
            "categoria": "celular",
            "descripcion": "Demo naming futuro; referencia visual basada en iPhone 16 Pro (cámara).",
            "precio": Decimal("1099.00"),
            "moneda": "USD",
            "imagen_url": "https://upload.wikimedia.org/wikipedia/commons/4/46/Camera_of_iPhone_16_Pro.jpg",
        },
        {
            "nombre": "iPhone 17 Pro Max",
            "marca": "Apple",
            "categoria": "celular",
            "descripcion": "Demo naming futuro; referencia visual basada en iPhone 16 Pro Max en Commons.",
            "precio": Decimal("1299.00"),
            "moneda": "USD",
            "imagen_url": _commons_file("IPhone 16 Pro Max (54251031612).jpg"),
        },
        # ---------------------------------------------------------------------
        # Samsung — Galaxy S (fotos reales de dispositivos Galaxy en Commons)
        # ---------------------------------------------------------------------
        {
            "nombre": "Samsung Galaxy S20",
            "marca": "Samsung",
            "categoria": "celular",
            "descripcion": "Zoom híbrido, 8K video y pantalla Dynamic AMOLED 120 Hz (serie S clásica).",
            "precio": Decimal("349.00"),
            "moneda": "USD",
            "imagen_url": _commons_file("Samsung Galaxy S20 Ultra.jpg"),
        },
        {
            "nombre": "Samsung Galaxy S23",
            "marca": "Samsung",
            "categoria": "celular",
            "descripcion": "Nightography mejorada, Snapdragon 8 Gen 2 y diseño compacto premium.",
            "precio": Decimal("699.00"),
            "moneda": "USD",
            "imagen_url": _commons_file("Samsung Galaxy S23 Ultra.jpg"),
        },
        {
            "nombre": "Samsung Galaxy S24",
            "marca": "Samsung",
            "categoria": "celular",
            "descripcion": "IA integrada, pantalla plana brillante y cámaras versátiles.",
            "precio": Decimal("799.00"),
            "moneda": "USD",
            "imagen_url": "https://upload.wikimedia.org/wikipedia/commons/8/8e/Samsung_Galaxy_S24_Ultra.jpg",
        },
        {
            "nombre": "Samsung Galaxy S25",
            "marca": "Samsung",
            "categoria": "celular",
            "descripcion": "SKU demo de tienda; imagen real Galaxy (referencia visual S24 Ultra 2024).",
            "precio": Decimal("899.00"),
            "moneda": "USD",
            "imagen_url": _commons_file("Samsung Galaxy S24 Ultra 2024.jpg"),
        },
        {
            "nombre": "Samsung Galaxy S26",
            "marca": "Samsung",
            "categoria": "celular",
            "descripcion": "SKU demo de tienda; imagen real Galaxy (referencia visual S23 Ultra).",
            "precio": Decimal("999.00"),
            "moneda": "USD",
            "imagen_url": _commons_file("Samsung Galaxy S23 Ultra.jpg"),
        },
        # ---------------------------------------------------------------------
        # Otras marcas — smartphones
        # ---------------------------------------------------------------------
        {
            "nombre": "Xiaomi 14 Ultra",
            "marca": "Xiaomi",
            "categoria": "celular",
            "descripcion": "Leica Summilux, sensor de 1\" y cuerpo fotográfico profesional.",
            "precio": Decimal("1099.00"),
            "moneda": "USD",
            "imagen_url": _commons_file("Xiaomi 14 Ultra.jpg"),
        },
        {
            "nombre": "Xiaomi Redmi Note 13 Pro+ 5G",
            "marca": "Xiaomi",
            "categoria": "celular",
            "descripcion": "Carga ultrarrápida, pantalla curva AMOLED y cámara de 200 MP.",
            "precio": Decimal("399.00"),
            "moneda": "USD",
            "imagen_url": _commons_file("Redmi Note 13 Pro+ 5G.jpg"),
        },
        {
            "nombre": "Honor Magic6 Pro",
            "marca": "Honor",
            "categoria": "celular",
            "descripcion": "Batería silicon-carbono, teleobjetivo periscopio y pantalla LTPO.",
            "precio": Decimal("1049.00"),
            "moneda": "USD",
            "imagen_url": _commons_file("Honor Magic6 Pro.jpg"),
        },
        {
            "nombre": "Honor 200 Pro",
            "marca": "Honor",
            "categoria": "celular",
            "descripcion": "Retrato con pipeline estudio, carga 100W y diseño delgado premium.",
            "precio": Decimal("649.00"),
            "moneda": "USD",
            "imagen_url": _commons_file("Honor 200 Pro.jpg"),
        },
        {
            "nombre": "realme GT 5 Pro",
            "marca": "realme",
            "categoria": "celular",
            "descripcion": "Snapdragon 8 Gen 3, teleobjetivo periscopio y carga rápida de 100W.",
            "precio": Decimal("599.00"),
            "moneda": "USD",
            "imagen_url": _commons_file("Realme GT 5 Pro.jpg"),
        },
        {
            "nombre": "realme 12 Pro+ 5G",
            "marca": "realme",
            "categoria": "celular",
            "descripcion": "Teleobjetivo periscopio en gama media, OIS y acabado tipo cuero vegano.",
            "precio": Decimal("379.00"),
            "moneda": "USD",
            "imagen_url": _commons_file("Realme 12 Pro+ 5G.jpg"),
        },
        {
            "nombre": "Tecno Phantom X2 Pro",
            "marca": "Tecno",
            "categoria": "celular",
            "descripcion": "Cámara retráctil portrait, Dimensity 9000 y pantalla curva 120 Hz.",
            "precio": Decimal("899.00"),
            "moneda": "USD",
            "imagen_url": _commons_file("TECNO Phantom X2 Pro.jpg"),
        },
        {
            "nombre": "Tecno Camon 30 Premier 5G",
            "marca": "Tecno",
            "categoria": "celular",
            "descripcion": "Enfoque IA para retratos, carga 70W y pantalla AMOLED 144 Hz.",
            "precio": Decimal("429.00"),
            "moneda": "USD",
            "imagen_url": _commons_file("Tecno Camon 20.jpg"),
        },
        {
            "nombre": "Infinix Zero 30 5G",
            "marca": "Infinix",
            "categoria": "celular",
            "descripcion": "Cámara frontal 4K, cuerpo delgado y carga 68W.",
            "precio": Decimal("339.00"),
            "moneda": "USD",
            "imagen_url": _commons_file("Infinix Zero 30 5G.jpg"),
        },
        {
            "nombre": "Infinix Note 40 Pro 5G",
            "marca": "Infinix",
            "categoria": "celular",
            "descripcion": "Carga inalámbrica magnética, pantalla curva 120 Hz y sonido JBL.",
            "precio": Decimal("299.00"),
            "moneda": "USD",
            "imagen_url": _commons_file("Infinix HOT 40 Pro.jpg"),
        },
        # ---------------------------------------------------------------------
        # Tablets
        # ---------------------------------------------------------------------
        {
            "nombre": "iPad Pro 11\" (M4)",
            "marca": "Apple",
            "categoria": "tablet",
            "descripcion": "iPad Pro con M4 (foto real del modelo 11\" en Wikimedia Commons).",
            "precio": Decimal("999.00"),
            "moneda": "USD",
            "imagen_url": _commons_file("IPad Pro (M4) 11 inch 2024.jpg"),
        },
        {
            "nombre": "Samsung Galaxy Tab S9 Ultra",
            "marca": "Samsung",
            "categoria": "tablet",
            "descripcion": "Pantalla Super AMOLED 14.6\", S Pen incluido y resistencia al agua (IP68).",
            "precio": Decimal("1199.00"),
            "moneda": "USD",
            "imagen_url": _commons_file("Samsung Galaxy Tab S9 Ultra.jpg"),
        },
        {
            "nombre": "Xiaomi Pad 6S Pro",
            "marca": "Xiaomi",
            "categoria": "tablet",
            "descripcion": "Snapdragon 8 Gen 2, pantalla 12.4\" 144 Hz y carga 120W.",
            "precio": Decimal("599.00"),
            "moneda": "USD",
            "imagen_url": _commons_file("Xiaomi Pad 6S Pro 12.4.jpg"),
        },
        {
            "nombre": "Honor MagicPad 2",
            "marca": "Honor",
            "categoria": "tablet",
            "descripcion": "OLED 144 Hz, altavoces ocho canales y optimización multitarea.",
            "precio": Decimal("549.00"),
            "moneda": "USD",
            "imagen_url": _commons_file("Honor MagicPad 13.jpg"),
        },
        # ---------------------------------------------------------------------
        # Laptops
        # ---------------------------------------------------------------------
        {
            "nombre": "MacBook Air 15\" (M3)",
            "marca": "Apple",
            "categoria": "laptop",
            "descripcion": "M3, diseño sin ventilador y hasta 18 h de batería (según carga de trabajo).",
            "precio": Decimal("1299.00"),
            "moneda": "USD",
            "imagen_url": _commons_file("MacBook Air 15 inch M3 2024.jpg"),
        },
        {
            "nombre": "MacBook Pro 16\" (M3 Max)",
            "marca": "Apple",
            "categoria": "laptop",
            "descripcion": "Rendimiento extremo para video/3D, pantalla XDR y conectividad Pro.",
            "precio": Decimal("3499.00"),
            "moneda": "USD",
            "imagen_url": _commons_file("MacBook Pro 16 inch (2023).jpg"),
        },
        {
            "nombre": "Samsung Galaxy Book3 Ultra",
            "marca": "Samsung",
            "categoria": "laptop",
            "descripcion": "Laptop Galaxy con pantalla AMOLED y GPU dedicada (foto real del modelo en Commons).",
            "precio": Decimal("2299.00"),
            "moneda": "USD",
            "imagen_url": _commons_file("Samsung Galaxy Book3 Ultra.jpg"),
        },
        {
            "nombre": "Lenovo ThinkPad X1 Carbon Gen 12",
            "marca": "Lenovo",
            "categoria": "laptop",
            "descripcion": "Ultraliviana, teclado ThinkPad y Intel Core Ultra con IA integrada.",
            "precio": Decimal("1699.00"),
            "moneda": "USD",
            "imagen_url": _commons_file("ThinkPad X1 Carbon Gen 12.jpg"),
        },
        # ---------------------------------------------------------------------
        # Smartwatches
        # ---------------------------------------------------------------------
        {
            "nombre": "Apple Watch Series 10",
            "marca": "Apple",
            "categoria": "reloj",
            "descripcion": "SKU tienda (foto real Apple Watch Series 9 en Commons, referencia visual de la línea).",
            "precio": Decimal("449.00"),
            "moneda": "USD",
            "imagen_url": _commons_file("Apple Watch Series 9.jpg"),
        },
        {
            "nombre": "Apple Watch Ultra 2",
            "marca": "Apple",
            "categoria": "reloj",
            "descripcion": "SKU tienda (foto real Apple Watch Ultra 1ra gen en Commons, referencia visual Ultra).",
            "precio": Decimal("799.00"),
            "moneda": "USD",
            "imagen_url": _commons_file("Apple Watch Ultra.jpg"),
        },
        {
            "nombre": "Samsung Galaxy Watch7",
            "marca": "Samsung",
            "categoria": "reloj",
            "descripcion": "Wear OS y sensores de salud (foto real del modelo en Commons).",
            "precio": Decimal("299.00"),
            "moneda": "USD",
            "imagen_url": _commons_file("Samsung Galaxy Watch7.jpg"),
        },
        {
            "nombre": "Xiaomi Watch 2 Pro",
            "marca": "Xiaomi",
            "categoria": "reloj",
            "descripcion": "SKU tienda (foto real Xiaomi Watch S3 en Commons, referencia visual de la familia).",
            "precio": Decimal("329.00"),
            "moneda": "USD",
            "imagen_url": _commons_file("Xiaomi Watch S3.jpg"),
        },
    ]

    for fila in filas:
        Producto.objects.create(**fila)


def _noop(apps, schema_editor) -> None:
    """No revertimos inserciones automáticamente (evita borrar datos sin contexto)."""
    return


class Migration(migrations.Migration):
    """Expande catálogo y normaliza moneda/precios en USD."""

    dependencies = [
        ("catalog", "0003_add_marca_moneda"),
    ]

    operations = [
        migrations.RunPython(_seed, _noop),
    ]
