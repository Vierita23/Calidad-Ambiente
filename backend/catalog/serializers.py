# =============================================================================
# Archivo: catalog/serializers.py
# Carpeta: backend/catalog/
# Propósito: Transforma modelos Django a JSON (y valida datos entrantes).
# =============================================================================
from rest_framework import serializers

from catalog.models import Producto


class ProductoSerializer(serializers.ModelSerializer):
    """
    Serializador del modelo `Producto`.

    `categoria_display` expone el nombre legible (ej. "Celulares") además del código.
    """

    categoria_display = serializers.CharField(source="get_categoria_display", read_only=True)

    class Meta:
        model = Producto
        fields = [
            "id",
            "nombre",
            "marca",
            "categoria",
            "categoria_display",
            "descripcion",
            "precio",
            "moneda",
            "imagen_url",
            "creado_en",
        ]
