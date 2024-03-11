"""
WSGI config for prediction_of_Parkinsons_illness

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.0/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'prediction_of_Parkinsons_illness.settings')
application = get_wsgi_application()
