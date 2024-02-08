"""
WSGI config for facemagic project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'elyon.settings')

paid = False

# if not paid:
#     application = make_payment_app()
# else:
#     application = get_wsgi_application()

application = get_wsgi_application()
