"""
ASGI config for edx_stats project.
"""

import os

from django.core.asgi import get_asgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'edx_stats.settings')

application = get_asgi_application()