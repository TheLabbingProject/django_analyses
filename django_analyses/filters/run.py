"""
Definition of a :class:`RunFilter` class for the
:class:`~django_analyses.models.run.Run` model.
"""
from django.db.models import QuerySet
from django_analyses.models.analysis import Analysis
from django_analyses.models.analysis_version import AnalysisVersion
from django_analyses.models.run import Run
from django_analyses.models.utils import get_subject_model
from django_analyses.models.utils.run_status import RunStatus
from django_filters import rest_framework as filters

ANALYSES_WITH_RUNS = Analysis.objects.filter(
    version_set__run__isnull=False
).distinct()
ANALYSIS_VERSIONS_WITH_RUNS = AnalysisVersion.objects.filter(
    run__isnull=False
).distinct()
Subject = get_subject_model()


class RunFilter(filters.FilterSet):
    """
    Provides useful filtering options for the
    :class:`~django_analyses.models.run.Run` model.
    """

    analysis = filters.ModelMultipleChoiceFilter(
        "analysis_version__analysis", queryset=ANALYSES_WITH_RUNS,
    )
    analysis_version = filters.ModelMultipleChoiceFilter(
        "analysis_version", queryset=ANALYSIS_VERSIONS_WITH_RUNS
    )
    status = filters.MultipleChoiceFilter(choices=RunStatus.choices())
    start_time = filters.DateTimeFromToRangeFilter()
    end_time = filters.DateTimeFromToRangeFilter()
    if Subject:
        subject = filters.NumberFilter(
            method="get_subject_runs", label="By subject ID:", required=False
        )

    class Meta:
        model = Run
        fields = ("id",)

    def get_subject_runs(
        self, queryset: QuerySet, name: str, pk: int
    ) -> QuerySet:
        try:
            subject = Subject.objects.get(id=pk)
        except Subject.DoesNotExist:
            pass
        else:
            return subject.query_run_set()
