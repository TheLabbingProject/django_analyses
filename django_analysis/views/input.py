from django_analysis.models.input.input import Input
from django_analysis.serializers.input.input import InputSerializer
from rest_framework import viewsets


class InputViewSet(viewsets.ModelViewSet):
    serializer_class = InputSerializer

    def get_queryset(self):
        return Input.objects.select_subclasses()
