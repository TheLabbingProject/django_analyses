from django_analysis.models.input.types.float_input import FloatInput
from rest_framework import serializers


class FloatInputSerializer(serializers.ModelSerializer):
    class Meta:
        model = FloatInput
        fields = "id", "key", "value", "run", "definition"
