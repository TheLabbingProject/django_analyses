from django.http import JsonResponse
from django_analyses.filters.output.output import OutputFilter
from django_analyses.models.output.output import Output
from django_analyses.serializers.output.output import OutputSerializer
from django_analyses.views.defaults import DefaultsMixin
from django_analyses.views.pagination import StandardResultsSetPagination
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.request import Request
from rest_framework.response import Response


class OutputViewSet(DefaultsMixin, viewsets.ModelViewSet):
    filter_class = OutputFilter
    pagination_class = StandardResultsSetPagination
    serializer_class = OutputSerializer

    def get_queryset(self):
        return Output.objects.select_subclasses()

    @action(detail=True, methods=["GET"])
    def html_repr(self, request: Request, pk: int = None) -> Response:
        instance = Output.objects.get_subclass(id=pk)
        content = "No preview available :("
        if hasattr(instance, "_repr_html_"):
            html_repr = instance._repr_html_()
            if html_repr:
                content = html_repr.get_iframe(width=1000, height=500)
        return JsonResponse({"content": content})
