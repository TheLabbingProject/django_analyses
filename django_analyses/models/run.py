import shutil

from django.conf import settings
from django.contrib.auth import get_user_model
from django.db import models
from django_analyses.models.managers.run import RunManager
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

    def get_raw_input_configuration(self) -> dict:
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
        return self.get_raw_input_configuration()
