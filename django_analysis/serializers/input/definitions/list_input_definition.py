from django_analysis.models.input.definitions.list_input_definition import (
    ListInputDefinition,
)
from rest_framework import serializers


class ListInputDefinitionSerializer(serializers.ModelSerializer):
    class Meta:
        model = ListInputDefinition
        fields = "__all__"

