from django.db import models
from model_utils.managers import InheritanceManager


class InputDefinition(models.Model):
    input_specification = models.ForeignKey(
        "django_analysis.InputSpecification", on_delete=models.CASCADE
    )
    key = models.CharField(max_length=50)
    required = models.BooleanField()

    objects = InheritanceManager()

