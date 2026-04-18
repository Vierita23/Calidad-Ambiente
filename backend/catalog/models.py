# =============================================================================
# Archivo: catalog/models.py
# Carpeta: backend/catalog/
# Propósito: Modelos de datos del catálogo (productos tecnológicos).
# Nota: Las imágenes se referencian por URL para simplificar Docker y despliegue.
# =============================================================================
from __future__ import annotations

from decimal import Decimal

from django.core.validators import MinValueValidator
from django.db import models


class Producto(models.Model):
    """
    Representa un artículo vendible en la tienda (celular, tablet, etc.).

    Campos principales:
    - `categoria`: clasifica el producto para filtros en el frontend.
    - `imagen_url`: URL pública de la imagen (puede ser Unsplash u otro CDN).
    """

    class Categoria(models.TextChoices):
        """Valores permitidos para `categoria` (expuestos también vía API)."""

        CELULAR = "celular", "Celulares"
        TABLET = "tablet", "Tablets"
        RELOJ = "reloj", "Relojes inteligentes"
        LAPTOP = "laptop", "Laptops"

    nombre = models.CharField(max_length=120)
    marca = models.CharField(
        max_length=80,
        blank=True,
        default="",
        help_text="Marca comercial (Apple, Samsung, Xiaomi, etc.).",
    )
    categoria = models.CharField(max_length=20, choices=Categoria.choices, db_index=True)
    descripcion = models.TextField(blank=True, default="")
    precio = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(Decimal("0.01"))],
    )
    moneda = models.CharField(
        max_length=8,
        default="USD",
        help_text="Código ISO de moneda para mostrar precios (ej. USD).",
    )
    imagen_url = models.URLField(max_length=500)

    creado_en = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["categoria", "nombre"]
        verbose_name = "Producto"
        verbose_name_plural = "Productos"

    def __str__(self) -> str:
        """Texto legible para el admin y depuración."""
        return f"{self.nombre} ({self.get_categoria_display()})"
