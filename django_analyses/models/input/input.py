from django.core.exceptions import ValidationError
from django.db import models
from model_utils.managers import InheritanceManager


class Input(models.Model):
    run = models.ForeignKey(
        "django_analyses.Run",
        on_delete=models.CASCADE,
        related_name="base_input_set",
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
        if self.value_is_foreign_key and isinstance(self.value, int):
            self.value = self.value.related_model.get(id=self.value)

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
            location = self.definition.value_attribute
            return self.definition.extract_nested_value(value, location)
        return value

    @property
    def key(self) -> str:
        if self.definition:
            return self.definition.key

    @property
    def argument_value(self):
        return self.get_argument_value()

    @property
    def value_is_foreign_key(self) -> bool:
        value_field = self._meta.get_field("value")
        return isinstance(value_field, models.ForeignKey)
