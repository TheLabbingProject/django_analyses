from django_analysis.models.input.input import Input
from django_analysis.models.input.types.input_types import InputTypes
from django_analysis.serializers.input.types.boolean_input import BooleanInputSerializer
from django_analysis.serializers.input.types.file_input import FileInputSerializer
from django_analysis.serializers.input.types.float_input import FloatInputSerializer
from django_analysis.serializers.input.types.integer_input import IntegerInputSerializer
from django_analysis.serializers.input.types.list_input import ListInputSerializer
from django_analysis.serializers.input.types.string_input import StringInputSerializer
from django_analysis.serializers.utils.polymorphic import PolymorphicSerializer
from rest_framework.serializers import Serializer

SERIALIZERS = {
    InputTypes.BLN.value: BooleanInputSerializer,
    InputTypes.FIL.value: FileInputSerializer,
    InputTypes.FLT.value: FloatInputSerializer,
    InputTypes.INT.value: IntegerInputSerializer,
    InputTypes.LST.value: ListInputSerializer,
    InputTypes.STR.value: StringInputSerializer,
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
