from django.db import models
from django_analysis.models.input.input import Input
from django_analysis.models.managers.input_definition import InputDefinitionManager


class InputDefinition(models.Model):
    key = models.CharField(max_length=50)
    required = models.BooleanField(default=False)
    description = models.TextField(blank=True, null=True)
    is_configuration = models.BooleanField(default=True)
    default = None

    objects = InputDefinitionManager()

    INPUT_CLASS = None

    def __str__(self) -> str:
        return self.key

    def create_input_instance(self, **kwargs) -> Input:
        return self.INPUT_CLASS.objects.create(definition=self, **kwargs)

    def validate(self) -> None:
        pass

    def save(self, *args, **kwargs):
        self.validate()
        super().save(*args, **kwargs)
