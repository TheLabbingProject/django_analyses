from django_analysis.filters.analysis import AnalysisFilter
from django_analysis.models.analysis import Analysis
from django_analysis.serializers.analysis import AnalysisSerializer
from django_analysis.views.defaults import DefaultsMixin
from django_analysis.views.pagination import StandardResultsSetPagination
from rest_framework import viewsets


class AnalysisViewSet(DefaultsMixin, viewsets.ModelViewSet):
    filter_class = AnalysisFilter
    pagination_class = StandardResultsSetPagination
    queryset = Analysis.objects.all()
    serializer_class = AnalysisSerializer

