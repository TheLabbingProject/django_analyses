from django_analysis.models.analysis import Analysis
from django_analysis.models.output.output_specification import OutputSpecification
from rest_framework import serializers


class OutputSpecificationSerializer(serializers.HyperlinkedModelSerializer):
    url = serializers.HyperlinkedIdentityField(
        view_name="analysis:outputspecification-detail"
    )
    analysis = serializers.HyperlinkedRelatedField(
        view_name="analysis:analysis-detail", queryset=Analysis.objects.all()
    )

    class Meta:
        model = OutputSpecification
        fields = "id", "analysis", "url", "created", "modified"

