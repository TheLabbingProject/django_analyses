import shutil

from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.exceptions import ObjectDoesNotExist
from django.db import models
from django_analyses.models.input.definitions.string_input_definition import (
    StringInputDefinition,
)
from django_analyses.models.input.definitions.directory_input_definition import (
    DirectoryInputDefinition,
)
from django_analyses.models.input.input import Input
from django_analyses.models.input.types.directory_input import DirectoryInput
from django_analyses.models.managers.run import RunManager
from django_analyses.models.output.output import Output
from django_extensions.db.models import TimeStampedModel
from pathlib import Path


class Run(TimeStampedModel):
    analysis_version = models.ForeignKey(
        "django_analyses.AnalysisVersion", on_delete=models.PROTECT
    )
    user = models.ForeignKey(
        get_user_model(), blank=True, null=True, on_delete=models.SET_NULL,
    )

    objects = RunManager()

    class Meta:
        ordering = ("-created",)

    def __str__(self):
        return f"#{self.id} {self.analysis_version} run from {self.created}"

    def delete(self, using=None, keep_parents=False):
        if self.path:
            shutil.rmtree(self.path)
        return super().delete(using=using, keep_parents=keep_parents)

    def create_input_instance(self, key: str, value) -> Input:
        input_definition = self.analysis_version.input_definitions.get(key=key)
        return input_definition.create_input_instance(value=value, run=self)

    def get_missing_output_path_definitions(self, **kwargs) -> list:
        return [
            definition
            for definition in self.analysis_version.input_definitions
            if isinstance(definition, StringInputDefinition)
            and definition.is_output_path
            and definition.key not in kwargs
        ]

    def get_missing_output_directory_definition(
        self, **kwargs
    ) -> DirectoryInputDefinition:
        try:
            return [
                definition
                for definition in self.analysis_version.input_definitions
                if isinstance(definition, DirectoryInputDefinition)
                and definition.is_output_directory
                and definition.key not in kwargs
            ][0]
        except IndexError:
            return None

    def create_missing_output_path_definitions(self, **kwargs) -> list:
        return [
            output_path_definition.create_input_instance(run=self)
            for output_path_definition in self.get_missing_output_path_definitions(
                **kwargs
            )
        ]

    def get_missing_dynamic_defaults(self, **kwargs) -> list:
        return [
            definition
            for definition in self.analysis_version.input_definitions
            if getattr(definition, "dynamic_default", False)
            and definition.key not in kwargs
        ]

    def create_missing_dynamic_defaults(self, **kwargs) -> list:
        return [
            dynamic_default_definition.create_input_instance(run=self)
            for dynamic_default_definition in self.get_missing_dynamic_defaults(
                **kwargs
            )
        ]

    def create_missing_output_directory_definition(self, **kwargs) -> DirectoryInput:
        definition = self.get_missing_output_directory_definition()
        if definition:
            return definition.create_input_instance(run=self)

    def create_input_instances(self, **kwargs) -> list:
        input_instances = [
            self.create_input_instance(key, value) for key, value in kwargs.items()
        ]
        input_instances += self.create_missing_output_path_definitions(**kwargs)
        input_instances += self.create_missing_dynamic_defaults(**kwargs)
        output_directory = self.create_missing_output_directory_definition()
        if output_directory:
            input_instances += [output_directory]
        return input_instances

    def create_output_path_destinations(self, inputs: models.QuerySet):
        for inpt in inputs:
            inpt.create_required_destination()

    def create_output_instance(self, key: str, value) -> Output:
        try:
            output_definition = self.analysis_version.output_definitions.get(key=key)
        except ObjectDoesNotExist:
            pass
        else:
            return output_definition.create_output_instance(value=value, run=self)

    def create_output_instances(self, **results) -> list:
        output_instances = [
            self.create_output_instance(key, value) for key, value in results.items()
        ]
        return [output for output in output_instances if output is not None]

    def get_input_set(self) -> models.QuerySet:
        return self.base_input_set.select_subclasses()

    def get_output_set(self) -> models.QuerySet:
        return self.base_output_set.select_subclasses()

    def get_input_configuration(self) -> dict:
        defaults = self.input_defaults.copy()
        defaults.update(self.raw_input_configuration)
        return defaults

    def get_output_configuration(self) -> dict:
        return {output.key: output.value for output in self.output_set}

    def get_raw_input_configuation(self) -> dict:
        return {
            inpt.key: inpt.value
            if not getattr(inpt.definition, "is_output_path", False)
            else Path(inpt.value).name
            for inpt in self.input_set
            if not getattr(inpt.definition, "is_output_directory", False)
        }

    @property
    def path(self) -> Path:
        path = Path(settings.ANALYSIS_BASE_PATH) / str(self.id)
        return path if path.is_dir() else None

    @property
    def input_defaults(self) -> dict:
        return self.analysis_version.input_specification.default_configuration

    @property
    def input_configuration(self) -> dict:
        return self.get_input_configuration()

    @property
    def output_configuration(self) -> dict:
        return self.get_output_configuration()

    @property
    def input_set(self) -> models.QuerySet:
        return self.get_input_set()

    @property
    def output_set(self) -> models.QuerySet:
        return self.get_output_set()

    @property
    def raw_input_configuration(self) -> dict:
        return self.get_raw_input_configuation()
