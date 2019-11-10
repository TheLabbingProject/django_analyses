from django.db import models
from django_analysis.analyses import model_to_analysis
from django_extensions.db.models import TitleDescriptionModel, TimeStampedModel
from model_utils.managers import InheritanceManager


class AnalysisVersion(TitleDescriptionModel, TimeStampedModel):
    analysis = models.ForeignKey(
        "django_analysis.Analysis",
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        related_name="analysis_version_set",
    )
    input_specification = models.ForeignKey(
        "django_analysis.InputSpecification",
        on_delete=models.PROTECT,
        blank=True,
        null=True,
        related_name="analysis_version_set",
    )

    objects = InheritanceManager()

    def __str__(self) -> str:
        return f"{self.analysis.title} v{self.title}"

    def get_class(self) -> object:
        return self.definition["class"]

    def run(self, *args, **kwargs):
        raise NotImplementedError

    @property
    def definition(self) -> dict:
        return model_to_analysis[self.analysis.title][self.title]
