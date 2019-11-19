from django_analysis.models.input.input_specification import InputSpecification
from django_analysis.serializers.input.input_specification import (
    InputSpecificationSerializer,
)
from rest_framework import viewsets


class InputSpecificationViewSet(viewsets.ModelViewSet):
    queryset = InputSpecification.objects.order_by("-id").all()
    serializer_class = InputSpecificationSerializer

