from django_analysis.filters.pipeline.node import NodeFilter
from django_analysis.models.pipeline.node import Node
from django_analysis.serializers.pipeline.node import NodeSerializer
from django_analysis.views.defaults import DefaultsMixin
from django_analysis.views.pagination import StandardResultsSetPagination
from rest_framework import viewsets


class NodeViewSet(DefaultsMixin, viewsets.ModelViewSet):
    filter_class = NodeFilter
    pagination_class = StandardResultsSetPagination
    queryset = Node.objects.all()
    serializer_class = NodeSerializer
