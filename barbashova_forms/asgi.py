"""
ASGI config for barbashova_forms project.
"""

import os

from django.core.asgi import get_asgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "barbashova_forms.settings")

application = get_asgi_application()
