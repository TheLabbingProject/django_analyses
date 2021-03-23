from django.http import FileResponse, JsonResponse
from django_analyses.filters.output.output import OutputFilter
from django_analyses.models.output.output import Output
from django_analyses.models.output.types.output_types import OutputTypes
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
            content = html_repr if html_repr else content
        return JsonResponse({"content": content})

    @action(detail=True, methods=["GET"])
    def download(self, request: Request, pk: int = None) -> Response:
        instance = Output.objects.get_subclass(id=pk)
        if instance.get_type() == OutputTypes.FIL:
            return FileResponse(open(instance.value, "rb"), as_attachment=True)

