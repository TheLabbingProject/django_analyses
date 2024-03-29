from pathlib import Path

from django.db import models
from django_analyses.models.output.output import Output
from django_analyses.models.output.types.output_types import OutputTypes
from django_analyses.models.utils.get_media_root import get_media_root
from django_analyses.models.utils.html_repr import html_repr


class FileOutput(Output):
    value = models.FilePathField(
        path=get_media_root(), max_length=1000, blank=True, null=True
    )
    definition = models.ForeignKey(
        "django_analyses.FileOutputDefinition",
        on_delete=models.PROTECT,
        related_name="output_set",
    )

    def get_type(self) -> str:
        return OutputTypes.FIL

    def raise_missing_output_error(self) -> None:
        raise FileNotFoundError(
            f"{self.key} could not be found in {self.value}!"
        )

    def validate(self) -> None:
        if self.value:
            file_exists = Path(self.value).is_file()
            if self.definition.validate_existence and not file_exists:
                self.raise_missing_output_error()
        return super().validate()

    def pre_save(self) -> None:
        if isinstance(self.value, Path):
            self.value = str(self.value.absolute())
        return super().pre_save()

    def _repr_html_(self) -> str:
        return html_repr(Path(self.value))
