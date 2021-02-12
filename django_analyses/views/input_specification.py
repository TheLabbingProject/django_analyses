from django_analyses.filters.input.input_specification import \
    InputSpecificationFilter
from django_analyses.models.input.input_specification import InputSpecification
from django_analyses.serializers.input.input_specification import \
    InputSpecificationSerializer
from django_analyses.views.defaults import DefaultsMixin
from django_analyses.views.pagination import StandardResultsSetPagination
from rest_framework import viewsets


class InputSpecificationViewSet(DefaultsMixin, viewsets.ModelViewSet):
    filter_class = InputSpecificationFilter
    pagination_class = StandardResultsSetPagination
    queryset = InputSpecification.objects.order_by("-id").all()
    serializer_class = InputSpecificationSerializer
