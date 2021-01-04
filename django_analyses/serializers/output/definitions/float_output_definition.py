from django_analyses.models.output.definitions.float_output_definition import (
    FloatOutputDefinition,
)
from rest_framework import serializers


class FloatOutputDefinitionSerializer(serializers.ModelSerializer):
    class Meta:
        model = FloatOutputDefinition
        fields = "__all__"
