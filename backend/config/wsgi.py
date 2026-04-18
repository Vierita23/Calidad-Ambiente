# =============================================================================
# Archivo: config/wsgi.py
# Carpeta: backend/config/
# Propósito: Punto de entrada WSGI usado por Gunicorn en Docker.
# =============================================================================
import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")

application = get_wsgi_application()
