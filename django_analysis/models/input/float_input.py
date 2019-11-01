from django.db import models
from django_analysis.models.input.number_input import NumberInput


class FloatInput(NumberInput):
    value = models.FloatField()
    configuration = models.ForeignKey(
        "django_analysis.FloatInputConfiguration", on_delete=models.PROTECT
    )
