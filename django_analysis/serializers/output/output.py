from django_analysis.models.output.output import Output
from django_analysis.models.output.types.output_types import OutputTypes
from django_analysis.serializers.output.types.file_output import FileOutputSerializer
from django_analysis.serializers.utils.polymorphic import PolymorphicSerializer
from rest_framework.serializers import Serializer

SERIALIZERS = {OutputTypes.FIL.value: FileOutputSerializer}


class OutputSerializer(PolymorphicSerializer):
    class Meta:
        model = Output
        fields = "__all__"

    def get_serializer(self, output_type: str) -> Serializer:
        try:
            return SERIALIZERS[output_type]
        except KeyError:
            raise ValueError(f'Serializer for "{output_type}" does not exist')
