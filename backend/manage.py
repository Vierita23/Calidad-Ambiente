#!/usr/bin/env python
# =============================================================================
# Archivo: manage.py
# Carpeta: backend/
# Propósito: Punto de entrada oficial de comandos administrativos de Django
#            (migraciones, servidor de desarrollo, shell, etc.).
# Nota: En Docker usamos principalmente `migrate` y Gunicorn desde el Dockerfile.
# =============================================================================
import os
import sys


def main() -> None:
    """Configura Django y delega la ejecución al sistema de comandos."""
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:  # pragma: no cover - mensaje útil en despliegues
        raise ImportError(
            "No se pudo importar Django. ¿Instalaste dependencias con pip?"
        ) from exc
    execute_from_command_line(sys.argv)


if __name__ == "__main__":
    main()
