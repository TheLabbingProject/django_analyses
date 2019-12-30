from django.db import models
from django_analyses.models.input.definitions.input_definitions import InputDefinitions
from django_analyses.models.input.definitions.number_input_definition import (
    NumberInputDefinition,
)
from django_analyses.models.input.types.float_input import FloatInput


class FloatInputDefinition(NumberInputDefinition):
    min_value = models.FloatField(blank=True, null=True)
    max_value = models.FloatField(blank=True, null=True)
    default = models.FloatField(blank=True, null=True)

    input_class = FloatInput

    def get_type(self) -> InputDefinitions:
        return InputDefinitions.FLT
