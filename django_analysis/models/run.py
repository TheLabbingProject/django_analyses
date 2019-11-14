from django.db import models
from django_analysis.models.analysis_version import AnalysisVersion
from django_extensions.db.models import TimeStampedModel


class RunManager(models.Manager):
    def get_existing(self, analysis_version: AnalysisVersion, **kwargs):
        runs = self.filter(analysis_version=analysis_version)
        configuration = analysis_version.update_input_with_defaults(**kwargs)
        matching = [run for run in runs if run.input_configuration == configuration]
        return matching[0] if matching else None

    def create_and_execute(self, analysis_version: AnalysisVersion, **kwargs):
        run = self.create(analysis_version=analysis_version)
        run.create_input_instances(**kwargs)
        results = analysis_version.run(**kwargs)
        run.create_output_instances(**results)
        return run

    def get_or_execute(self, analysis_version: AnalysisVersion, **kwargs):
        existing = self.get_existing(analysis_version, **kwargs)
        return existing or self.create_and_execute(analysis_version, **kwargs)


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

    def create_input_instances(self, **kwargs) -> list:
        input_definitions = self.analysis_version.get_input_definitions_for_kwargs(
            **kwargs
        )
        inputs = []
        for key, value in kwargs.items():
            input_definition = input_definitions.get(key=key)
            input_instance = input_definition.create_input_instance(
                value=value, definition=input_definition, run=self
            )
            inputs.append(input_instance)
        return inputs

    def create_output_instances(self, **results) -> list:
        output_definitions = self.analysis_version.get_output_definitions_for_results(
            **results
        )
        outputs = []
        for key, value in results.items():
            output_definition = output_definitions.get(key=key)
            output_instance = output_definition.create_output_instance(
                value=value, definition=output_definition, run=self
            )
            outputs.append(output_instance)
        return outputs

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
