from django_analysis.filters.output.output_definition import OutputDefinitionFilter
from django_analysis.models.output.definitions.output_definition import OutputDefinition
from django_analysis.serializers.output.definitions.output_definition import (
    OutputDefinitionSerializer,
)
from django_analysis.views.defaults import DefaultsMixin
from django_analysis.views.pagination import StandardResultsSetPagination
from rest_framework import viewsets


class OutputDefinitionViewSet(DefaultsMixin, viewsets.ModelViewSet):
    filter_class = OutputDefinitionFilter
    pagination_class = StandardResultsSetPagination
    serializer_class = OutputDefinitionSerializer

    def get_queryset(self):
        return OutputDefinition.objects.select_subclasses()
