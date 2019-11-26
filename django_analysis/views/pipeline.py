from django_analysis.filters.pipeline.pipeline import PipelineFilter
from django_analysis.models.pipeline.pipeline import Pipeline
from django_analysis.serializers.pipeline.pipeline import PipelineSerializer
from django_analysis.views.defaults import DefaultsMixin
from django_analysis.views.pagination import StandardResultsSetPagination
from rest_framework import viewsets


class PipelineViewSet(DefaultsMixin, viewsets.ModelViewSet):
    queryset = Pipeline.objects.all()
    filter_class = PipelineFilter
    pagination_class = StandardResultsSetPagination
    serializer_class = PipelineSerializer
