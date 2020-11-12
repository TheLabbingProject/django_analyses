from django_analyses.filters.output.output_specification import (
    OutputSpecificationFilter,
)
from django_analyses.models.output.output_specification import (
    OutputSpecification,
)
from django_analyses.serializers.output.output_specification import (
    OutputSpecificationSerializer,
)
from django_analyses.views.defaults import DefaultsMixin
from django_analyses.views.pagination import StandardResultsSetPagination
from rest_framework import viewsets


class OutputSpecificationViewSet(DefaultsMixin, viewsets.ModelViewSet):
    filter_class = OutputSpecificationFilter
    pagination_class = StandardResultsSetPagination
    queryset = OutputSpecification.objects.order_by("-id").all()
    serializer_class = OutputSpecificationSerializer

