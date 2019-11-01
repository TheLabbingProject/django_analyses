from django_analysis.models.input.input import Input


class NumberInput(Input):
    value = None
    configuration = None

    def validate_min_value(self):
        min_value = self.configuration.min_value
        return self.value >= min_value if min_value or min_value == 0 else True

    def raise_min_value_error(self):
        key = self.configuration.key
        min_value = self.configuration.min_value
        raise ValueError(f"{key} must be greater than {min_value}!")

    def validate_max_value(self):
        max_value = self.configuration.max_value
        return self.value <= max_value if max_value or max_value == 0 else True

    def raise_max_value_error(self):
        key = self.configuration.key
        max_value = self.configuration.max_value
        raise ValueError(f"{key} must be less than {max_value}!")

    def validate(self):
        if not self.valid_min_value:
            self.raise_min_value_error()
        if not self.valid_max_value:
            self.raise_max_value_error()

    @property
    def valid_min_value(self) -> bool:
        return self.validate_min_value()

    @property
    def valid_max_value(self) -> bool:
        return self.validate_max_value()

