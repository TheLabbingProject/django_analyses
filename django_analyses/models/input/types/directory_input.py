from django.conf import settings
from django.db import models
from django_analyses.models.input.input import Input
from django_analyses.models.input.types.input_types import InputTypes
from pathlib import Path


class DirectoryInput(Input):
    value = models.FilePathField(
        settings.MEDIA_ROOT, max_length=1000, allow_files=False, allow_folders=True
    )
    definition = models.ForeignKey(
        "django_analyses.DirectoryInputDefinition",
        on_delete=models.PROTECT,
        related_name="input_set",
    )

    def get_type(self) -> InputTypes:
        return InputTypes.DIR

    def fix_output_path(self) -> str:
        if not Path(self.value).is_absolute():
            return str(self.default_output_directory / self.value)
        return str(self.default_output_directory)

    def pre_save(self) -> None:
        if self.definition.is_output_directory:
            self.value = self.fix_output_path()

    @property
    def default_output_directory(self) -> Path:
        return Path(settings.ANALYSIS_BASE_PATH) / str(self.run.id)

    @property
    def required_path(self) -> Path:
        if self.definition.is_output_directory:
            return Path(self.value)
