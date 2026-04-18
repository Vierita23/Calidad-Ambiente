# =============================================================================
# Archivo: catalog/urls.py
# Carpeta: backend/catalog/
# Propósito: Rutas REST del catálogo (montadas bajo `/api/` en `config/urls.py`).
# =============================================================================
from django.urls import include, path
from rest_framework.routers import DefaultRouter

from catalog.views import ProductoViewSet

router = DefaultRouter()
router.register("productos", ProductoViewSet, basename="producto")

urlpatterns = [
    path("", include(router.urls)),
]
