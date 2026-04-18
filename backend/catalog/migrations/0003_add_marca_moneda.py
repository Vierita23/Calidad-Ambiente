# =============================================================================
# Archivo: catalog/migrations/0003_add_marca_moneda.py
# Carpeta: backend/catalog/migrations/
# Propósito: Añade `marca` y `moneda` al modelo `Producto` sin perder datos previos.
# =============================================================================
from django.db import migrations, models


class Migration(migrations.Migration):
    """Agrega columnas nuevas con valores por defecto seguros."""

    dependencies = [
        ("catalog", "0002_seed_demo_productos"),
    ]

    operations = [
        migrations.AddField(
            model_name="producto",
            name="marca",
            field=models.CharField(
                blank=True,
                default="",
                help_text="Marca comercial (Apple, Samsung, Xiaomi, etc.).",
                max_length=80,
            ),
        ),
        migrations.AddField(
            model_name="producto",
            name="moneda",
            field=models.CharField(
                default="USD",
                help_text="Código ISO de moneda para mostrar precios (ej. USD).",
                max_length=8,
            ),
        ),
    ]
