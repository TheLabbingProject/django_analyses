"""
Definition of an :class:`OutputSpecificationFilter` for the
:class:`~django_analyses.models.output.output_specification.OutputSpecification`
model.
"""

from django_analyses.models.output.output_specification import (
    OutputSpecification,
)
from django_filters import rest_framework as filters


class OutputSpecificationFilter(filters.FilterSet):
    """
    Provides useful filtering options for the
    :class:`~django_analyses.models.output.output_specification.OutputSpecification`
    model.

    """

    class Meta:
        model = OutputSpecification
        fields = "id", "analysis"
