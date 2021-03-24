import io
import zipfile
from pathlib import Path

from django.http import FileResponse, HttpResponse, JsonResponse
from django.views.decorators.clickjacking import xframe_options_sameorigin
from django_analyses.filters.output.output import OutputFilter
from django_analyses.models.output.output import Output
from django_analyses.models.output.types.file_output import FileOutput
from django_analyses.models.output.types.list_output import ListOutput
from django_analyses.serializers.output.output import OutputSerializer
from django_analyses.views.defaults import DefaultsMixin
from django_analyses.views.pagination import StandardResultsSetPagination
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.request import Request
from rest_framework.response import Response

CONTENT_DISPOSITION = "attachment; filename={name}.zip"
ZIP_CONTENT_TYPE = "application/x-zip-compressed"


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
    @xframe_options_sameorigin
    def download(self, request: Request, pk: int = None) -> Response:
        instance = Output.objects.get_subclass(id=pk)
        is_file_list = (
            isinstance(instance, ListOutput)
            and instance.definition.element_type == "FIL"
        )
        if isinstance(instance, FileOutput):
            file_object = open(instance.value, "rb")
            return FileResponse(file_object, as_attachment=True)
        elif is_file_list:
            buffer = io.BytesIO()
            with zipfile.ZipFile(buffer, "w") as zip_file:
                for path in instance.value:
                    zip_file.write(path, Path(path).name)
            response = HttpResponse(
                buffer.getvalue(), content_type=ZIP_CONTENT_TYPE
            )
            content_disposition = CONTENT_DISPOSITION.format(
                name=instance.definition.key
            )
            response["Content-Disposition"] = content_disposition
            return response
