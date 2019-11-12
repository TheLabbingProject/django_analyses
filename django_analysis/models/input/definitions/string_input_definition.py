from django.contrib.postgres.fields import ArrayField
from django.db import models
from django_analysis.models.input.definitions.input_definition import InputDefinition
from django_analysis.models.input.types.string_input import StringInput


class StringInputDefinition(InputDefinition):
    min_length = models.IntegerField(blank=True, null=True)
    max_length = models.IntegerField(blank=True, null=True)
    default = models.CharField(max_length=500, blank=True, null=True)
    choices = ArrayField(
        models.CharField(max_length=255, blank=True, null=True), blank=True, null=True
    )

    INPUT_CLASS = StringInput
