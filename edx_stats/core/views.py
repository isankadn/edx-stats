from django.views.generic import TemplateView, View
from django.http import HttpResponse
from django.shortcuts import render
from django.utils import timezone
from django.db.models import Sum

from .models import CourseStats, UserStats, CountryStats, YearlyStats
from .edx_db import (
    fetch_course_stats,
    fetch_total_users,
    fetch_users_by_country,
    fetch_users_by_year
)


class DashboardView(TemplateView):
    """Main dashboard view"""
    template_name = 'core/dashboard.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Get the latest stats
        try:
            user_stats = UserStats.objects.latest('last_updated')
        except UserStats.DoesNotExist:
            user_stats = None

        # Get course stats
        course_stats = CourseStats.objects.all().order_by('-enrollment_count')[:10]

        # Get country stats
        country_stats = CountryStats.objects.all().order_by('-user_count')[:10]

        # Get yearly stats
        yearly_stats = YearlyStats.objects.all().order_by('year')

        context.update({
            'user_stats': user_stats,
            'course_stats': course_stats,
            'country_stats': country_stats,
            'yearly_stats': yearly_stats,
            'total_courses': CourseStats.objects.count(),
            'total_enrollments': CourseStats.objects.aggregate(total=Sum('enrollment_count'))['total'] or 0,
        })

        return context


class CourseListView(TemplateView):
    """View for listing all courses"""
    template_name = 'core/course_list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['courses'] = CourseStats.objects.all().order_by('-enrollment_count')
        return context


class CountryListView(TemplateView):
    """View for listing all countries"""
    template_name = 'core/country_list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['countries'] = CountryStats.objects.all().order_by('-user_count')
        return context


class YearlyStatsView(TemplateView):
    """View for yearly statistics"""
    template_name = 'core/yearly_stats.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['yearly_stats'] = YearlyStats.objects.all().order_by('year')
        return context


class RefreshStatsView(View):
    """View for refreshing statistics from the Open edX database"""

    def get(self, request, *args, **kwargs):
        # Refresh course stats
        courses = fetch_course_stats()
        for course in courses:
            CourseStats.objects.update_or_create(
                course_id=course['course_id'],
                defaults={
                    'display_name': course['display_name'],
                    'enrollment_count': course['enrollment_count'],
                }
            )

        # Refresh user stats
        total_users = fetch_total_users()
        UserStats.objects.create(total_users=total_users)

        # Refresh country stats
        countries = fetch_users_by_country()
        for country in countries:
            CountryStats.objects.update_or_create(
                country_code=country['country_code'],
                defaults={
                    'country_name': country['country_name'],
                    'user_count': country['user_count'],
                }
            )

        # Refresh yearly stats
        yearly_data = fetch_users_by_year()
        for data in yearly_data:
            YearlyStats.objects.update_or_create(
                year=data['year'],
                defaults={
                    'new_users': data['new_users'],
                    'new_enrollments': data['new_enrollments'],
                }
            )

        # Return a simple response
        return HttpResponse(f"Statistics refreshed at {timezone.now()}")


# HTMX Views for partial updates
class HtmxCourseListView(View):
    """HTMX view for course list"""

    def get(self, request, *args, **kwargs):
        courses = CourseStats.objects.all().order_by('-enrollment_count')
        return render(request, 'core/partials/course_list.html', {'courses': courses})


class HtmxCountryListView(View):
    """HTMX view for country list"""

    def get(self, request, *args, **kwargs):
        countries = CountryStats.objects.all().order_by('-user_count')
        return render(request, 'core/partials/country_list.html', {'countries': countries})


class HtmxYearlyStatsView(View):
    """HTMX view for yearly stats"""

    def get(self, request, *args, **kwargs):
        yearly_stats = YearlyStats.objects.all().order_by('year')
        return render(request, 'core/partials/yearly_stats.html', {'yearly_stats': yearly_stats})


class HtmxDashboardStatsView(View):
    """HTMX view for dashboard stats"""

    def get(self, request, *args, **kwargs):
        try:
            user_stats = UserStats.objects.latest('last_updated')
        except UserStats.DoesNotExist:
            user_stats = None

        total_courses = CourseStats.objects.count()
        total_enrollments = CourseStats.objects.aggregate(total=Sum('enrollment_count'))['total'] or 0

        return render(request, 'core/partials/dashboard_stats.html', {
            'user_stats': user_stats,
            'total_courses': total_courses,
            'total_enrollments': total_enrollments,
        })