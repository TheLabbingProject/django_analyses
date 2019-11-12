from django.db import models
from django_analysis.models.input.definitions.input_definition import InputDefinition
from django_analysis.models.input.types.list_input import ListInput
from django_analysis.models.input.utils import ListElementTypes


class ListInputDefinition(InputDefinition):
    element_type = models.CharField(max_length=3, choices=ListElementTypes.choices())
    min_length = models.PositiveIntegerField(blank=True, null=True)
    max_length = models.PositiveIntegerField(blank=True, null=True)

    INPUT_CLASS = ListInput
