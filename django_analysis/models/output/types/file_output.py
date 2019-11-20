from django.conf import settings
from django.db import models
from django_analysis.models.output.output import Output
from django_analysis.models.output.types.output_types import OutputTypes


class FileOutput(Output):
    value = models.FilePathField(settings.MEDIA_ROOT, blank=True, null=True)
    definition = models.ForeignKey(
        "django_analysis.FileOutputDefinition",
        on_delete=models.PROTECT,
        related_name="output_set",
    )

    def get_type(self) -> str:
        return OutputTypes.FIL
