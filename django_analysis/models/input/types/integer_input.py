from django.db import models
from django_analysis.models.input.types.number_input import NumberInput


class IntegerInput(NumberInput):
    value = models.IntegerField()
    definition = models.ForeignKey(
        "django_analysis.IntegerInputDefinition", on_delete=models.PROTECT
    )
