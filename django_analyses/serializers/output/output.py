import importlib

from django.conf import settings
from django_analyses.models.output.output import Output
from django_analyses.models.output.types.output_types import OutputTypes
from django_analyses.serializers.output.types.file_output import FileOutputSerializer
from django_analyses.serializers.utils.polymorphic import PolymorphicSerializer
from rest_framework.serializers import Serializer


def get_extra_output_serializers() -> dict:
    extra_serializers_definition = getattr(settings, "EXTRA_OUTPUT_SERIALIZERS", {})
    serializers = {}
    for input_type, definition in extra_serializers_definition.items():
        module_location, class_name = definition
        module = importlib.import_module(module_location)
        serializer = getattr(module, class_name)
        serializers[input_type] = serializer
    return serializers


SERIALIZERS = {
    OutputTypes.FIL.value: FileOutputSerializer,
    **get_extra_output_serializers(),
}


class OutputSerializer(PolymorphicSerializer):
    class Meta:
        model = Output
        fields = "__all__"

    def get_serializer(self, output_type: str) -> Serializer:
        try:
            return SERIALIZERS[output_type]
        except KeyError:
            raise ValueError(f'Serializer for "{output_type}" does not exist')
