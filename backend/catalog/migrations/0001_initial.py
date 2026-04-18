# =============================================================================
# Archivo: catalog/migrations/0001_initial.py
# Carpeta: backend/catalog/migrations/
# Propósito: Crea la tabla del modelo `Producto` en PostgreSQL.
# =============================================================================
import django.core.validators
from decimal import Decimal

from django.db import migrations, models


class Migration(migrations.Migration):
    """Migración inicial del catálogo."""

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Producto",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("nombre", models.CharField(max_length=120)),
                (
                    "categoria",
                    models.CharField(
                        choices=[
                            ("celular", "Celulares"),
                            ("tablet", "Tablets"),
                            ("reloj", "Relojes inteligentes"),
                            ("laptop", "Laptops"),
                        ],
                        db_index=True,
                        max_length=20,
                    ),
                ),
                ("descripcion", models.TextField(blank=True, default="")),
                (
                    "precio",
                    models.DecimalField(
                        decimal_places=2,
                        max_digits=10,
                        validators=[django.core.validators.MinValueValidator(Decimal("0.01"))],
                    ),
                ),
                ("imagen_url", models.URLField(max_length=500)),
                ("creado_en", models.DateTimeField(auto_now_add=True)),
            ],
            options={
                "verbose_name": "Producto",
                "verbose_name_plural": "Productos",
                "ordering": ["categoria", "nombre"],
            },
        ),
    ]
