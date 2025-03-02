from setuptools import setup, find_packages

setup(
    name="edx-stats",
    version="0.1.0",
    packages=find_packages(),
    include_package_data=True,
    package_data={
        'edx_stats': [
            'templates/*.html',
            'templates/edx_stats/*.html',
            'templates/edx_stats/partials/*.html',
            'static/*',
        ],
    },
    install_requires=[
        "Django>=3.2.12,<4.0",
        "django-htmx>=1.14.0",
    ],
    dependency_links=[
        "https://packages.edx.org/pypi/simple/",
    ],
    author="Open edX Community",
    author_email="info@openedx.org",
    description="Statistics and analytics for Open edX",
    long_description="Statistics and analytics for Open edX",
    url="https://github.com/openedx/edx-stats",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Framework :: Django",
        "Framework :: Django :: 3.2",
        "Intended Audience :: Education",
        "License :: OSI Approved :: GNU Affero General Public License v3",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
    ],
    python_requires=">=3.8",
    entry_points={
        "lms.djangoapp": [
            "edx_stats = edx_stats.apps:EdxStatsConfig",
        ],
    },
)