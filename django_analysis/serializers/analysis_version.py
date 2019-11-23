from django_analysis.models.analysis import Analysis
from django_analysis.models.analysis_version import AnalysisVersion
from django_analysis.models.input.input_specification import InputSpecification
from rest_framework import serializers


class AnalysisVersionSerializer(serializers.HyperlinkedModelSerializer):
    url = serializers.HyperlinkedIdentityField(
        view_name="analysis:analysisversion-detail"
    )
    analysis = serializers.HyperlinkedRelatedField(
        view_name="analysis:analysis-detail", queryset=Analysis.objects.all()
    )
    input_specification = serializers.HyperlinkedRelatedField(
        view_name="analysis:inputspecification-detail",
        queryset=InputSpecification.objects.all(),
    )

    class Meta:
        model = AnalysisVersion
        fields = (
            "id",
            "analysis",
            "title",
            "description",
            "input_specification",
            "created",
            "modified",
            "url",
        )

