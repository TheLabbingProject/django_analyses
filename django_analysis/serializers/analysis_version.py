from django_analysis.models.analysis_version import AnalysisVersion
from django_analysis.models.input.input_specification import InputSpecification
from rest_framework import serializers


class AnalysisVersionSerializer(serializers.HyperlinkedModelSerializer):
    url = serializers.HyperlinkedIdentityField(
        view_name="analysis:analysisversion-detail"
    )
    input_specification = serializers.HyperlinkedRelatedField(
        view_name="analysis:inputspecification-detail",
        queryset=InputSpecification.objects.all(),
    )

    class Meta:
        model = AnalysisVersion
        fields = (
            "id",
            "title",
            "description",
            "input_specification",
            "created",
            "modified",
            "url",
        )

