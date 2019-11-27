from django_analysis.models.pipeline.node import Node
from django_analysis.serializers.analysis_version import AnalysisVersionSerializer
from rest_framework import serializers


class NodeSerializer(serializers.HyperlinkedModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name="analysis:node-detail")
    analysis_version = AnalysisVersionSerializer()

    class Meta:
        model = Node
        fields = "id", "analysis_version", "configuration", "created", "modified", "url"

