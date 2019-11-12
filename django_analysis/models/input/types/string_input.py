from django.core.exceptions import ValidationError
from django.db import models
from django_analysis.models.input.input import Input


class StringInput(Input):
    value = models.CharField(max_length=1000)
    definition = models.ForeignKey(
        "django_analysis.StringInputDefinition",
        on_delete=models.PROTECT,
        related_name="input_set",
    )

    def validate_min_length(self) -> bool:
        min_length = self.definition.min_length
        return len(self.value) >= min_length if min_length else True

    def raise_min_length_error(self) -> None:
        min_length = self.definition.min_length
        raise ValidationError(f"{self.key} must be {min_length} characters or longer!")

    def validate_max_length(self) -> bool:
        max_length = self.definition.max_length
        return len(self.value) <= max_length if max_length else True

    def raise_max_length_error(self) -> None:
        max_length = self.definition.max_length
        raise ValidationError(f"{self.key} must be {max_length} characters or shorter!")

    def validate_from_choices(self) -> bool:
        choices = self.definition.choices
        return self.value in choices if choices else True

    def raise_invalid_choice_error(self) -> None:
        choices = self.definition.choices
        raise ValidationError(
            f"{self.key} must be one of the following choices: {choices}!"
        )

    def validate(self) -> None:
        if not self.valid_min_length:
            self.raise_min_length_error()
        if not self.valid_max_length:
            self.raise_max_length_error()
        if not self.valid_choice:
            self.raise_invalid_choice_error()

    @property
    def key(self) -> str:
        return self.definition.key

    @property
    def valid_min_length(self) -> bool:
        return self.validate_min_length()

    @property
    def valid_max_length(self) -> bool:
        return self.validate_max_length()

    @property
    def valid_choice(self) -> bool:
        return self.validate_from_choices()
