# =============================================================================
# Archivo: catalog/admin.py
# Carpeta: backend/catalog/
# Propósito: Registro de modelos en el panel administrativo de Django.
# =============================================================================
from django.contrib import admin

from catalog.models import Producto


@admin.register(Producto)
class ProductoAdmin(admin.ModelAdmin):
    """Configuración de columnas y búsqueda para gestionar productos."""

    list_display = ("nombre", "marca", "categoria", "precio", "moneda", "creado_en")
    list_filter = ("categoria",)
    search_fields = ("nombre", "descripcion")
