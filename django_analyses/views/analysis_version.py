from django_analyses.filters.analysis_version import AnalysisVersionFilter
from django_analyses.models.analysis_version import AnalysisVersion
from django_analyses.serializers.analysis_version import \
    AnalysisVersionSerializer
from django_analyses.views.defaults import DefaultsMixin
from django_analyses.views.pagination import StandardResultsSetPagination
from rest_framework import viewsets


class AnalysisVersionViewSet(DefaultsMixin, viewsets.ModelViewSet):
    filter_class = AnalysisVersionFilter
    pagination_class = StandardResultsSetPagination
    queryset = AnalysisVersion.objects.order_by("title").all()
    serializer_class = AnalysisVersionSerializer
