from django.db import models
from django_extensions.db.models import TimeStampedModel


class Run(TimeStampedModel):
    analysis = models.ForeignKey("django_analysis.Analysis", on_delete=models.CASCADE)

