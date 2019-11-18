from django.db import models
from django_analysis.models.managers.input_specification import (
    InputSpecificationManager,
)


class InputSpecification(models.Model):
    analysis = models.ForeignKey("django_analysis.Analysis", on_delete=models.CASCADE)
    base_input_definitions = models.ManyToManyField("django_analysis.InputDefinition")

    objects = InputSpecificationManager()

    def __str__(self) -> str:
        formatted_definitions = "\n\t".join(
            [str(definition) for definition in self.input_definitions]
        )
        return f"\n[{self.analysis}]\n\t{formatted_definitions}\n"

    def get_default_input_configurations(self) -> dict:
        return {
            definition.key: definition.default
            for definition in self.input_definitions
            if definition.default is not None
        }

    @property
    def default_configuration(self) -> dict:
        return self.get_default_input_configurations()

    @property
    def input_definitions(self) -> models.QuerySet:
        return self.base_input_definitions.select_subclasses()
