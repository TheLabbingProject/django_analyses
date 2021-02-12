from django_analyses.models.analysis import Analysis
from django_analyses.models.output.output_specification import \
    OutputSpecification
from rest_framework import serializers


class OutputSpecificationSerializer(serializers.HyperlinkedModelSerializer):
    analysis = serializers.HyperlinkedRelatedField(
        view_name="analyses:analysis-detail", queryset=Analysis.objects.all()
    )
    output_definitions_count = serializers.IntegerField(
        source="output_definitions.count", read_only=True
    )

    class Meta:
        model = OutputSpecification
        fields = (
            "id",
            "analysis",
            "created",
            "modified",
            "output_definitions_count",
        )
