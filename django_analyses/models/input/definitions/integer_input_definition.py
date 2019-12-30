from django.db import models
from django_analyses.models.input.definitions.input_definitions import InputDefinitions
from django_analyses.models.input.definitions.number_input_definition import (
    NumberInputDefinition,
)
from django_analyses.models.input.types.integer_input import IntegerInput


class IntegerInputDefinition(NumberInputDefinition):
    min_value = models.IntegerField(blank=True, null=True)
    max_value = models.IntegerField(blank=True, null=True)
    default = models.IntegerField(blank=True, null=True)

    input_class = IntegerInput

    def get_type(self) -> InputDefinitions:
        return InputDefinitions.INT

