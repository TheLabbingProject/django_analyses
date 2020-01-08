from django_analyses.models.output.definitions.output_definition import OutputDefinition
from django_analyses.models.output.definitions.output_definitions import (
    OutputDefinitions,
)
from django_analyses.models.output.types.float_output import FloatOutput


class FloatOutputDefinition(OutputDefinition):
    output_class = FloatOutput

    def get_type(self) -> str:
        return OutputDefinitions.FLT
