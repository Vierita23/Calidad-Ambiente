#!/usr/bin/env sh
# =============================================================================
# Archivo: entrypoint.sh
# Carpeta: backend/
# Propósito: Arranque del contenedor: aplica migraciones y levanta Gunicorn.
# =============================================================================
set -eu

echo "[entrypoint] Aplicando migraciones..."
python manage.py migrate --noinput

echo "[entrypoint] Iniciando Gunicorn..."
exec gunicorn config.wsgi:application --bind 0.0.0.0:8000 --workers 3
