from django.http import JsonResponse
from django_analyses.filters.input.input import InputFilter
from django_analyses.models.input.input import Input
from django_analyses.serializers.input.input import InputSerializer
from django_analyses.views.defaults import DefaultsMixin
from django_analyses.views.pagination import StandardResultsSetPagination
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.request import Request
from rest_framework.response import Response


class InputViewSet(DefaultsMixin, viewsets.ModelViewSet):
    filter_class = InputFilter
    pagination_class = StandardResultsSetPagination
    serializer_class = InputSerializer

    def get_queryset(self):
        return Input.objects.select_subclasses()

    @action(detail=True, methods=["GET"])
    def html_repr(
        self, request: Request, input_id: int = None, index: int = None
    ) -> Response:
        instance = Input.objects.get_subclass(id=input_id)
        content = "No preview available :("
        html_repr = False
        has_repr = hasattr(instance, "_repr_html_")
        has_getter = hasattr(instance, "get_html_repr")
        if index is None and has_repr:
            html_repr = instance._repr_html_()
        elif index is not None and has_getter:
            html_repr = instance.get_html_repr(index)
        content = html_repr if html_repr else content
        return JsonResponse({"content": content})
