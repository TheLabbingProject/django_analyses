from django.db import models
from django_analyses.models.input.types.input_types import InputTypes
from django_analyses.models.input.types.number_input import NumberInput


class FloatInput(NumberInput):
    value = models.FloatField(blank=True, null=True)
    definition = models.ForeignKey(
        "django_analyses.FloatInputDefinition",
        on_delete=models.PROTECT,
        related_name="input_set",
    )

    def get_type(self) -> InputTypes:
        return InputTypes.FLT
