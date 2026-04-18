# =============================================================================
# Archivo: config/settings.py
# Carpeta: backend/config/
# Propósito: Configuración central de Django (BD, apps instaladas, CORS, DRF).
# Variables de entorno: permiten cambiar credenciales sin editar código.
# =============================================================================
from __future__ import annotations

import os
from pathlib import Path

# -----------------------------------------------------------------------------
# Rutas base
# -----------------------------------------------------------------------------
# BASE_DIR apunta a la carpeta `backend/` (donde está manage.py).
BASE_DIR = Path(__file__).resolve().parent.parent


# -----------------------------------------------------------------------------
# Seguridad / modo debug
# -----------------------------------------------------------------------------
# SECRET_KEY debe ser distinta en producción real (idealmente variable de entorno).
SECRET_KEY = os.environ.get(
    "DJANGO_SECRET_KEY",
    "clave-solo-para-desarrollo-cambiar-en-produccion",
)

# DEBUG=True en desarrollo; en Docker lo dejamos True por claridad del taller,
# pero en producción real debería ser False.
DEBUG = os.environ.get("DJANGO_DEBUG", "true").lower() in {"1", "true", "yes"}

# Hosts permitidos: incluimos nombres típicos de Docker y localhost.
ALLOWED_HOSTS = [
    h.strip()
    for h in os.environ.get("DJANGO_ALLOWED_HOSTS", "localhost,127.0.0.1,backend").split(",")
    if h.strip()
]


# -----------------------------------------------------------------------------
# Apps instaladas
# -----------------------------------------------------------------------------
INSTALLED_APPS = [
    # Apps nativas de Django
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    # Terceros
    "rest_framework",
    "corsheaders",
    # Propio del proyecto
    "catalog.apps.CatalogConfig",
]


# -----------------------------------------------------------------------------
# Middleware
# -----------------------------------------------------------------------------
MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]


# -----------------------------------------------------------------------------
# URLs / WSGI
# -----------------------------------------------------------------------------
ROOT_URLCONF = "config.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    }
]

WSGI_APPLICATION = "config.wsgi.application"


# -----------------------------------------------------------------------------
# Base de datos (PostgreSQL)
# -----------------------------------------------------------------------------
# En docker-compose el host suele llamarse `db`.
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": os.environ.get("POSTGRES_DB", "tienda"),
        "USER": os.environ.get("POSTGRES_USER", "tienda"),
        "PASSWORD": os.environ.get("POSTGRES_PASSWORD", "tienda"),
        "HOST": os.environ.get("POSTGRES_HOST", "localhost"),
        "PORT": os.environ.get("POSTGRES_PORT", "5432"),
    }
}


# -----------------------------------------------------------------------------
# Validación de contraseñas (por defecto de Django)
# -----------------------------------------------------------------------------
AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]


# -----------------------------------------------------------------------------
# Internacionalización
# -----------------------------------------------------------------------------
LANGUAGE_CODE = "es-es"
TIME_ZONE = "America/Mexico_City"
USE_I18N = True
USE_TZ = True


# -----------------------------------------------------------------------------
# Archivos estáticos
# -----------------------------------------------------------------------------
STATIC_URL = "static/"
STATIC_ROOT = BASE_DIR / "staticfiles"


# -----------------------------------------------------------------------------
# Modelo de usuario por defecto
# -----------------------------------------------------------------------------
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"


# -----------------------------------------------------------------------------
# CORS (Angular en otro puerto u otro host)
# -----------------------------------------------------------------------------
# En desarrollo Angular suele correr en :4200.
CORS_ALLOWED_ORIGINS = [
    o.strip()
    for o in os.environ.get(
        "DJANGO_CORS_ALLOWED_ORIGINS",
        "http://localhost:4200,http://127.0.0.1:4200,http://localhost,http://127.0.0.1",
    ).split(",")
    if o.strip()
]

# Permite enviar cookies/encabezados si en el futuro agregas autenticación basada en sesión.
CORS_ALLOW_CREDENTIALS = True


# -----------------------------------------------------------------------------
# Django REST Framework
# -----------------------------------------------------------------------------
REST_FRAMEWORK = {
    # Paginación simple para que el catálogo no crezca sin control en el futuro.
    "DEFAULT_PAGINATION_CLASS": "rest_framework.pagination.PageNumberPagination",
    "PAGE_SIZE": 50,
}
