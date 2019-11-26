from django_analysis.models.pipeline.pipeline import Pipeline
from django_filters import rest_framework as filters


class PipelineFilter(filters.FilterSet):
    """
    Provides useful filtering options for the
    :class:`~django_analysis.models.pipeline.pipeline.Pipeline`
    model.
    
    """

    class Meta:
        model = Pipeline
        fields = "title", "description", "created", "modified"
