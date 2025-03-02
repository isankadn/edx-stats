from django.views.generic import TemplateView, View
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from django.utils import timezone
from django.db.models import Count, Sum
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import get_user_model
from django.db.models.functions import ExtractYear
from django.core.cache import cache
import logging
import redis
from django.conf import settings

from openedx.core.djangoapps.content.course_overviews.models import CourseOverview
from common.djangoapps.student.models import CourseEnrollment, UserProfile
from openedx.core.djangoapps.site_configuration import helpers as configuration_helpers
from common.djangoapps.student.models import User as OpenEdxUser

logger = logging.getLogger(__name__)

User = get_user_model()

def check_redis_connection():
    """Check Redis connection and log the status"""
    try:
        # Try to get Redis configuration from Django settings
        redis_host = getattr(settings, 'REDIS_HOST', 'localhost')
        redis_port = getattr(settings, 'REDIS_PORT', 6379)
        redis_db = getattr(settings, 'REDIS_DB', 0)

        # Create Redis connection
        redis_client = redis.Redis(
            host=redis_host,
            port=redis_port,
            db=redis_db,
            socket_timeout=1
        )

        # Test connection
        redis_client.ping()
        logger.info("Redis connection successful")
        return True
    except Exception as e:
        logger.error(f"Redis connection failed: {str(e)}")
        return False

class DashboardView(LoginRequiredMixin, TemplateView):
    """Main dashboard view - the only full page view we need"""
    template_name = 'core/dashboard.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class HtmxCourseListView(LoginRequiredMixin, View):
    """HTMX view for course list"""

    def get(self, request, *args, **kwargs):
        courses = CourseOverview.objects.annotate(
            enrollment_count=Count('courseenrollment')
        ).order_by('-enrollment_count')[:10]

        return render(request, 'core/partials/course_list.html', {'courses': courses})


class HtmxCountryListView(LoginRequiredMixin, View):
    """HTMX view for country list"""

    def get(self, request, *args, **kwargs):
        countries = UserProfile.objects.values(
            'country'
        ).annotate(
            user_count=Count('id')
        ).filter(
            user__is_active=True
        ).exclude(
            country=''
        ).order_by('-user_count')[:10]

        return render(request, 'core/partials/country_list.html', {'countries': countries})


class HtmxYearlyStatsView(LoginRequiredMixin, View):
    """HTMX view for yearly stats"""

    def get(self, request, *args, **kwargs):
        yearly_stats = OpenEdxUser.objects.filter(
            is_active=True
        ).annotate(
            year=ExtractYear('date_joined')
        ).values('year').annotate(
            new_users=Count('id'),
            new_enrollments=Count('courseenrollment')
        ).order_by('year')

        return render(request, 'core/partials/yearly_stats.html', {'yearly_stats': yearly_stats})


class HtmxDashboardStatsView(LoginRequiredMixin, View):
    """HTMX view for dashboard stats"""

    def get(self, request, *args, **kwargs):
        # Check Redis connection
        redis_status = check_redis_connection()
        logger.info(f"Redis connection status: {redis_status}")

        # Clear cache for user-related queries
        cache.delete('user_count_cache')
        cache.delete('course_count_cache')
        cache.delete('enrollment_count_cache')

        try:
            # Debug the user query with .using('default') to ensure correct database
            users_query = OpenEdxUser.objects.using('default').filter(is_active=True)
            logger.info(f"User Query SQL: {str(users_query.query)}")
            total_users = users_query.count()
            logger.info(f"Total Users Result: {total_users}")

            # Try direct database query
            from django.db import connections
            with connections['default'].cursor() as cursor:
                cursor.execute("SELECT COUNT(*) FROM auth_user WHERE is_active = true")
                direct_count = cursor.fetchone()[0]
                logger.info(f"Direct SQL count: {direct_count}")

            # Also try alternative query without cache
            auth_user_query = get_user_model().objects.using('default').filter(is_active=True)
            logger.info(f"Auth User Query SQL: {str(auth_user_query.query)}")
            auth_total_users = auth_user_query.count()
            logger.info(f"Auth Total Users Result: {auth_total_users}")

            # Try querying UserProfile as well
            profile_query = UserProfile.objects.using('default').filter(user__is_active=True)
            logger.info(f"Profile Query SQL: {str(profile_query.query)}")
            profile_total = profile_query.count()
            logger.info(f"Profile Total Result: {profile_total}")

            total_courses = CourseOverview.objects.using('default').filter(ended__isnull=True).count()
            total_enrollments = CourseEnrollment.objects.using('default').filter(is_active=True).count()

            # Log current user info for debugging
            logger.info(f"Current user ID: {request.user.id}")
            logger.info(f"Current user is authenticated: {request.user.is_authenticated}")
            logger.info(f"Current user is active: {request.user.is_active}")

            return render(request, 'core/partials/dashboard_stats.html', {
                'total_users': total_users,
                'auth_total_users': auth_total_users,
                'profile_total': profile_total,
                'direct_count': direct_count,
                'total_courses': total_courses,
                'total_enrollments': total_enrollments,
                'redis_status': redis_status,
            })
        except Exception as e:
            logger.error(f"Error in dashboard stats: {str(e)}")
            return render(request, 'core/partials/dashboard_stats.html', {
                'error': str(e),
                'redis_status': redis_status
            })


class RefreshStatsView(LoginRequiredMixin, View):
    """View for refreshing statistics"""

    def get(self, request, *args, **kwargs):
        # Since we're using direct ORM queries now, we just need to return success
        return JsonResponse({
            'status': 'success',
            'message': f"Statistics refreshed at {timezone.now()}"
        })