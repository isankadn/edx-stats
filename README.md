# edX Stats

A Django app for displaying statistics and analytics for Open edX instances.

## Features

- Dashboard with key statistics
- Course statistics (number of courses, course names, enrollments)
- User statistics (total users, users by country, users by year)
- HTMX integration for dynamic updates

## Installation

1. Install the package:

```bash
pip install -e git+https://github.com/yourusername/edx-stats.git#egg=edx-stats
```

Or add to your requirements.txt:

```
-e git+https://github.com/yourusername/edx-stats.git#egg=edx-stats
```

2. Add to your INSTALLED_APPS in settings.py:

```python
INSTALLED_APPS = [
    # ...
    'django_htmx',
    'edx_stats',
    # ...
]
```

3. Add the middleware in settings.py:

```python
MIDDLEWARE = [
    # ...
    'django_htmx.middleware.HtmxMiddleware',
    # ...
]
```

4. Configure the database connection to your Open edX database:

```python
# For connecting to Open edX MySQL database
EDX_DATABASE = {
    'ENGINE': os.getenv('EDX_DB_ENGINE', 'django.db.backends.mysql'),
    'NAME': os.getenv('EDX_DB_NAME', 'edxapp'),
    'USER': os.getenv('EDX_DB_USER', 'edxapp001'),
    'PASSWORD': os.getenv('EDX_DB_PASSWORD', ''),
    'HOST': os.getenv('EDX_DB_HOST', 'mysql'),
    'PORT': os.getenv('EDX_DB_PORT', '3306'),
}
```

5. Include the URLs in your project's urls.py:

```python
urlpatterns = [
    # ...
    path('stats/', include('edx_stats.urls')),
    # ...
]
```

6. Run migrations:

```bash
python manage.py migrate edx_stats
```

## Usage

1. Visit the dashboard at `/stats/`
2. Use the "Refresh Stats" button to fetch the latest data from your Open edX database
3. Navigate through the different views to see detailed statistics

## Compatibility

This app is compatible with Open edX Olive release and Django 3.2.

## License

AGPL v3