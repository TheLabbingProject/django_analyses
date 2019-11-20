from django.db import models
from django_analysis.models.input.definitions.input_definition import InputDefinition
from django_analysis.models.input.types.boolean_input import BooleanInput
from django_analysis.models.input.definitions.input_definitions import InputDefinitions


class BooleanInputDefinition(InputDefinition):
    default = models.BooleanField(blank=True, null=True)

    INPUT_CLASS = BooleanInput

    def get_input_type(self) -> InputDefinitions:
        return InputDefinitions.BLN
