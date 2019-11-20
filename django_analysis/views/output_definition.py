from django_analysis.models.output.definitions.output_definition import OutputDefinition
from django_analysis.serializers.output.definitions.output_definition import (
    OutputDefinitionSerializer,
)
from rest_framework import viewsets


class OutputDefinitionViewSet(viewsets.ModelViewSet):
    serializer_class = OutputDefinitionSerializer

    def get_queryset(self):
        return OutputDefinition.objects.select_subclasses()
