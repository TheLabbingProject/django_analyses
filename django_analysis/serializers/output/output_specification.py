from django_analysis.models.analysis import Analysis
from django_analysis.models.output.output_specification import OutputSpecification
from django_analysis.serializers.output.definitions.output_definition import (
    OutputDefinitionSerializer,
)
from rest_framework import serializers


class OutputSpecificationSerializer(serializers.HyperlinkedModelSerializer):
    url = serializers.HyperlinkedIdentityField(
        view_name="analysis:outputspecification-detail"
    )
    analysis = serializers.HyperlinkedRelatedField(
        view_name="analysis:analysis-detail", queryset=Analysis.objects.all()
    )
    output_definitions = OutputDefinitionSerializer(many=True)

    class Meta:
        model = OutputSpecification
        fields = (
            "id",
            "analysis",
            "output_definitions",
            "created",
            "modified",
            "url",
        )

