from django_analysis.models.output.output import Output
from django_analysis.serializers.output.output import OutputSerializer
from rest_framework import viewsets


class OutputViewSet(viewsets.ModelViewSet):
    serializer_class = OutputSerializer

    def get_queryset(self):
        return Output.objects.select_subclasses()
