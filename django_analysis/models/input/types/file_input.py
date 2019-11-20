from django.conf import settings
from django.db import models
from django_analysis.models.input.input import Input
from django_analysis.models.input.types.input_types import InputTypes


class FileInput(Input):
    value = models.FilePathField(settings.MEDIA_ROOT)
    definition = models.ForeignKey(
        "django_analysis.FileInputDefinition",
        on_delete=models.PROTECT,
        related_name="input_set",
    )

    def get_type(self) -> InputTypes:
        return InputTypes.FIL
