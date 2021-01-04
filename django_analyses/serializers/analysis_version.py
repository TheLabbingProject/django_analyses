from django_analyses.models.analysis_version import AnalysisVersion
from django_analyses.models.input.input_specification import InputSpecification
from django_analyses.serializers.analysis import AnalysisSerializer
from django_analyses.serializers.output.output_specification import (
    OutputSpecification,
)
from rest_framework import serializers


class AnalysisVersionSerializer(serializers.HyperlinkedModelSerializer):
    analysis = AnalysisSerializer()
    input_specification = serializers.PrimaryKeyRelatedField(
        queryset=InputSpecification.objects.all()
    )
    output_specification = serializers.PrimaryKeyRelatedField(
        queryset=OutputSpecification.objects.all()
    )

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
        )
