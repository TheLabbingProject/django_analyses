"""
Definition of an :class:`~django_analyses.filters.output.output.OutputFilter`
for the :class:`~django_analyses.models.output.output.Output` model.
"""

from django_analyses.models.output.output import Output
from django_analyses.models.output.types.output_types import OutputTypes
from django_filters import rest_framework as filters


class OutputFilter(filters.FilterSet):
    """
    Provides useful filtering options for the
    :class:`~django_analyses.models.output.output.Output`
    model.

    """

    key = filters.CharFilter(
        lookup_expr="icontains",
        label="Definition key contains (case-insensitive)",
        method="filter_key",
    )
    output_type = filters.ChoiceFilter(
        choices=OutputTypes.choices(),
        method="filter_output_type",
        label="Type",
    )

    class Meta:
        model = Output
        fields = "run", "key"

    def filter_key(self, queryset, name, value):
        ids = [
            output.id
            for output in queryset.all()
            if value in output.definition.key
        ]
        return queryset.filter(id__in=ids)

    def filter_output_type(self, queryset, name, value):
        ids = [
            output.id
            for output in queryset.all()
            if output.get_type().name == value
        ]
        return queryset.filter(id__in=ids)
