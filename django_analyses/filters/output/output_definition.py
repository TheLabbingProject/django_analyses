"""
Definition of an
:class:`~django_analyses.filters.output.output_definition.OutputDefinitionFilter`
for the :class:`~django_analyses.models.output.definitions.OutputDefinition`
model.
"""

from django_analyses.models.output.definitions.output_definition import \
    OutputDefinition
from django_filters import rest_framework as filters


class OutputDefinitionFilter(filters.FilterSet):
    """
    Provides useful filtering options for the
    :class:`~django_analyses.models.output.definitions.output_definition.OutputDefinition`
    model.

    """

    output_specification = filters.AllValuesFilter("specification_set")

    class Meta:
        model = OutputDefinition
        fields = "key", "output_specification"
