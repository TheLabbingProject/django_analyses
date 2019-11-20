from django.db import models
from django_analysis.models.input.types.number_input import NumberInput
from django_analysis.models.input.types.input_types import InputTypes


class IntegerInput(NumberInput):
    value = models.IntegerField()
    definition = models.ForeignKey(
        "django_analysis.IntegerInputDefinition",
        on_delete=models.PROTECT,
        related_name="input_set",
    )

    def get_type(self) -> InputTypes:
        return InputTypes.INT
