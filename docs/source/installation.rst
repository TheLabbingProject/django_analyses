Installation
============

    1. Install from `PyPi <https://pypi.org/project/django-analyses/>`_:

        .. code-block:: bash

            pip install django_analyses

    2. Add *"django_analyses"* to your project's :obj:`INSTALLED_APPS` setting:

        .. code-block:: python
            :caption: settings.py

            INSTALLED_APPS = [
                ...,
                "django_analyses",
            ]

    3. Include the *analyses* URLconf in your prject *urls.py*:

        .. code-block:: python
            :caption: urls.py

            urlpatterns = [
                ...,
                path("api/", include("django_analyses.urls", namespace="analyses")),
            ]

    4. Run:

        .. code-block:: bash

            python manage.py migrate

    5. Start the development server and visit http://127.0.0.1:8000/admin/.

    6. Visit http://127.0.0.1:8000/api/analyses/.

