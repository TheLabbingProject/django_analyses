from django.db import models
from model_utils.managers import InheritanceManager


class Input(models.Model):
    run = models.ForeignKey("django_analysis.Run", on_delete=models.CASCADE)
    objects = InheritanceManager()

    def validate(self):
        raise NotImplementedError

    def save(self, *args, **kwargs):
        self.validate()
        super().save(*args, **kwargs)
