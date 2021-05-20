"""
Definition of an :class:`~django_analyses.filters.input.input.InputFilter`
for the :class:`~django_analyses.models.input.input.Input` model.
"""

from django_analyses.models.input.input import Input
from django_analyses.models.input.types.input_types import InputTypes
from django_filters import rest_framework as filters


class InputFilter(filters.FilterSet):
    """
    Provides useful filtering options for the
    :class:`~django_analyses.models.input.input.Input`
    model.

    """

    key = filters.CharFilter(
        lookup_expr="icontains",
        label="Definition key contains (case-insensitive)",
        method="filter_key",
    )
    input_type = filters.ChoiceFilter(
        choices=InputTypes.choices(), method="filter_input_type", label="Type"
    )

    class Meta:
        model = Input
        fields = "run", "key"

    def filter_key(self, queryset, name, value):
        ids = [
            inpt.id for inpt in queryset.all() if value in inpt.definition.key
        ]
        return queryset.filter(id__in=ids)

    def filter_input_type(self, queryset, name, value):
        ids = [
            inpt.id for inpt in queryset.all() if inpt.get_type().name == value
        ]
        return queryset.filter(id__in=ids)
