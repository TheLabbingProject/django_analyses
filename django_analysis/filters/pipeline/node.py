from django_analysis.models.pipeline.node import Node
from django_filters import rest_framework as filters


class NodeFilter(filters.FilterSet):
    """
    Provides useful filtering options for the
    :class:`~django_analysis.models.pipeline.node.Node`
    model.
    
    """

    class Meta:
        model = Node
        fields = ("analysis_version",)

