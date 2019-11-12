from django.db import models
from django_extensions.db.models import TimeStampedModel


class Run(TimeStampedModel):
    analysis_version = models.ForeignKey(
        "django_analysis.AnalysisVersion", on_delete=models.PROTECT
    )

    class Meta:
        ordering = ("-created",)

    def get_input_configuration(self) -> dict:
        return {
            inpt.definition.key: inpt.value
            for inpt in self.input_set.select_subclasses()
        }

    @property
    def input_configuration(self) -> dict:
        return self.get_input_configuration()
