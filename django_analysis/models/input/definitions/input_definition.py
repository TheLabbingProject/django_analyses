from copy import deepcopy
from django.db import models
from model_utils.managers import InheritanceManager


class InputDefinitionManager(InheritanceManager):
    def from_specification_dict(self, specification: dict) -> list:
        specification = deepcopy(specification)
        input_definitions = []
        for key, definition in specification.items():
            input_type_model = definition.pop("type")
            input_type_instance, _ = input_type_model.objects.get_or_create(
                key=key, **definition
            )
            input_definitions.append(input_type_instance)
        return input_definitions


class InputDefinition(models.Model):
    key = models.CharField(max_length=50)
    required = models.BooleanField(default=False)
    description = models.TextField(blank=True, null=True)

    objects = InputDefinitionManager()

    INPUT_CLASS = None

    def __str__(self) -> str:
        return self.key