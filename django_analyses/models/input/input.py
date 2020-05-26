from django.core.exceptions import ValidationError
from django.db import models
from model_utils.managers import InheritanceManager


class Input(models.Model):
    run = models.ForeignKey(
        "django_analyses.Run", on_delete=models.CASCADE, related_name="base_input_set"
    )

    value = None
    definition = None

    objects = InheritanceManager()

    class Meta:
        ordering = ("run",)

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

    def get_argument_value(self):
        value = self.value
        if self.definition.value_attribute:
            parts = self.definition.value_attribute.split(".")
            for part in parts:
                value = getattr(value, part)
        return value() if callable(value) else value

    @property
    def key(self) -> str:
        if self.definition:
            return self.definition.key

    @property
    def argument_value(self):
        return self.get_argument_value()
