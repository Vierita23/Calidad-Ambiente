# =============================================================================
# Archivo: config/urls.py
# Carpeta: backend/config/
# Propósito: Enrutamiento global del proyecto Django.
# Rutas:
# - /admin/  -> panel administrativo
# - /api/    -> endpoints REST del catálogo
# =============================================================================
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("admin/", admin.site.urls),
    # Toda la API del negocio vive bajo el prefijo `/api/` para alinearla con Nginx.
    path("api/", include("catalog.urls")),
]
