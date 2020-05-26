[![PyPI version](https://img.shields.io/pypi/v/django-analyses.svg)](https://pypi.python.org/pypi/django-analyses/)
[![PyPI status](https://img.shields.io/pypi/status/django-analyses.svg)](https://pypi.python.org/pypi/django-analyses/)
[![TheLabbingProject](https://circleci.com/gh/TheLabbingProject/django_analyses.svg?style=shield)](https://app.circleci.com/pipelines/github/TheLabbingProject/django-analyses)
[![Documentation Status](https://readthedocs.org/projects/django-analyses/badge/?version=latest)](http://django-analyses.readthedocs.io/?badge=latest)

# django-analyses

A reusable Django app to manage analyses.

## Quick start

1. Add "django_analyses" to your INSTALLED_APPS setting:

<pre>
    INSTALLED_APPS = [
        ...
        'django_analyses',
    ]
</pre>

2. Include the `analyses` URLconf in your prject urls.py:

<pre>
    path("api/", include("django_analyses.urls", namespace="analyses")),
</pre>

3. Run `python manage.py migrate` to create the analyses models.

4. Start the development server and visit http://127.0.0.1:8000/admin/.

5. Visit http://127.0.0.1:8000/api/analyses/.
