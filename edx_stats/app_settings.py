"""
Default settings for the edx_stats app.
"""
from django.conf import settings

# Refresh interval in seconds (default: 1 hour)
STATS_REFRESH_INTERVAL = getattr(settings, 'STATS_REFRESH_INTERVAL', 3600)

# Number of top items to show in dashboard
STATS_DASHBOARD_TOP_ITEMS = getattr(settings, 'STATS_DASHBOARD_TOP_ITEMS', 10)

# Login URL (use Open edX's login URL)
LOGIN_URL = getattr(settings, 'LOGIN_URL', '/login')