from django_analysis.models.input.types.list_input import ListInput
from rest_framework import serializers


class ListInputSerializer(serializers.ModelSerializer):
    class Meta:
        model = ListInput
        fields = "id", "key", "value", "run", "definition"
