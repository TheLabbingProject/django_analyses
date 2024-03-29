from pathlib import Path

from django.core.exceptions import ValidationError
from django.db import models
from django_analyses.models.input.input import Input
from django_analyses.models.input.types.input_types import InputTypes
from django_analyses.models.input.utils import TYPES_DICT, ListElementTypes
from django_analyses.models.utils.html_repr import html_repr


class ListInput(Input):
    value = models.JSONField()
    definition = models.ForeignKey(
        "django_analyses.ListInputDefinition",
        on_delete=models.PROTECT,
        related_name="input_set",
    )

    @classmethod
    def validate_element_types(cls, value: list, expected_type: type) -> bool:
        if expected_type == "file":
            return all([Path(element).is_file() for element in value])
        return all([type(element) is expected_type for element in value])

    def validate_min_length(self) -> bool:
        min_length = self.definition.min_length
        return len(self.value) >= min_length if min_length else True

    def raise_min_length_error(self) -> None:
        key = self.definition.key
        min_length = self.definition.min_length
        raise ValidationError(
            f"'{key}' must have at least {min_length} elements!"
        )

    def validate_max_length(self) -> bool:
        max_length = self.definition.max_length
        return len(self.value) <= max_length if max_length else True

    def raise_max_length_error(self) -> None:
        key = self.definition.key
        max_length = self.definition.max_length
        raise ValidationError(
            f"'{key}' must have at most {max_length} elements!"
        )

    def raise_not_list_error(self) -> None:
        raise ValidationError("ListInput value must be a list instance!")

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
        if not self.valid_min_length:
            self.raise_min_length_error()
        if not self.valid_max_length:
            self.raise_max_length_error()

    def get_type(self) -> InputTypes:
        return InputTypes.LST

    def get_argument_value(self):
        value = super().get_argument_value()
        if self.definition.as_tuple:
            return tuple(value)
        return value

    def get_html_repr(self, index: int) -> str:
        path = Path(self.value[index])
        return html_repr(path)

    def query_related_instance(self) -> models.QuerySet:
        if self.definition.content_type:
            Model = self.definition.content_type.model_class()
            field_name = self.definition.field_name or "id"
            return Model.objects.filter(**{f"{field_name}__in": self.value})

    def _repr_html_(self) -> str:
        try:
            return "<br>".join(
                [self.get_html_repr(index) for index in range(len(self.value))]
            )
        except TypeError:
            pass

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
