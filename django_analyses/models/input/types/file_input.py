from pathlib import Path

from django.db import models
from django_analyses.models.input.input import Input
from django_analyses.models.input.types.input_types import InputTypes
from django_analyses.models.utils.html_repr import html_repr


class FileInput(Input):
    value = models.FilePathField(max_length=1000)
    definition = models.ForeignKey(
        "django_analyses.FileInputDefinition",
        on_delete=models.PROTECT,
        related_name="input_set",
    )

    def get_type(self) -> InputTypes:
        return InputTypes.FIL

    def _repr_html_(self) -> str:
        return html_repr(Path(self.value))
