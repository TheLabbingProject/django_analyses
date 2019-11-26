from django_analysis.models.pipeline.pipeline import Pipeline
from rest_framework import serializers


class PipelineSerializer(serializers.HyperlinkedModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name="analysis:pipe-detail")

    class Meta:
        model = Pipeline
        fields = "id", "title", "description", "created", "modified", "url"

