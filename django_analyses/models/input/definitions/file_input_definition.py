from django.db import models
from django_analyses.models.input.definitions.input_definition import InputDefinition
from django_analyses.models.input.types.file_input import FileInput
from django_analyses.models.input.definitions.input_definitions import InputDefinitions


class FileInputDefinition(InputDefinition):
    default = models.FilePathField(blank=True, null=True)

    input_class = FileInput

    def get_type(self) -> InputDefinitions:
        return InputDefinitions.FIL
