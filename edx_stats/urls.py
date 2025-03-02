from django.urls import path
from . import views

app_name = 'edx_stats'

urlpatterns = [
    # Main views
    path('', views.DashboardView.as_view(), name='dashboard'),
    path('courses/', views.CourseListView.as_view(), name='course_list'),
    path('countries/', views.CountryListView.as_view(), name='country_list'),
    path('yearly/', views.YearlyStatsView.as_view(), name='yearly_stats'),
]