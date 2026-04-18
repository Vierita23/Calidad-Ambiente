# =============================================================================
# Archivo: catalog/migrations/0002_seed_demo_productos.py
# Carpeta: backend/catalog/migrations/
# Propósito: Inserta productos de demostración si la tabla está vacía.
# Importante: Es idempotente (no duplica datos si ya existen filas).
# =============================================================================
from __future__ import annotations

from decimal import Decimal

from django.db import migrations


def seed_forward(apps, schema_editor) -> None:
    """Crea filas demo usando el historial de modelos (buena práctica en migraciones)."""
    Producto = apps.get_model("catalog", "Producto")
    if Producto.objects.exists():
        return

    # URLs de imágenes públicas (Unsplash). Sirven para un catálogo visual sin subir archivos.
    filas: list[dict[str, object]] = [
        {
            "nombre": "Smartphone Pro X",
            "categoria": "celular",
            "descripcion": "Pantalla AMOLED, cámara triple y carga rápida.",
            "precio": Decimal("12999.00"),
            "imagen_url": "https://images.unsplash.com/photo-1511707171634-5f897ff02aa9?auto=format&fit=crop&w=900&q=80",
        },
        {
            "nombre": "Smartphone Lite 5G",
            "categoria": "celular",
            "descripcion": "Equilibrio perfecto entre rendimiento y autonomía.",
            "precio": Decimal("7999.00"),
            "imagen_url": "https://images.unsplash.com/photo-1601784551446-20c9e07cdbdb?auto=format&fit=crop&w=900&q=80",
        },
        {
            "nombre": "Tablet Air 11",
            "categoria": "tablet",
            "descripcion": "Ideal para estudio, diseño y entretenimiento.",
            "precio": Decimal("9999.00"),
            "imagen_url": "https://images.unsplash.com/photo-1544244015-0df4b3ffc6b0?auto=format&fit=crop&w=900&q=80",
        },
        {
            "nombre": "Tablet Kids 10",
            "categoria": "tablet",
            "descripcion": "Resistente, ligera y con controles parentales.",
            "precio": Decimal("5499.00"),
            "imagen_url": "https://images.unsplash.com/photo-1585790050230-5dd28404ccb9?auto=format&fit=crop&w=900&q=80",
        },
        {
            "nombre": "Smartwatch Pulse",
            "categoria": "reloj",
            "descripcion": "Monitoreo de salud, GPS y resistencia al agua.",
            "precio": Decimal("3499.00"),
            "imagen_url": "https://images.unsplash.com/photo-1523275335684-37898b6baf30?auto=format&fit=crop&w=900&q=80",
        },
        {
            "nombre": "Smartwatch Sport",
            "categoria": "reloj",
            "descripcion": "Modo deportivo avanzado y batería de larga duración.",
            "precio": Decimal("2999.00"),
            "imagen_url": "https://images.unsplash.com/photo-1434493789847-2f02dc6ca35d?auto=format&fit=crop&w=900&q=80",
        },
        {
            "nombre": "Laptop Ultrabook 14",
            "categoria": "laptop",
            "descripcion": "Ultradelgada, SSD NVMe y teclado retroiluminado.",
            "precio": Decimal("18999.00"),
            "imagen_url": "https://images.unsplash.com/photo-1496181133206-80ce9b88a853?auto=format&fit=crop&w=900&q=80",
        },
        {
            "nombre": "Laptop Creator 16",
            "categoria": "laptop",
            "descripcion": "Pantalla alta resolución para edición y render.",
            "precio": Decimal("24999.00"),
            "imagen_url": "https://images.unsplash.com/photo-1525547719571-a2d4ac8945e2?auto=format&fit=crop&w=900&q=80",
        },
    ]

    for fila in filas:
        Producto.objects.create(**fila)


def seed_backward(apps, schema_editor) -> None:
    """No borramos datos automáticamente (evita pérdidas accidentales)."""
    return


class Migration(migrations.Migration):
    """Encadena el seed después de crear el modelo."""

    dependencies = [
        ("catalog", "0001_initial"),
    ]

    operations = [
        migrations.RunPython(seed_forward, seed_backward),
    ]
