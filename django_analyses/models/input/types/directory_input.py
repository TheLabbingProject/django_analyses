from django.conf import settings
from django.db import models
from django_analyses.models.input.input import Input
from django_analyses.models.input.types.input_types import InputTypes


class DirectoryInput(Input):
    value = models.FilePathField(
        settings.MEDIA_ROOT, max_length=1000, allow_files=False, allow_folders=True
    )
    definition = models.ForeignKey(
        "django_analyses.DirectoryInputDefinition",
        on_delete=models.PROTECT,
        related_name="input_set",
    )

    def get_type(self) -> InputTypes:
        return InputTypes.DIR
