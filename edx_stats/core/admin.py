from django.contrib import admin
from .models import CourseStats, UserStats, CountryStats, YearlyStats

@admin.register(CourseStats)
class CourseStatsAdmin(admin.ModelAdmin):
    list_display = ('display_name', 'course_id', 'enrollment_count', 'last_updated')
    search_fields = ('display_name', 'course_id')
    ordering = ('-enrollment_count',)


@admin.register(UserStats)
class UserStatsAdmin(admin.ModelAdmin):
    list_display = ('total_users', 'last_updated')


@admin.register(CountryStats)
class CountryStatsAdmin(admin.ModelAdmin):
    list_display = ('country_name', 'country_code', 'user_count', 'last_updated')
    search_fields = ('country_name', 'country_code')
    ordering = ('-user_count',)


@admin.register(YearlyStats)
class YearlyStatsAdmin(admin.ModelAdmin):
    list_display = ('year', 'new_users', 'new_enrollments', 'last_updated')
    ordering = ('-year',)