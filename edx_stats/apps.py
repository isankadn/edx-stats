from django.apps import AppConfig


class EdxStatsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'edx_stats'
    verbose_name = 'Open edX Statistics'

    def ready(self):
        """
        Connect signal handlers when the app is ready.
        """
        # Import signal handlers
        from . import signals  # pylint: disable=unused-import