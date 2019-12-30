from django.core.exceptions import ValidationError
from django_analyses.models.input.definitions.input_definition import InputDefinition


class NumberInputDefinition(InputDefinition):
    def raise_default_under_min_error(self):
        raise ValidationError(f"{self.key} must be greater than {self.min_value}")

    def raise_default_over_max_error(self):
        raise ValidationError(f"{self.key} must be lesser than {self.max_value}")

    def validate_default(self):
        if self.min_value is not None:
            if self.default < self.min_value:
                self.raise_default_under_min_error()
        if self.max_value is not None:
            if self.default > self.max_value:
                self.raise_default_over_max_error()

    def validate(self) -> None:
        if self.default:
            self.validate_default()

