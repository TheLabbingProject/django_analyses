from django_analysis.models.analysis import Analysis
from django_analysis.serializers.analysis import AnalysisSerializer
from rest_framework import viewsets


class AnalysisViewSet(viewsets.ModelViewSet):
    queryset = Analysis.objects.order_by("title").all()
    serializer_class = AnalysisSerializer

