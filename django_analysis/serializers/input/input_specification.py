from django_analysis.models.analysis import Analysis
from django_analysis.models.input.input_specification import InputSpecification
from django_analysis.serializers.input.definitions.input_definition import (
    InputDefinitionSerializer,
)
from rest_framework import serializers


class InputSpecificationSerializer(serializers.HyperlinkedModelSerializer):
    url = serializers.HyperlinkedIdentityField(
        view_name="analysis:inputspecification-detail"
    )
    analysis = serializers.HyperlinkedRelatedField(
        view_name="analysis:analysis-detail", queryset=Analysis.objects.all()
    )
    input_definitions = InputDefinitionSerializer(many=True)

    class Meta:
        model = InputSpecification
        fields = "id", "analysis", "url", "input_definitions", "created", "modified"

