from django_analysis.models.analysis_version import AnalysisVersion
from django_analysis.serializers.analysis import AnalysisSerializer
from django_analysis.serializers.input.input_specification import (
    InputSpecificationSerializer,
)
from django_analysis.serializers.output.output_specification import (
    OutputSpecificationSerializer,
)
from rest_framework import serializers


class AnalysisVersionSerializer(serializers.HyperlinkedModelSerializer):
    url = serializers.HyperlinkedIdentityField(
        view_name="analysis:analysisversion-detail"
    )
    analysis = AnalysisSerializer()
    input_specification = InputSpecificationSerializer()
    output_specification = OutputSpecificationSerializer()

    class Meta:
        model = AnalysisVersion
        fields = (
            "id",
            "analysis",
            "title",
            "description",
            "input_specification",
            "output_specification",
            "created",
            "modified",
            "url",
        )

