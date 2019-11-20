from django_analysis.models.input.definitions.input_definition import InputDefinition
from django_analysis.models.input.types.file_input import FileInput
from django_analysis.models.input.definitions.input_definitions import InputDefinitions


class FileInputDefinition(InputDefinition):
    INPUT_CLASS = FileInput

    def get_type(self) -> InputDefinitions:
        return InputDefinitions.FIL
