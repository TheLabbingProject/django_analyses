"""
Definition of an :class:`AnalysisVersionFilter` for the
:class:`~django_analyses.models.analysis_version.AnalysisVersion` model.
"""
from django_analyses.filters.utils import DEFAULT_LOOKUP_CHOICES
from django_analyses.models.analysis import Analysis
from django_analyses.models.analysis_version import AnalysisVersion
from django_filters import rest_framework as filters


class AnalysisVersionFilter(filters.FilterSet):
    """
    Provides useful filtering options for the
    :class:`~django_analyses.models.analysis_version.AnalysisVersion` model.
    """

    analysis = filters.ModelMultipleChoiceFilter(
        queryset=Analysis.objects.all()
    )
    title = filters.LookupChoiceFilter(lookup_choices=DEFAULT_LOOKUP_CHOICES)
    description = filters.LookupChoiceFilter(
        lookup_choices=DEFAULT_LOOKUP_CHOICES
    )
    created = filters.DateTimeFromToRangeFilter("created")
    has_runs = filters.BooleanFilter(
        field_name="run__isnull",
        method="filter_has_runs",
        label="Has existing runs:",
    )

    class Meta:
        model = AnalysisVersion
        fields = "id", "analysis", "title", "description", "created"

    def filter_has_runs(self, queryset, name, value):
        return queryset.filter(**{name: not value}).distinct()
