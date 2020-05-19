import importlib

from django.conf import settings
from django_analyses.models.output.definitions.output_definition import OutputDefinition
from django_analyses.models.output.definitions.output_definitions import (
    OutputDefinitions,
)
from django_analyses.serializers.output.definitions.file_output_definition import (
    FileOutputDefinitionSerializer,
)
from django_analyses.serializers.utils.polymorphic import PolymorphicSerializer
from rest_framework.serializers import Serializer


def get_extra_output_definition_serializers() -> dict:
    extra_serializers_definition = getattr(
        settings, "EXTRA_OUTPUT_DEFINITION_SERIALIZERS", {}
    )
    serializers = {}
    for input_type, definition in extra_serializers_definition.items():
        module_location, class_name = definition
        module = importlib.import_module(module_location)
        serializer = getattr(module, class_name)
        serializers[input_type] = serializer
    return serializers


SERIALIZERS = {
    OutputDefinitions.FIL.value: FileOutputDefinitionSerializer,
    **get_extra_output_definition_serializers(),
}


class OutputDefinitionSerializer(PolymorphicSerializer):
    class Meta:
        model = OutputDefinition
        fields = "__all__"

    def get_serializer(self, output_type: str) -> Serializer:
        try:
            return SERIALIZERS[output_type]
        except KeyError:
            raise ValueError(f'Serializer for "{output_type}" does not exist')
