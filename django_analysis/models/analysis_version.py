from django.db import models
from django_analysis.models.input_specification import InputSpecification
from django_analysis.models.output_specification import OutputSpecification
from django_extensions.db.models import TitleDescriptionModel, TimeStampedModel


class AnalysisVersion(TitleDescriptionModel, TimeStampedModel):
    analysis = models.ForeignKey(
        "django_analysis.Analysis",
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        related_name="version_set",
    )
    input_specification = models.ForeignKey(
        "django_analysis.InputSpecification",
        on_delete=models.PROTECT,
        blank=True,
        null=True,
        related_name="analysis_version_set",
    )
    output_specification = models.ForeignKey(
        "django_analysis.OutputSpecification",
        on_delete=models.PROTECT,
        blank=True,
        null=True,
        related_name="analysis_version_set",
    )

    def __str__(self) -> str:
        return f"{self.analysis.title} v{self.title}"

    def run(self, *args, **kwargs):
        raise NotImplementedError
