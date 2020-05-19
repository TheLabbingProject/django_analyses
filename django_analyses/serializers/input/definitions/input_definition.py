import importlib

from django.conf import settings
from django_analyses.models.input.definitions.input_definition import InputDefinition
from django_analyses.models.input.definitions.input_definitions import InputDefinitions
from django_analyses.serializers.input.definitions.string_input_definition import (
    StringInputDefinitionSerializer,
)
from django_analyses.serializers.input.definitions.boolean_input_definition import (
    BooleanInputDefinitionSerializer,
)
from django_analyses.serializers.input.definitions.directory_input_definition import (
    DirectoryInputDefinitionSerializer,
)
from django_analyses.serializers.input.definitions.file_input_definition import (
    FileInputDefinitionSerializer,
)
from django_analyses.serializers.input.definitions.integer_input_definition import (
    IntegerInputDefinitionSerializer,
)
from django_analyses.serializers.input.definitions.float_input_definition import (
    FloatInputDefinitionSerializer,
)
from django_analyses.serializers.input.definitions.list_input_definition import (
    ListInputDefinitionSerializer,
)
from django_analyses.serializers.utils.polymorphic import PolymorphicSerializer
from rest_framework.serializers import Serializer


def get_extra_input_definition_serializers() -> dict:
    extra_serializers_definition = getattr(
        settings, "EXTRA_INPUT_DEFINITION_SERIALIZERS", {}
    )
    serializers = {}
    for input_type, definition in extra_serializers_definition.items():
        module_location, class_name = definition
        module = importlib.import_module(module_location)
        serializer = getattr(module, class_name)
        serializers[input_type] = serializer
    return serializers


SERIALIZERS = {
    InputDefinitions.STR.value: StringInputDefinitionSerializer,
    InputDefinitions.BLN.value: BooleanInputDefinitionSerializer,
    InputDefinitions.DIR.value: DirectoryInputDefinitionSerializer,
    InputDefinitions.FIL.value: FileInputDefinitionSerializer,
    InputDefinitions.INT.value: IntegerInputDefinitionSerializer,
    InputDefinitions.FLT.value: FloatInputDefinitionSerializer,
    InputDefinitions.LST.value: ListInputDefinitionSerializer,
    **get_extra_input_definition_serializers(),
}


class InputDefinitionSerializer(PolymorphicSerializer):
    class Meta:
        model = InputDefinition
        fields = "__all__"

    def get_serializer(self, input_type: str) -> Serializer:
        try:
            return SERIALIZERS[input_type]
        except KeyError:
            raise ValueError(f'Serializer for "{input_type}" does not exist')
