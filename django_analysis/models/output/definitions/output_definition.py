from copy import deepcopy
from django.db import models
from model_utils.managers import InheritanceManager


class OutputDefinitionManager(InheritanceManager):
    def from_specification_dict(self, specification: dict) -> list:
        specification = deepcopy(specification)
        output_definitions = []
        for key, definition in specification.items():
            output_type_model = definition.pop("type")
            output_type_instance, _ = output_type_model.objects.get_or_create(
                key=key, **definition
            )
            output_definitions.append(output_type_instance)
        return output_definitions


class OutputDefinition(models.Model):
    key = models.CharField(max_length=50)
    description = models.TextField(blank=True, null=True)

    objects = OutputDefinitionManager()

    OUTPUT_CLASS = None

    def __str__(self) -> str:
        return self.key
