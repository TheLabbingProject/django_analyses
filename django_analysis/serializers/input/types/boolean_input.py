from django_analysis.models.input.types.boolean_input import BooleanInput
from rest_framework import serializers


class BooleanInputSerializer(serializers.ModelSerializer):
    class Meta:
        model = BooleanInput
        fields = "id", "key", "value", "run", "definition"
