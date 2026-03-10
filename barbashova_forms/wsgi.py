"""
WSGI config for barbashova_forms project.
"""

import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "barbashova_forms.settings")

application = get_wsgi_application()
