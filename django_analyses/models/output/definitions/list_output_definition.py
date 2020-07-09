############ Ask Zvi ############

from django.contrib.postgres.fields import JSONField
from django.core.exceptions import ValidationError
from django.db import models
from django.utils.translation import gettext_lazy as _
from django_analyses.models.output.definitions.output_definition import OutputDefinition
from django_analyses.models.output.types.list_output import ListOutput
from django_analyses.models.input.utils import ListElementTypes
from django_analyses.models.output.definitions.output_definitions import (
    OutputDefinitions,
)
from pathlib import Path


class ListOutputDefinition(OutputDefinition):
    element_type = models.CharField(max_length=3, choices=ListElementTypes.choices())
    as_tuple = models.BooleanField(default=False)

    output_class = ListOutput

    def get_type(self) -> OutputDefinitions:
        return OutputDefinitions.LST
