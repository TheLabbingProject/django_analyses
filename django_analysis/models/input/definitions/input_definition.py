from django.db import models
from model_utils.managers import InheritanceManager


class InputDefinition(models.Model):
    key = models.CharField(max_length=50)
    required = models.BooleanField(default=False)
    description = models.TextField(blank=True, null=True)

    objects = InheritanceManager()

    def __str__(self) -> str:
        return self.key
