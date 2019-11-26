from django_analysis.models.pipeline.pipe import Pipe
from django_filters import rest_framework as filters


class PipeFilter(filters.FilterSet):
    """
    Provides useful filtering options for the
    :class:`~django_analysis.models.pipeline.pipe.Pipe`
    model.
    
    """

    class Meta:
        model = Pipe
        fields = (
            "pipeline",
            "source",
            "source_port",
            "destination",
            "destination_port",
        )

