from django.db import models
from django_analyses.models.input.definitions.input_definition import InputDefinition
from django_analyses.models.input.types.boolean_input import BooleanInput
from django_analyses.models.input.definitions.input_definitions import InputDefinitions


class BooleanInputDefinition(InputDefinition):
    default = models.BooleanField(blank=True, null=True)
    is_output_switch = models.BooleanField(default=False)

    input_class = BooleanInput

    def get_type(self) -> InputDefinitions:
        return InputDefinitions.BLN
