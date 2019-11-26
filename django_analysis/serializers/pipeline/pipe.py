from django_analysis.models.input.definitions.input_definition import InputDefinition
from django_analysis.models.output.definitions.output_definition import OutputDefinition
from django_analysis.models.pipeline.node import Node
from django_analysis.models.pipeline.pipe import Pipe
from django_analysis.models.pipeline.pipeline import Pipeline
from rest_framework import serializers


class PipeSerializer(serializers.HyperlinkedModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name="analysis:pipe-detail")
    pipeline = serializers.HyperlinkedRelatedField(
        view_name="analysis:pipeline-detail", queryset=Pipeline.objects.all(),
    )
    source = serializers.HyperlinkedRelatedField(
        view_name="analysis:node-detail", queryset=Node.objects.all()
    )
    source_port = serializers.HyperlinkedRelatedField(
        view_name="analysis:outputdefinition-detail",
        queryset=OutputDefinition.objects.all(),
    )
    destination = serializers.HyperlinkedRelatedField(
        view_name="analysis:node-detail", queryset=Node.objects.all()
    )
    destination_port = serializers.HyperlinkedRelatedField(
        view_name="analysis:inputdefinition-detail",
        queryset=InputDefinition.objects.all(),
    )

    class Meta:
        model = Pipe
        fields = (
            "id",
            "pipeline",
            "source",
            "source_port",
            "destination",
            "destination_port",
            "url",
        )

