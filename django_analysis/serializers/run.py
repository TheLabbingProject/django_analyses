from django_analysis.models.analysis_version import AnalysisVersion
from django_analysis.models.run import Run
from rest_framework import serializers


class RunSerializer(serializers.HyperlinkedModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name="analysis:run-detail")
    analysis_version = serializers.HyperlinkedRelatedField(
        view_name="analysis:analysisversion-detail",
        queryset=AnalysisVersion.objects.all(),
    )

    class Meta:
        model = Run
        fields = ("id", "analysis_version", "created", "modified", "url")

