import os
import sys

sys.path.insert(0, os.path.dirname(__file__))

# Reemplaza 'tu_proyecto' por la carpeta donde reside settings.py
os.environ['DJANGO_SETTINGS_MODULE'] = 'config.settings'

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()