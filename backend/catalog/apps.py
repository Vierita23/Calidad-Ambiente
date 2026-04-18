# =============================================================================
# Archivo: catalog/apps.py
# Carpeta: backend/catalog/
# Propósito: Configuración de la app Django `catalog` (nombre legible en admin).
# =============================================================================
from django.apps import AppConfig


class CatalogConfig(AppConfig):
    """Define metadatos de la app para el registro en INSTALLED_APPS."""

    default_auto_field = "django.db.models.BigAutoField"
    name = "catalog"
    verbose_name = "Catálogo de productos"
