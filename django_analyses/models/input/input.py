from django.core.exceptions import ValidationError
from django.db import models
from model_utils.managers import InheritanceManager
from pathlib import Path


class Input(models.Model):
    run = models.ForeignKey(
        "django_analyses.Run", on_delete=models.CASCADE, related_name="base_input_set"
    )

    value = None
    definition = None

    objects = InheritanceManager()

    def __str__(self) -> str:
        return f"'{self.key}' = {self.value}"

    def raise_required_error(self):
        raise ValidationError(f"{self.key} is required!")

    def pre_save(self) -> None:
        pass

    def validate(self) -> None:
        if self.definition.required and self.value is None:
            self.raise_required_error()

    def save(self, *args, **kwargs):
        self.pre_save()
        self.validate()
        super().save(*args, **kwargs)

    def get_required_destination(self) -> Path:
        output_path = getattr(self.definition, "is_output_path", False)
        if output_path:
            return Path(self.value).parent
        output_directory = getattr(self.definition, "is_output_directory", False)
        if output_directory:
            return Path(self.value)

    def create_required_destination(self) -> Path:
        if self.required_destination:
            self.required_destination.mkdir(parents=True, exist_ok=True)
            return self.required_destination

    @property
    def key(self) -> str:
        return self.definition.key

    @property
    def required_destination(self) -> Path:
        return self.get_required_destination()
