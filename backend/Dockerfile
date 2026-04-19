# =============================================================================
# Archivo: Dockerfile
# Carpeta: backend/
# Propósito: Imagen Docker del API Django (Python) con Gunicorn.
# Etapas: una sola etapa simple para claridad en proyectos académicos.
#
# El entrypoint se copia fuera de `/app` y se normaliza a LF porque en Windows
# `docker-compose` suele montar `./backend:/app` con CRLF y rompe `set -eu`.
# =============================================================================
FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

RUN apt-get update \
  && apt-get install -y --no-install-recommends libpq5 \
  && rm -rf /var/lib/apt/lists/*

COPY requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r /app/requirements.txt

COPY entrypoint.sh /usr/local/bin/dt-backend-entrypoint.sh
RUN sed -i 's/\r$//' /usr/local/bin/dt-backend-entrypoint.sh \
  && chmod +x /usr/local/bin/dt-backend-entrypoint.sh

COPY . /app

EXPOSE 8000

ENTRYPOINT ["/bin/sh", "/usr/local/bin/dt-backend-entrypoint.sh"]
