from django.db import models
from django_analyses.models.input.utils import ListElementTypes
from django_analyses.models.output.definitions.output_definition import \
    OutputDefinition
from django_analyses.models.output.definitions.output_definitions import \
    OutputDefinitions
from django_analyses.models.output.types.list_output import ListOutput


class ListOutputDefinition(OutputDefinition):
    element_type = models.CharField(
        max_length=3, choices=ListElementTypes.choices()
    )
    as_tuple = models.BooleanField(default=False)

    output_class = ListOutput

    def get_type(self) -> OutputDefinitions:
        return OutputDefinitions.LST
