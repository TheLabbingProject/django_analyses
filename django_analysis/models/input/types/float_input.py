from django.db import models
from django_analysis.models.input.types.number_input import NumberInput


class FloatInput(NumberInput):
    value = models.FloatField()
    definition = models.ForeignKey(
        "django_analysis.FloatInputDefinition",
        on_delete=models.PROTECT,
        related_name="input_set",
    )
