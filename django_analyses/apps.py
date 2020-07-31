"""
Definition of the :class:`DjangoAnalysesConfig` class.

References
----------
* `Django applications`_

.. _Django applications:
   https://docs.djangoproject.com/en/3.0/ref/applications/#module-django.apps
"""

from django.apps import AppConfig


class DjangoAnalysesConfig(AppConfig):
    """
    *django_analyses* app configuration.

    References
    ----------
    * `AppConfig attributes`_

    .. _AppConfig attributes:
       https://docs.djangoproject.com/en/3.0/ref/applications/#configurable-attributes
    """

    #: Full Python path to the application.
    name = "django_analyses"
