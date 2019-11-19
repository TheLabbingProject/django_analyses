from django_analysis.models.analysis import Analysis
from rest_framework import serializers


class AnalysisSerializer(serializers.HyperlinkedModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name="analysis:analysis-detail")

    class Meta:
        model = Analysis
        fields = ("id", "title", "description", "created", "modified", "url")

