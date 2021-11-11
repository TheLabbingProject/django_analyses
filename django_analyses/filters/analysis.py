"""
Definition of an :class:`AnalysisFilter` for the
:class:`~django_analyses.models.analysis.Analysis` model.
"""
from django_analyses.filters.utils import DEFAULT_LOOKUP_CHOICES
from django_analyses.models.analysis import Analysis
from django_filters import rest_framework as filters


class AnalysisFilter(filters.FilterSet):
    """
    Provides useful filtering options for the
    :class:`~django_analyses.models.analysis.Analysis` model.
    """

    title = filters.LookupChoiceFilter(lookup_choices=DEFAULT_LOOKUP_CHOICES)
    description = filters.LookupChoiceFilter(
        lookup_choices=DEFAULT_LOOKUP_CHOICES
    )
    created = filters.DateTimeFromToRangeFilter()

    class Meta:
        model = Analysis
        fields = "id", "category"
