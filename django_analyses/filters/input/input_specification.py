"""
Definition of an :class:`InputSpecificationFilter` for the
:class:`~django_analyses.models.input.input_specification.InputSpecification`
model.
"""

from django_analyses.models.input.input_specification import InputSpecification
from django_filters import rest_framework as filters


class InputSpecificationFilter(filters.FilterSet):
    """
    Provides useful filtering options for the
    :class:`~django_analyses.models.input.input_specification.InputSpecification`
    model.

    """

    class Meta:
        model = InputSpecification
        fields = "id", "analysis"
