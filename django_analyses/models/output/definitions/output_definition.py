from django.core.exceptions import ValidationError
from django.db import models
from django.db.models.base import ModelBase
from django_analyses.models.managers.output_definition import OutputDefinitionManager
from django_analyses.models.output.output import Output


class OutputDefinition(models.Model):
    key = models.CharField(max_length=50)
    description = models.TextField(blank=True, null=True)

    objects = OutputDefinitionManager()

    output_class = None

    class Meta:
        ordering = ("key",)

    def __str__(self) -> str:
        return self.key

    def check_output_class_definition(self) -> None:
        output_base_name = f"{Output.__module__}.{Output.__name__}"
        not_model = not isinstance(self.output_class, ModelBase)
        base = getattr(self.output_class, "__base__", None)
        not_output_subclass = base is not Output
        if not self.output_class or not_model or not_output_subclass:
            raise ValidationError(
                f"Please set the output_class attribute to the appropriate {output_base_name} subclass."
            )

    def pre_output_instance_create(self, kwargs: dict) -> None:
        pass

    def create_output_instance(self, **kwargs) -> Output:
        self.pre_output_instance_create(kwargs)
        try:
            return self.output_class.objects.create(definition=self, **kwargs)
        except AttributeError:
            self.check_output_class_definition()
            raise
