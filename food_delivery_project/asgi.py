"""
ASGI config for food_delivery_project project.
"""

import os
from django.core.asgi import get_asgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'food_delivery_project.settings')

application = get_asgi_application()