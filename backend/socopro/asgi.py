"""ASGI config for socopro project."""
import os
from django.core.asgi import get_asgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'socopro.settings')
application = get_asgi_application()
