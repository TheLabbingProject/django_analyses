from django.core.exceptions import ValidationError
from django.db import models
from django.db.models.base import ModelBase
from django_analyses.models.managers.output_definition import OutputDefinitionManager
from django_analyses.models.output.definitions.messages import (
    INVALID_OUTPUT_CLASS_DEFINITION,
)
from django_analyses.models.output.output import Output


class OutputDefinition(models.Model):
    key = models.CharField(max_length=50)
    description = models.TextField(blank=True, null=True)

    objects = OutputDefinitionManager()

    output_class = None

    class Meta:
        ordering = ("key",)

    def __str__(self) -> str:
        try:
            output_type = self.output_class.__name__.replace("Output", "")
        except AttributeError:
            return self.key
        else:
            return f"{self.key:<50}\t{output_type:<30}"

    def check_output_class_definition(self) -> None:
        output_base_name = f"{Output.__module__}.{Output.__name__}"
        not_model = not isinstance(self.output_class, ModelBase)
        base = getattr(self.output_class, "__base__", None)
        not_output_subclass = base is not Output
        if not self.output_class or not_model or not_output_subclass:
            message = INVALID_OUTPUT_CLASS_DEFINITION.format(base_name=output_base_name)
            raise ValidationError(message)

    def pre_output_instance_create(self, kwargs: dict) -> None:
        pass

    def create_output_instance(self, **kwargs) -> Output:
        self.pre_output_instance_create(kwargs)
        try:
            return self.output_class.objects.create(definition=self, **kwargs)
        except AttributeError:
            self.check_output_class_definition()
            raise
