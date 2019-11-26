from django_analysis.models.analysis_version import AnalysisVersion
from django_analysis.models.pipeline.node import Node
from rest_framework import serializers


class NodeSerializer(serializers.HyperlinkedModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name="analysis:node-detail")
    analysis_version = serializers.HyperlinkedRelatedField(
        view_name="analysis:analysisversion-detail",
        queryset=AnalysisVersion.objects.all(),
    )

    class Meta:
        model = Node
        fields = "id", "analysis_version", "configuration", "created", "modified", "url"

