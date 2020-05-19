from django.db import models
from model_utils.managers import InheritanceManager


class Output(models.Model):
    run = models.ForeignKey(
        "django_analyses.Run", on_delete=models.CASCADE, related_name="base_output_set"
    )

    value = None
    definition = None

    objects = InheritanceManager()

    class Meta:
        ordering = ("run",)

    def __str__(self) -> str:
        return f"'{self.key}' = {self.value}"

    def pre_save(self) -> None:
        pass

    def validate(self) -> None:
        pass

    def save(self, *args, **kwargs):
        self.pre_save()
        self.validate()
        super().save(*args, **kwargs)

    @property
    def key(self) -> str:
        if self.definition:
            return self.definition.key
