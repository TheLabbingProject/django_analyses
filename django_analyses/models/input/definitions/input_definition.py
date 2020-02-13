from django.core.exceptions import ValidationError
from django.db.models.base import ModelBase
from django.db import models
from django_analyses.models.input.input import Input
from django_analyses.models.managers.input_definition import InputDefinitionManager


class InputDefinition(models.Model):
    key = models.CharField(max_length=50)
    required = models.BooleanField(default=False)
    description = models.TextField(blank=True, null=True)

    # Whether this input definition is a configuration of the analysis
    # parameters or, e.g., a definition of the input or output of it.
    is_configuration = models.BooleanField(default=True)

    # Whether the created inputs instances should be passed to interface's
    # class at initialization (False) or upon calling the run method (True).
    run_method_input = models.BooleanField(default=False)

    # Child models may allow setting a default value using the
    # appropriate django.db.models.Field type.
    default = None

    # Each definition should override this class attribute in order
    # to allow for Input instances creation.
    input_class = None

    objects = InputDefinitionManager()

    class Meta:
        ordering = ("key",)

    def __str__(self) -> str:
        return self.key

    def check_input_class_definition(self) -> None:
        input_base_name = f"{Input.__module__}.{Input.__name__}"
        not_model = not isinstance(self.input_class, ModelBase)
        base = getattr(self.input_class, "__base__", None)
        not_input_subclass = base is not Input
        if not self.input_class or not_model or not_input_subclass:
            raise ValidationError(
                f"Please set the input_class attribute to the appropriate {input_base_name} subclass."
            )

    def get_or_create_input_instance(self, **kwargs) -> Input:
        try:
            return self.input_class.objects.get_or_create(definition=self, **kwargs)
        except AttributeError:
            self.check_input_class_definition()
            raise

    def validate(self) -> None:
        pass

    def save(self, *args, **kwargs):
        self.validate()
        super().save(*args, **kwargs)
