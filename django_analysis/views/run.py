from django_analysis.models.run import Run
from django_analysis.serializers.run import RunSerializer
from rest_framework import viewsets


class RunViewSet(viewsets.ModelViewSet):
    queryset = Run.objects.all()
    serializer_class = RunSerializer

