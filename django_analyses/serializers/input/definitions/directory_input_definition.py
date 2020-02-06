from django_analyses.models.input.definitions.directory_input_definition import (
    DirectoryInputDefinition,
)
from rest_framework import serializers


class DirectoryInputDefinitionSerializer(serializers.ModelSerializer):
    class Meta:
        model = DirectoryInputDefinition
        fields = "__all__"
