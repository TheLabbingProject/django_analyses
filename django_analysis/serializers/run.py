from django_analysis.models.analysis_version import AnalysisVersion
from django_analysis.models.run import Run
from django_analysis.serializers.input.input import InputSerializer
from django_analysis.serializers.output.output import OutputSerializer
from rest_framework import serializers


class RunSerializer(serializers.HyperlinkedModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name="analysis:run-detail")
    analysis_version = serializers.HyperlinkedRelatedField(
        view_name="analysis:analysisversion-detail",
        queryset=AnalysisVersion.objects.all(),
    )
    input_set = InputSerializer(many=True)
    output_set = OutputSerializer(many=True)

    class Meta:
        model = Run
        fields = (
            "id",
            "analysis_version",
            "input_set",
            "output_set",
            "created",
            "modified",
            "url",
        )

