from django.core.exceptions import ValidationError
from django.db.models.base import ModelBase
from django.db import models
from django_analyses.models.input.input import Input
from django_analyses.models.managers.input_definition import (
    InputDefinitionManager,
)
from django_analyses.models.input.definitions import messages


class InputDefinition(models.Model):
    key = models.CharField(max_length=50)
    required = models.BooleanField(default=False)
    description = models.TextField(blank=True, null=True)

    # Child models may allow setting a default value using the
    # appropriate django.db.models.Field type.
    default = None

    # Whether this input definition is a configuration of the analysis
    # parameters or, e.g., a definition of the input or output of it.
    is_configuration = models.BooleanField(default=True)

    # If the actual input to the analysis class is meant to be some attribute
    # of given input, the attribute name may be set here.
    value_attribute = models.CharField(max_length=255, blank=True, null=True)

    db_value_preprocessing = models.CharField(
        max_length=255, blank=True, null=True
    )

    # Whether the created inputs instances should be passed to interface's
    # class at initialization (False) or upon calling the run method (True).
    run_method_input = models.BooleanField(default=False)

    # Each definition should override this class attribute in order
    # to allow for Input instances creation.
    input_class = None

    objects = InputDefinitionManager()

    class Meta:
        ordering = ("key",)

    def __str__(self) -> str:
        try:
            input_type = self.input_class.__name__.replace("Input", "")
        except AttributeError:
            return self.key
        else:
            return f"{self.key:<50}\t{input_type:<30}"

    def extract_nested_value(self, value, location: str):
        parts = location.split(".")
        for part in parts:
            value = getattr(value, part)
        return value() if callable(value) else value

    def check_input_class_definition(self) -> None:
        input_base_name = f"{Input.__module__}.{Input.__name__}"
        not_model = not isinstance(self.input_class, ModelBase)
        base = getattr(self.input_class, "__base__", None)
        not_input_subclass = base is not Input
        invalid_input_class = (
            not self.input_class or not_model or not_input_subclass
        )
        if invalid_input_class:
            message = messages.INVALID_INPUT_CLASS.format(
                base_name=input_base_name
            )
            raise ValidationError(message)

    def get_db_value(self, value):
        if value and self.db_value_preprocessing:
            location = self.db_value_preprocessing
            if isinstance(value, list):
                return [
                    self.extract_nested_value(element, location)
                    for element in value
                ]
            return self.extract_nested_value(value, location)
        return value

    def get_or_create_input_instance(self, **kwargs) -> Input:
        kwargs["value"] = self.get_db_value(kwargs.get("value"))
        try:
            return self.input_class.objects.get_or_create(
                definition=self, **kwargs
            )
        except AttributeError:
            self.check_input_class_definition()
            raise

    def validate(self) -> None:
        pass

    def save(self, *args, **kwargs):
        self.validate()
        super().save(*args, **kwargs)
