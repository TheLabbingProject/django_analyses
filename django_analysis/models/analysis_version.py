from django.db import models
from django_extensions.db.models import TitleDescriptionModel, TimeStampedModel
from model_utils.managers import InheritanceManager


class AnalysisVersion(TitleDescriptionModel, TimeStampedModel):
    analysis = models.ForeignKey(
        "django_analysis.Analysis", on_delete=models.CASCADE, blank=True, null=True
    )
    input_specification = models.ForeignKey(
        "django_analysis.InputSpecification",
        on_delete=models.CASCADE,
        blank=True,
        null=True,
    )

    objects = InheritanceManager()

    def run(self, *args, **kwargs):
        raise NotImplementedError
