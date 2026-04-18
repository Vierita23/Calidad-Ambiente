# =============================================================================
# Archivo: config/asgi.py
# Carpeta: backend/config/
# Propósito: Punto de entrada ASGI (servidores asíncronos / WebSockets).
# En este proyecto el despliegue principal usa WSGI (Gunicorn), pero Django
# requiere este archivo por convención.
# =============================================================================
import os

from django.core.asgi import get_asgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")

application = get_asgi_application()
