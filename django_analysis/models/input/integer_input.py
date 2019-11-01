from django.db import models
from django_analysis.models.input.number_input import NumberInput


class IntegerInput(NumberInput):
    value = models.IntegerField()
    configuration = models.ForeignKey(
        "django_analysis.IntegerInputConfiguration", on_delete=models.PROTECT
    )
