# Open edX Statistics

A Django app for displaying statistics and analytics for Open edX instances. This app integrates directly with your Open edX installation and provides real-time statistics about courses, enrollments, and user demographics.

## Features

- Real-time dashboard with key statistics
- Course statistics (enrollments, active courses)
- User demographics (users by country)
- Yearly growth statistics
- Redis-based caching for performance
- Multi-site support

## Requirements

- Open edX (Olive release or later)
- Django 3.2
- Redis (uses Open edX's existing Redis setup)

## Installation

1. Install the package:

```bash
pip install -e git+https://github.com/yourusername/edx-stats.git#egg=edx-stats
```

2. Add to your INSTALLED_APPS in `lms/envs/common.py`:

```python
INSTALLED_APPS = [
    # ...
    'edx_stats',
    # ...
]
```

3. Include the URLs in your project's `lms/urls.py`:

```python
urlpatterns = [
    # ...
    path('stats/', include('edx_stats.urls')),
    # ...
]
```

## Configuration

This app uses your existing Open edX database and Redis configuration. No additional database setup is required.

### Cache Settings

The app uses Open edX's default Redis cache configuration. You can customize the cache timeout in your settings:

```python
# In lms/envs/common.py or lms/envs/production.py
STATS_CACHE_TIMEOUT = 3600  # Cache timeout in seconds (default: 1 hour)
```

### Permissions

Access to the statistics is restricted to staff users only. Make sure users have the appropriate staff permissions in the Django admin interface.

## Usage

1. Visit `/stats/` on your Open edX LMS
2. Navigate through different sections:
   - Dashboard: Overview of key statistics
   - Courses: Detailed course enrollment statistics
   - Countries: User distribution by country
   - Yearly Stats: Growth trends over time

## Performance Considerations

- All statistics are cached in Redis with a default timeout of 1 hour
- Cache is automatically invalidated when relevant data changes
- Each site in a multi-site installation has its own cache namespace
- Direct integration with Open edX models ensures data consistency

## Development

1. Clone the repository:
```bash
git clone https://github.com/yourusername/edx-stats.git
cd edx-stats
```

2. Install development requirements:
```bash
pip install -e ".[dev]"
```

3. Run tests:
```bash
pytest
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## License

AGPL v3

## Notes

- This app integrates directly with Open edX's database using Django ORM
- No separate database configuration is needed
- Uses Open edX's existing Redis setup for caching
- All queries are optimized and cached for performance