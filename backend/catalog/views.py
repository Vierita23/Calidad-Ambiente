# =============================================================================
# Archivo: catalog/views.py
# Carpeta: backend/catalog/
# Propósito: Vistas REST para consultar productos desde Angular.
# =============================================================================
from django.db.models import QuerySet
from rest_framework import mixins, viewsets
from rest_framework.permissions import AllowAny

from catalog.models import Producto
from catalog.serializers import ProductoSerializer


class ProductoViewSet(mixins.ListModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    """
    Endpoint de solo lectura:
    - GET /api/productos/        -> lista
    - GET /api/productos/{id}/   -> detalle

    Nota: No implementamos creación/edición pública; eso se haría vía admin o API privada.
    """

    permission_classes = [AllowAny]
    serializer_class = ProductoSerializer
    # Desactivamos paginación global solo para este ViewSet: el catálogo demo es pequeño
    # y el frontend consume un arreglo JSON directo.
    pagination_class = None

    def get_queryset(self) -> QuerySet[Producto]:
        """Permite filtrar por categoría con `?categoria=celular`."""
        qs = Producto.objects.all()
        categoria = self.request.query_params.get("categoria")
        if categoria:
            qs = qs.filter(categoria=categoria)
        return qs
