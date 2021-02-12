from pathlib import Path

from django.core.exceptions import ValidationError
from django.db import models
from django_analyses.models.input.utils import TYPES_DICT, ListElementTypes
from django_analyses.models.output.output import Output
from django_analyses.models.output.types.output_types import OutputTypes


class ListOutput(Output):
    value = models.JSONField()
    definition = models.ForeignKey(
        "django_analyses.ListOutputDefinition",
        on_delete=models.PROTECT,
        related_name="output_set",
    )

    @classmethod
    def validate_element_types(cls, value: list, expected_type: type) -> bool:
        if expected_type == "file":
            return all([Path(element).is_file() for element in value])
        return all([type(element) is expected_type for element in value])

    def raise_not_list_error(self) -> None:
        raise ValidationError("ListOutput value must be a list instance!")

    def raise_incorrect_type_error(self) -> None:
        raise ValidationError(
            f"List elements must be of type {self.expected_type}!"
        )

    def validate(self) -> None:
        if not isinstance(self.value, list):
            self.raise_not_list_error()
        if not self.valid_elements:
            if self.expected_type is float and self.validate_element_types(
                self.value, int
            ):
                self.value = [float(element) for element in self.value]
                self.validate()
            else:
                self.raise_incorrect_type_error()

    def get_type(self) -> OutputTypes:
        return OutputTypes.LST

    def get_argument_value(self):
        value = super().get_argument_value()
        if self.definition.as_tuple:
            return tuple(value)
        return value

    @property
    def expected_type_definition(self) -> ListElementTypes:
        return ListElementTypes[self.definition.element_type]

    @property
    def expected_type(self) -> type:
        return TYPES_DICT[self.expected_type_definition]

    @property
    def valid_elements(self) -> bool:
        return self.validate_element_types(self.value, self.expected_type)

    @property
    def valid_min_length(self) -> bool:
        return self.validate_min_length()

    @property
    def valid_max_length(self) -> bool:
        return self.validate_max_length()
