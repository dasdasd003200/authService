# config/asgi.py - CORREGIDO para async
"""
ASGI config for authservice project.
"""

import os
from django.core.asgi import get_asgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")

# IMPORTANTE: Obtener la aplicación ASGI para manejar async
application = get_asgi_application()

