from django.db import models
from django_analysis.models.input.definitions.input_definition import InputDefinition


class IntegerInputDefinition(InputDefinition):
    min_value = models.IntegerField(blank=True, null=True)
    max_value = models.IntegerField(blank=True, null=True)
    default = models.IntegerField(blank=True, null=True)

