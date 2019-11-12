from django.conf import settings
from django.db import models
from django_analysis.models.output.output import Output


class FileOutput(Output):
    value = models.FilePathField(settings.MEDIA_ROOT)
    definition = models.ForeignKey(
        "django_analysis.FileOutputDefinition",
        on_delete=models.PROTECT,
        related_name="output_set",
    )
