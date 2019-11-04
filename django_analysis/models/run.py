from django.db import models
from django_extensions.db.models import TimeStampedModel


class Run(TimeStampedModel):
    analysis_version = models.ForeignKey(
        "django_analysis.AnalysisVersion", on_delete=models.PROTECT
    )

