from django.db import models
from django_analyses.models.input.definitions.input_definition import InputDefinition
from django_analyses.models.input.types.directory_input import DirectoryInput
from django_analyses.models.input.definitions.input_definitions import InputDefinitions


class DirectoryInputDefinition(InputDefinition):
    is_output_directory = models.BooleanField(default=False)
    default = models.FilePathField(
        allow_files=False, allow_folders=True, null=True, blank=True
    )

    input_class = DirectoryInput

    def get_type(self) -> InputDefinitions:
        return InputDefinitions.DIR
