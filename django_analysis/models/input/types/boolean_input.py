from django.db import models
from django_analysis.models.input.input import Input


class BooleanInput(Input):
    value = models.BooleanField()
    definition = models.ForeignKey(
        "django_analysis.BooleanInputDefinition",
        on_delete=models.PROTECT,
        related_name="input_set",
    )

    def validate(self) -> None:
        pass
