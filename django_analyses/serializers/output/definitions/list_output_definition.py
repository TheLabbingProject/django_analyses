from django_analyses.models.output.definitions.list_output_definition import \
    ListOutputDefinition
from rest_framework import serializers


class ListOutputDefinitionSerializer(serializers.ModelSerializer):
    class Meta:
        model = ListOutputDefinition
        fields = "__all__"
