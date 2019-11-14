from django.db import models
from model_utils.managers import InheritanceManager


class Output(models.Model):
    run = models.ForeignKey("django_analysis.Run", on_delete=models.CASCADE)

    value = None
    definition = None

    objects = InheritanceManager()

    def __str__(self) -> str:
        return str(self.value)

    def validate(self) -> None:
        pass

    def save(self, *args, **kwargs):
        self.validate()
        super().save(*args, **kwargs)
