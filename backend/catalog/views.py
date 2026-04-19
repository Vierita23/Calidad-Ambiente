# =============================================================================
# Archivo: catalog/views.py
# Carpeta: backend/catalog/
# Propósito: Vistas REST para consultar productos desde Angular.
# =============================================================================
from django.db.models import Q, QuerySet
from rest_framework import mixins, viewsets
from rest_framework.permissions import AllowAny

from catalog.models import Producto
from catalog.serializers import ProductoSerializer


class ProductoViewSet(mixins.ListModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    """
    Endpoint de solo lectura:
    - GET /api/productos/        -> lista
    - GET /api/productos/{id}/   -> detalle

    Query params (lista):
    - `categoria`: celular | tablet | reloj | laptop
    - `q`: texto en nombre, marca o descripción (icontains)
    - `ordering`: -creado_en | precio | -precio | nombre | -nombre | id | -id
    """

    permission_classes = [AllowAny]
    serializer_class = ProductoSerializer
    pagination_class = None

    _ordering_map = {
        "precio": "precio",
        "-precio": "-precio",
        "nombre": "nombre",
        "-nombre": "-nombre",
        "creado_en": "creado_en",
        "-creado_en": "-creado_en",
        "id": "id",
        "-id": "-id",
    }

    def get_queryset(self) -> QuerySet[Producto]:
        qs = Producto.objects.all()

        categoria = self.request.query_params.get("categoria")
        if categoria:
            qs = qs.filter(categoria=categoria)

        q = (self.request.query_params.get("q") or "").strip()
        if q:
            qs = qs.filter(
                Q(nombre__icontains=q) | Q(marca__icontains=q) | Q(descripcion__icontains=q),
            )

        ordering = (self.request.query_params.get("ordering") or "").strip()
        if ordering in self._ordering_map:
            qs = qs.order_by(self._ordering_map[ordering])

        return qs
