"""
Cache utilities for edx_stats using Open edX's Redis setup.
"""
from django.core.cache import cache
from django.conf import settings
from openedx.core.djangoapps.site_configuration import helpers as configuration_helpers

# Cache keys
STATS_CACHE_KEY_PREFIX = 'edx_stats:'
COURSE_STATS_CACHE_KEY = f'{STATS_CACHE_KEY_PREFIX}course_stats'
COUNTRY_STATS_CACHE_KEY = f'{STATS_CACHE_KEY_PREFIX}country_stats'
YEARLY_STATS_CACHE_KEY = f'{STATS_CACHE_KEY_PREFIX}yearly_stats'
TOTAL_STATS_CACHE_KEY = f'{STATS_CACHE_KEY_PREFIX}total_stats'

# Cache timeout (in seconds)
STATS_CACHE_TIMEOUT = getattr(settings, 'STATS_CACHE_TIMEOUT', 3600)  # 1 hour default

def get_cache_key(key_suffix):
    """
    Get a cache key with the site-specific prefix.
    """
    site_prefix = configuration_helpers.get_value('SITE_NAME', 'default')
    return f'{STATS_CACHE_KEY_PREFIX}{site_prefix}:{key_suffix}'

def get_cached_stats(cache_key, data_function):
    """
    Get stats from cache or compute them if not cached.

    Args:
        cache_key (str): The cache key to use
        data_function (callable): Function to call to compute the data if not cached

    Returns:
        The cached or computed data
    """
    data = cache.get(cache_key)
    if data is None:
        data = data_function()
        cache.set(cache_key, data, STATS_CACHE_TIMEOUT)
    return data

def invalidate_stats_cache():
    """
    Invalidate all stats cache.
    """
    cache.delete_pattern(f'{STATS_CACHE_KEY_PREFIX}*')