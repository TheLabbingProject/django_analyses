from django.db import models
from django_analyses.models.output.output import Output
from django_analyses.models.output.types.output_types import OutputTypes


class FloatOutput(Output):
    value = models.FloatField()
    definition = models.ForeignKey(
        "django_analyses.FloatOutputDefinition",
        on_delete=models.PROTECT,
        related_name="output_set",
    )

    def get_type(self) -> str:
        return OutputTypes.FLT
