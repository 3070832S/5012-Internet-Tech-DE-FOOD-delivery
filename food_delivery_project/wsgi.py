"""
WSGI config for food_delivery_project project.
"""

import os
from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'food_delivery_project.settings')

application = get_wsgi_application()