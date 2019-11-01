from django.db import models
from django_analysis.models.input.input import Input


class StringInput(Input):
    value = models.CharField(max_length=1000)
    configuration = models.ForeignKey(
        "django_analysis.StringInputConfiguration", on_delete=models.PROTECT
    )

    def validate_min_length(self):
        min_length = self.configuration.min_length
        return len(self.value) >= min_length if min_length else True

    def raise_min_length_error(self):
        key = self.configuration.key
        min_length = self.configuration.min_length
        raise ValueError(f"{key} must be {min_length} characters or longer!")

    def validate_max_length(self):
        max_length = self.configuration.max_length
        return len(self.value) <= max_length if max_length else True

    def raise_max_length_error(self):
        key = self.configuration.key
        max_length = self.configuration.max_length
        raise ValueError(f"{key} must be {max_length} characters or shorter!")

    def validate(self):
        if not self.valid_min_length:
            self.raise_min_length_error()
        if not self.valid_max_length:
            self.raise_max_length_error()

    @property
    def valid_min_length(self) -> bool:
        return self.validate_min_length()

    @property
    def valid_max_length(self) -> bool:
        return self.validate_max_length()

