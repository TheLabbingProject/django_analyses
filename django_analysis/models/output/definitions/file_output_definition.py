from django_analysis.models.output.definitions.output_definition import OutputDefinition
from django_analysis.models.output.definitions.output_definitions import (
    OutputDefinitions,
)
from django_analysis.models.output.types.file_output import FileOutput


class FileOutputDefinition(OutputDefinition):
    OUTPUT_CLASS = FileOutput

    def get_type(self) -> str:
        return OutputDefinitions.FIL
