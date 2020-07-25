from django_analyses.models.output.types.list_output import ListOutput
from rest_framework import serializers


class ListOutputSerializer(serializers.ModelSerializer):
    class Meta:
        model = ListOutput
        fields = "id", "key", "value", "run", "definition"
