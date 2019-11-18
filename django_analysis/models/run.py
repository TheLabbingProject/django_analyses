from django.db import models
from django_analysis.models.input.input import Input
from django_analysis.models.managers.run import RunManager
from django_extensions.db.models import TimeStampedModel


class Run(TimeStampedModel):
    analysis_version = models.ForeignKey(
        "django_analysis.AnalysisVersion", on_delete=models.PROTECT
    )

    objects = RunManager()

    class Meta:
        ordering = ("-created",)

    def get_input_configuration(self) -> dict:
        configuration = {
            inpt.definition.key: inpt.value
            for inpt in self.input_set.select_subclasses()
        }
        defaults = self.input_defaults.copy()
        defaults.update(configuration)
        return defaults

    def create_input_instance(self, key: str, value) -> Input:
        input_definition = self.analysis_version.input_definitions.get(key=key)
        return input_definition.create_input_instance(value=value, run=self)

    def create_output_instance(self, key: str, value) -> Input:
        output_definition = self.analysis_version.output_definitions.get(key=key)
        return output_definition.create_output_instance(value=value, run=self)

    def create_input_instances(self, **kwargs) -> list:
        return [self.create_input_instance(key, value) for key, value in kwargs.items()]

    def create_output_instances(self, **results) -> list:
        return [
            self.create_output_instance(key, value) for key, value in results.items()
        ]

    def get_input_set(self) -> models.QuerySet:
        return self.base_input_set.select_subclasses()

    def get_output_set(self) -> models.QuerySet:
        return self.base_output_set.select_subclasses()

    @property
    def input_defaults(self) -> dict:
        return self.analysis_version.input_specification.default_configuration

    @property
    def input_configuration(self) -> dict:
        return self.get_input_configuration()

    @property
    def input_set(self) -> models.QuerySet:
        return self.get_input_set()

    @property
    def output_set(self) -> models.QuerySet:
        return self.get_output_set()
