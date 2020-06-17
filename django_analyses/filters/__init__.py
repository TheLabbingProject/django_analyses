"""
Filters for the app's :ref:`models <modules/django_analyses.models:Models>`.

References
----------

    * `Django REST Framework`_ `filtering documentation`_.
    * django-filter_'s documentation for `Integration with DRF`_.

.. _django-filter: https://django-filter.readthedocs.io/en/stable/index.html
.. _Django REST Framework: https://www.django-rest-framework.org/
.. _filtering documentation:
   https://www.django-rest-framework.org/api-guide/filtering/
.. _Integration with DRF:
   https://django-filter.readthedocs.io/en/stable/guide/rest_framework.html
"""

from django_analyses.filters.analysis import AnalysisFilter
from django_analyses.filters.category import CategoryFilter
from django_analyses.filters.input import InputDefinitionFilter, InputFilter
from django_analyses.filters.output import OutputDefinitionFilter, OutputFilter
from django_analyses.filters.pipeline import (
    NodeFilter,
    PipeFilter,
    PipelineFilter,
)
