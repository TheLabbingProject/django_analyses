from pathlib import Path

from django.core.exceptions import ValidationError
from django.db import models
from django.utils.translation import gettext_lazy as _
from django_analyses.models.input.definitions.input_definition import (
    InputDefinition,
)
from django_analyses.models.input.definitions.input_definitions import (
    InputDefinitions,
)
from django_analyses.models.input.types.list_input import ListInput
from django_analyses.models.input.utils import TYPES_DICT, ListElementTypes


class ListInputDefinition(InputDefinition):
    element_type = models.CharField(
        max_length=3, choices=ListElementTypes.choices()
    )
    min_length = models.PositiveIntegerField(blank=True, null=True)
    max_length = models.PositiveIntegerField(blank=True, null=True)
    default = models.JSONField(blank=True, null=True)
    as_tuple = models.BooleanField(default=False)

    input_class = ListInput

    def raise_not_list_error(self) -> None:
        raise ValidationError(
            _("Default ListInputDefinition value must be a list instance!")
        )

    def raise_wrong_type_error(self) -> None:
        required_type = ListElementTypes[self.element_type].value.lower()
        raise ValidationError(
            _(f"List elements must be of type {required_type}")
        )

    def validate_elements_type_for_default(self) -> bool:
        required_type = TYPES_DICT[ListElementTypes[self.element_type]]
        if required_type == "file":
            return all([Path(element).is_file() for element in self.default])
        return all(
            [type(element) == required_type for element in self.default]
        )

    def validate_default_value_min_length(self) -> bool:
        return (
            len(self.default) >= self.min_length if self.min_length else True
        )

    def raise_min_length_error(self) -> None:
        raise ValidationError(
            _(f"Default value must have at least {self.min_length} elements!")
        )

    def validate_default_value_max_length(self) -> bool:
        return (
            len(self.default) <= self.max_length if self.max_length else True
        )

    def raise_max_length_error(self) -> None:
        raise ValidationError(
            _(f"Default value must have at most {self.max_length} elements!")
        )

    def validate_default_value(self) -> None:
        if not isinstance(self.default, list):
            self.raise_not_list_error()
        if not self.validate_elements_type_for_default():
            self.raise_wrong_type_error()
        if not self.validate_default_value_min_length():
            self.raise_min_length_error()
        if not self.validate_default_value_max_length():
            self.raise_max_length_error()

    def validate(self):
        if self.default is not None:
            self.validate_default_value()
        super().validate()

    def get_type(self) -> InputDefinitions:
        return InputDefinitions.LST

    @property
    def expected_type_definition(self) -> ListElementTypes:
        return ListElementTypes[self.element_type]
