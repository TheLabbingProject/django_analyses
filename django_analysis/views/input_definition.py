from django_analysis.views.defaults import DefaultsMixin
from django_analysis.filters.input.input_definition import InputDefinitionFilter
from django_analysis.models.input.definitions.input_definition import InputDefinition
from django_analysis.serializers.input.definitions.input_definition import (
    InputDefinitionSerializer,
)
from django_analysis.views.pagination import StandardResultsSetPagination
from rest_framework import viewsets


class InputDefinitionViewSet(DefaultsMixin, viewsets.ModelViewSet):
    filter_class = InputDefinitionFilter
    serializer_class = InputDefinitionSerializer
    pagination_class = StandardResultsSetPagination

    def get_queryset(self):
        return InputDefinition.objects.select_subclasses()
