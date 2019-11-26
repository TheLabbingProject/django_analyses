from django_analysis.filters.output.output import OutputFilter
from django_analysis.models.output.output import Output
from django_analysis.serializers.output.output import OutputSerializer
from django_analysis.views.defaults import DefaultsMixin
from django_analysis.views.pagination import StandardResultsSetPagination
from rest_framework import viewsets


class OutputViewSet(DefaultsMixin, viewsets.ModelViewSet):
    filter_class = OutputFilter
    pagination_class = StandardResultsSetPagination
    serializer_class = OutputSerializer

    def get_queryset(self):
        return Output.objects.select_subclasses()
