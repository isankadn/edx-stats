from django.urls import path
from . import views

app_name = 'core'

urlpatterns = [
    # Main dashboard - the only full page
    path('', views.DashboardView.as_view(), name='dashboard'),

    # HTMX endpoints
    path('htmx/courses/', views.HtmxCourseListView.as_view(), name='htmx_courses'),
    path('htmx/countries/', views.HtmxCountryListView.as_view(), name='htmx_countries'),
    path('htmx/yearly-stats/', views.HtmxYearlyStatsView.as_view(), name='htmx_yearly_stats'),
    path('htmx/dashboard-stats/', views.HtmxDashboardStatsView.as_view(), name='htmx_dashboard_stats'),

    # Data refresh endpoint
    path('refresh/', views.RefreshStatsView.as_view(), name='refresh_stats'),
]