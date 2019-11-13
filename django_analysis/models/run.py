from django.db import models
from django_extensions.db.models import TimeStampedModel


class Run(TimeStampedModel):
    analysis_version = models.ForeignKey(
        "django_analysis.AnalysisVersion", on_delete=models.PROTECT
    )

    class Meta:
        ordering = ("-created",)

    def get_input_configuration(self) -> dict:
        input_specification = self.analysis_version.input_specification
        defaults = input_specification.get_default_input_configurations()
        configuration = {
            inpt.definition.key: inpt.value
            for inpt in self.input_set.select_subclasses()
        }
        defaults.update(configuration)
        return defaults

    @property
    def input_configuration(self) -> dict:
        return self.get_input_configuration()
