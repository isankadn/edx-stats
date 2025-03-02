"""
Signal handlers for edx_stats.
"""
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.contrib.auth.models import User
from openedx.core.djangoapps.content.course_overviews.models import CourseOverview
from common.djangoapps.student.models import CourseEnrollment, UserProfile

from . import cache

@receiver([post_save, post_delete], sender=CourseOverview)
def invalidate_course_stats(sender, **kwargs):
    """Invalidate course stats cache when a course is updated."""
    cache.invalidate_stats_cache()

@receiver([post_save, post_delete], sender=CourseEnrollment)
def invalidate_enrollment_stats(sender, **kwargs):
    """Invalidate enrollment stats cache when enrollments change."""
    cache.invalidate_stats_cache()

@receiver([post_save, post_delete], sender=User)
def invalidate_user_stats(sender, **kwargs):
    """Invalidate user stats cache when users are updated."""
    cache.invalidate_stats_cache()

@receiver([post_save, post_delete], sender=UserProfile)
def invalidate_profile_stats(sender, **kwargs):
    """Invalidate profile stats cache when user profiles are updated."""
    cache.invalidate_stats_cache()