"""
WSGI config for mvcproject project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/howto/deployment/wsgi/
"""

import os
from django.core.wsgi import get_wsgi_application

# Set the settings module for the 'mvcapi' app
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mvcproject.mvcapi_settings')

application = get_wsgi_application()
