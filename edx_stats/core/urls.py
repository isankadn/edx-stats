from django.urls import path
from . import views

app_name = 'core'

urlpatterns = [
    # Main views
    path('', views.DashboardView.as_view(), name='dashboard'),
    path('courses/', views.CourseListView.as_view(), name='course_list'),
    path('countries/', views.CountryListView.as_view(), name='country_list'),
    path('yearly/', views.YearlyStatsView.as_view(), name='yearly_stats'),
    path('refresh/', views.RefreshStatsView.as_view(), name='refresh_stats'),

    # HTMX partial views
    path('htmx/courses/', views.HtmxCourseListView.as_view(), name='htmx_course_list'),
    path('htmx/countries/', views.HtmxCountryListView.as_view(), name='htmx_country_list'),
    path('htmx/yearly/', views.HtmxYearlyStatsView.as_view(), name='htmx_yearly_stats'),
    path('htmx/dashboard-stats/', views.HtmxDashboardStatsView.as_view(), name='htmx_dashboard_stats'),
]