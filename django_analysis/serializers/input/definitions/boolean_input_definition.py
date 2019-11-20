from django_analysis.models.input.definitions.boolean_input_definition import (
    BooleanInputDefinition,
)
from rest_framework import serializers


class BooleanInputDefinitionSerializer(serializers.ModelSerializer):
    class Meta:
        model = BooleanInputDefinition
        fields = "__all__"
