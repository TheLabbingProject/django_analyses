from django_analysis.filters.input.input import InputFilter
from django_analysis.models.input.input import Input
from django_analysis.serializers.input.input import InputSerializer
from django_analysis.views.defaults import DefaultsMixin
from django_analysis.views.pagination import StandardResultsSetPagination
from rest_framework import viewsets


class InputViewSet(DefaultsMixin, viewsets.ModelViewSet):
    filter_class = InputFilter
    pagination_class = StandardResultsSetPagination
    serializer_class = InputSerializer

    def get_queryset(self):
        return Input.objects.select_subclasses()
