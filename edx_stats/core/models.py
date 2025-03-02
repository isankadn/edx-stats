from django.db import models

# These models are for caching data from the Open edX database
# We'll use them to store aggregated statistics

class CourseStats(models.Model):
    """Statistics for a course"""
    course_id = models.CharField(max_length=255, unique=True)
    display_name = models.CharField(max_length=255)
    enrollment_count = models.IntegerField(default=0)
    last_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.display_name} ({self.course_id})"


class UserStats(models.Model):
    """Aggregated user statistics"""
    total_users = models.IntegerField(default=0)
    last_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"User Stats (Last updated: {self.last_updated})"


class CountryStats(models.Model):
    """User statistics by country"""
    country_code = models.CharField(max_length=2, unique=True)
    country_name = models.CharField(max_length=255)
    user_count = models.IntegerField(default=0)
    last_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.country_name} ({self.user_count} users)"


class YearlyStats(models.Model):
    """User statistics by year"""
    year = models.IntegerField(unique=True)
    new_users = models.IntegerField(default=0)
    new_enrollments = models.IntegerField(default=0)
    last_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Stats for {self.year}"