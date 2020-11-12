from django_analyses.models.analysis import Analysis
from django_analyses.models.input.input_specification import InputSpecification
from rest_framework import serializers


class InputSpecificationSerializer(serializers.HyperlinkedModelSerializer):
    analysis = serializers.HyperlinkedRelatedField(
        view_name="analyses:analysis-detail", queryset=Analysis.objects.all()
    )
    input_definitions_count = serializers.IntegerField(
        source="input_definitions.count", read_only=True
    )

    class Meta:
        model = InputSpecification
        fields = (
            "id",
            "analysis",
            "created",
            "modified",
            "input_definitions_count",
        )
