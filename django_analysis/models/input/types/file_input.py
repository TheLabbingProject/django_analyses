from django.conf import settings
from django.db import models
from django_analysis.models.input.input import Input


class FileInput(Input):
    definition = models.ForeignKey(
        "django_analysis.FileInputDefinition", on_delete=models.PROTECT
    )
    path = models.FilePathField(settings.MEDIA_ROOT)
