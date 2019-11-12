from django_analysis.models.input.definitions.input_definition import InputDefinition
from django_analysis.models.input.types.file_input import FileInput


class FileInputDefinition(InputDefinition):
    INPUT_CLASS = FileInput

