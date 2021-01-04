"""
Definition of an :class:`AnalysisVersionFilter` for the
:class:`~django_analyses.models.analysis_version.AnalysisVersion` model.
"""

from django_analyses.models.analysis_version import AnalysisVersion
from django_filters import rest_framework as filters


class AnalysisVersionFilter(filters.FilterSet):
    """
    Provides useful filtering options for the
    :class:`~django_analyses.models.analysis_version.AnalysisVersion` model.

    """

    title = filters.LookupChoiceFilter(
        lookup_choices=[
            ("contains", "Contains (case-sensitive)"),
            ("icontains", "Contains (case-insensitive)"),
            ("exact", "Exact"),
        ]
    )
    description = filters.LookupChoiceFilter(
        lookup_choices=[
            ("contains", "Contains (case-sensitive)"),
            ("icontains", "Contains (case-insensitive)"),
            ("exact", "Exact"),
        ]
    )
    created = filters.DateTimeFromToRangeFilter("created")

    class Meta:
        model = AnalysisVersion
        fields = "id", "analysis", "title", "description", "created"
