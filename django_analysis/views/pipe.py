from django_analysis.filters.pipeline.pipe import PipeFilter
from django_analysis.models.pipeline.pipe import Pipe
from django_analysis.serializers.pipeline.pipe import PipeSerializer
from django_analysis.views.defaults import DefaultsMixin
from django_analysis.views.pagination import StandardResultsSetPagination
from rest_framework import viewsets


class PipeViewSet(DefaultsMixin, viewsets.ModelViewSet):
    queryset = Pipe.objects.all()
    filter_class = PipeFilter
    pagination_class = StandardResultsSetPagination
    serializer_class = PipeSerializer
