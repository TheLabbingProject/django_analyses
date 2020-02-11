from django.db import models
from django_analyses.models.output.definitions.output_definition import OutputDefinition
from django_analyses.models.output.definitions.output_definitions import (
    OutputDefinitions,
)
from django_analyses.models.output.types.file_output import FileOutput


class FileOutputDefinition(OutputDefinition):
    validate_existence = models.BooleanField(default=True)
    output_class = FileOutput

    def get_type(self) -> str:
        return OutputDefinitions.FIL
