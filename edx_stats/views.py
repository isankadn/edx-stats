"""
Views for the edx_stats application.
"""
import logging
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, get_user_model
from django.db.models import Count
from django.db.models.functions import ExtractYear
from openedx.core.djangoapps.content.course_overviews.models import CourseOverview
from common.djangoapps.student.models import CourseEnrollment, UserProfile
from openedx.core.djangoapps.site_configuration import helpers as configuration_helpers
from django.conf import settings

from . import cache

logger = logging.getLogger(__name__)

User = get_user_model()
class StaffRequiredMixin:
    """Verify that the user has staff access."""
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_staff:
            return self.handle_no_permission()
        return super().dispatch(request, *args, **kwargs)


def get_course_stats():
    """Get course statistics."""
    return CourseOverview.objects.annotate(
        enrollment_count=Count('courseenrollment')
    ).order_by('-enrollment_count')


def get_country_stats():
    """Get country statistics."""
    return UserProfile.objects.exclude(
        country__isnull=True
    ).exclude(
        country=''
    ).values(
        'country'
    ).annotate(
        user_count=Count('user')
    ).order_by('-user_count')


def get_yearly_stats():
    """Get yearly statistics."""
    # Get user counts by year
    user_counts = User.objects.annotate(
        year=ExtractYear('date_joined')
    ).values('year').annotate(
        new_users=Count('id')
    ).order_by('year')

    # Get enrollment counts by year
    enrollment_counts = CourseEnrollment.objects.annotate(
        year=ExtractYear('created')
    ).values('year').annotate(
        new_enrollments=Count('id')
    ).order_by('year')

    # Combine user and enrollment stats
    years = set()
    year_data = {}

    for count in user_counts:
        year = count['year']
        years.add(year)
        if year not in year_data:
            year_data[year] = {'new_users': 0, 'new_enrollments': 0}
        year_data[year]['new_users'] = count['new_users']

    for count in enrollment_counts:
        year = count['year']
        years.add(year)
        if year not in year_data:
            year_data[year] = {'new_users': 0, 'new_enrollments': 0}
        year_data[year]['new_enrollments'] = count['new_enrollments']

    return [
        {'year': year, **year_data[year]}
        for year in sorted(years)
    ]


def get_total_stats():
    """Get total statistics."""
    logger.info("Getting total stats")
    logger.debug(f"CourseOverview.objects.count(): {CourseOverview.objects.count()}")
    logger.debug(f"CourseEnrollment.objects.count(): {CourseEnrollment.objects.count()}")
    logger.debug(f"User.objects.count(): {User.objects.count()}")
    return {
        'total_courses': CourseOverview.objects.count(),
        'total_enrollments': CourseEnrollment.objects.count(),
        'total_users': User.objects.count(),
    }


class DashboardView(LoginRequiredMixin, StaffRequiredMixin, TemplateView):
    """Main dashboard view"""
    template_name = 'edx_stats/dashboard.html'
    logger.info("Getting dashboard context")
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Get cached stats
        course_stats = cache.get_cached_stats(
            cache.get_cache_key('course_stats_top'),
            lambda: list(get_course_stats()[:10])
        )

        country_stats = cache.get_cached_stats(
            cache.get_cache_key('country_stats_top'),
            lambda: list(get_country_stats()[:10])
        )

        yearly_stats = cache.get_cached_stats(
            cache.get_cache_key('yearly_stats'),
            get_yearly_stats
        )

        total_stats = cache.get_cached_stats(
            cache.get_cache_key('total_stats'),
            get_total_stats
        )

        context.update({
            'course_stats': course_stats,
            'country_stats': country_stats,
            'yearly_stats': yearly_stats,
            **total_stats,
            'platform_name': configuration_helpers.get_value('PLATFORM_NAME', settings.PLATFORM_NAME),
        })

        return context


class CourseListView(LoginRequiredMixin, StaffRequiredMixin, TemplateView):
    """View for listing all courses"""
    template_name = 'edx_stats/course_list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['courses'] = cache.get_cached_stats(
            cache.get_cache_key('course_stats_all'),
            lambda: list(get_course_stats())
        )
        context['platform_name'] = configuration_helpers.get_value('PLATFORM_NAME', settings.PLATFORM_NAME)
        return context


class CountryListView(LoginRequiredMixin, StaffRequiredMixin, TemplateView):
    """View for listing all countries"""
    template_name = 'edx_stats/country_list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['countries'] = cache.get_cached_stats(
            cache.get_cache_key('country_stats_all'),
            lambda: list(get_country_stats())
        )
        context['platform_name'] = configuration_helpers.get_value('PLATFORM_NAME', settings.PLATFORM_NAME)
        return context


class YearlyStatsView(LoginRequiredMixin, StaffRequiredMixin, TemplateView):
    """View for yearly statistics"""
    template_name = 'edx_stats/yearly_stats.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['yearly_stats'] = cache.get_cached_stats(
            cache.get_cache_key('yearly_stats'),
            get_yearly_stats
        )
        context['platform_name'] = configuration_helpers.get_value('PLATFORM_NAME', settings.PLATFORM_NAME)
        return context