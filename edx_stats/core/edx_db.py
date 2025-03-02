"""
Utilities for interacting with the Open edX database
"""
import logging
from django.db import connections
from django.conf import settings
from django.db.utils import OperationalError

logger = logging.getLogger(__name__)

def get_edx_db_connection():
    """
    Get a connection to the Open edX database
    """
    if 'edx_readonly' not in connections.databases:
        # Add the connection dynamically
        connections.databases['edx_readonly'] = settings.EDX_DATABASE

    try:
        return connections['edx_readonly']
    except OperationalError as e:
        logger.error(f"Failed to connect to Open edX database: {e}")
        return None

def fetch_course_stats():
    """
    Fetch course statistics from the Open edX database

    Returns a list of dictionaries with course_id, display_name, and enrollment_count
    """
    connection = get_edx_db_connection()
    if not connection:
        return []

    with connection.cursor() as cursor:
        # Query to get course information and enrollment counts
        cursor.execute("""
            SELECT
                c.id as course_id,
                c.display_name,
                COUNT(ce.id) as enrollment_count
            FROM
                course_overviews_courseoverview c
            LEFT JOIN
                student_courseenrollment ce ON c.id = ce.course_id
            GROUP BY
                c.id, c.display_name
            ORDER BY
                enrollment_count DESC
        """)

        columns = [col[0] for col in cursor.description]
        return [dict(zip(columns, row)) for row in cursor.fetchall()]

def fetch_total_users():
    """
    Fetch the total number of users from the Open edX database

    Returns an integer
    """
    connection = get_edx_db_connection()
    if not connection:
        return 0

    with connection.cursor() as cursor:
        cursor.execute("SELECT COUNT(*) FROM auth_user")
        return cursor.fetchone()[0]

def fetch_users_by_country():
    """
    Fetch user counts by country from the Open edX database

    Returns a list of dictionaries with country_code, country_name, and user_count
    """
    connection = get_edx_db_connection()
    if not connection:
        return []

    with connection.cursor() as cursor:
        # Query to get user counts by country
        cursor.execute("""
            SELECT
                up.country as country_code,
                up.country as country_name,
                COUNT(u.id) as user_count
            FROM
                auth_user u
            JOIN
                auth_userprofile up ON u.id = up.user_id
            WHERE
                up.country IS NOT NULL AND up.country != ''
            GROUP BY
                up.country
            ORDER BY
                user_count DESC
        """)

        columns = [col[0] for col in cursor.description]
        return [dict(zip(columns, row)) for row in cursor.fetchall()]

def fetch_users_by_year():
    """
    Fetch user and enrollment counts by year from the Open edX database

    Returns a list of dictionaries with year, new_users, and new_enrollments
    """
    connection = get_edx_db_connection()
    if not connection:
        return []

    with connection.cursor() as cursor:
        # Query to get user counts by year
        cursor.execute("""
            SELECT
                YEAR(date_joined) as year,
                COUNT(*) as new_users
            FROM
                auth_user
            GROUP BY
                YEAR(date_joined)
            ORDER BY
                year
        """)

        user_results = cursor.fetchall()

        # Query to get enrollment counts by year
        cursor.execute("""
            SELECT
                YEAR(created) as year,
                COUNT(*) as new_enrollments
            FROM
                student_courseenrollment
            GROUP BY
                YEAR(created)
            ORDER BY
                year
        """)

        enrollment_results = cursor.fetchall()

        # Combine the results
        years = set([r[0] for r in user_results] + [r[0] for r in enrollment_results])
        result = []

        for year in sorted(years):
            user_count = next((r[1] for r in user_results if r[0] == year), 0)
            enrollment_count = next((r[1] for r in enrollment_results if r[0] == year), 0)

            result.append({
                'year': year,
                'new_users': user_count,
                'new_enrollments': enrollment_count
            })

        return result