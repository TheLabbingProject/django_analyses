from django_analysis.models.input.definitions.input_definition import InputDefinition
from django_analysis.serializers.input.definitions.input_definition import (
    InputDefinitionSerializer,
)
from rest_framework import viewsets


class InputDefinitionViewSet(viewsets.ModelViewSet):
    serializer_class = InputDefinitionSerializer

    def get_queryset(self):
        return InputDefinition.objects.select_subclasses()
