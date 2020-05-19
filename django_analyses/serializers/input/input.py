
import importlib

from django_analyses.models.input.input import Input
from django_analyses.models.input.types.input_types import InputTypes
from django_analyses.serializers.input.types.boolean_input import BooleanInputSerializer
from django_analyses.serializers.input.types.directory_input import (
    DirectoryInputSerializer,
)
from django_analyses.serializers.input.types.file_input import FileInputSerializer
from django_analyses.serializers.input.types.float_input import FloatInputSerializer
from django_analyses.serializers.input.types.integer_input import IntegerInputSerializer
from django_analyses.serializers.input.types.list_input import ListInputSerializer
from django.conf import settings
from django_analyses.serializers.input.types.string_input import StringInputSerializer
from django_analyses.serializers.utils.polymorphic import PolymorphicSerializer
from rest_framework.serializers import Serializer


def get_extra_input_serializers() -> dict:
    extra_serializers_definition = getattr(settings, 'EXTRA_INPUT_SERIALIZERS', {})
    serializers = {}
    for input_type, definition in extra_serializers_definition.items():
        module_location, class_name = definition
        module = importlib.import_module(module_location)
        serializer = getattr(module, class_name)
        serializers[input_type] = serializer
    return serializers


SERIALIZERS = {
    InputTypes.BLN.value: BooleanInputSerializer,
    InputTypes.DIR.value: DirectoryInputSerializer,
    InputTypes.FIL.value: FileInputSerializer,
    InputTypes.FLT.value: FloatInputSerializer,
    InputTypes.INT.value: IntegerInputSerializer,
    InputTypes.LST.value: ListInputSerializer,
    InputTypes.STR.value: StringInputSerializer,
    **get_extra_input_serializers(),
}


class InputSerializer(PolymorphicSerializer):
    class Meta:
        model = Input
        fields = "__all__"

    def get_serializer(self, input_type: str) -> Serializer:
        try:
            return SERIALIZERS[input_type]
        except KeyError:
            raise ValueError(f'Serializer for "{input_type}" does not exist')