"""
Definition of the :class:`InputDefinition` class.
"""
from pathlib import Path
from typing import Any

from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import ValidationError
from django.db import models
from django.db.models.base import ModelBase
from django_analyses.models import help_text
from django_analyses.models.input.definitions import messages
from django_analyses.models.input.input import Input
from django_analyses.models.managers.input_definition import (
    InputDefinitionManager,
)


class InputDefinition(models.Model):
    """
    Represents a single input definition in the database. Instances are used to
    as the building blocks for
    :class:`~django_analyses.models.input.input_specification.InputSpecification`
    instances.
    """

    #: Input key used when passing inputs to run some analysis.
    key = models.CharField(max_length=50)

    #: A description of this input definition.
    description = models.TextField(blank=True, null=True)

    #: Whether this input is required for the execution of the analysis.
    required = models.BooleanField(default=False)

    #: Child models may allow setting a default value using the appropriate
    #: :class:`~django.db.models.Field` subclass.
    default = None

    #: Whether this input definition is a configuration of the analysis
    #: parameters or, e.g., a definition of the input or output of it.
    is_configuration = models.BooleanField(
        default=True, help_text=help_text.IS_CONFIGURATION
    )

    #: If the actual input to the analysis class is meant to be some attribute
    #: of given input, the attribute name may be set here.
    value_attribute = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        help_text=help_text.VALUE_ATTRIBUTE,
    )

    #: If values passed as inputs matching this input definition should be
    #: extracted from some object, this field specifies the name of the
    #: attribute which will be called using :func:`get_db_value`.
    db_value_preprocessing = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        help_text=help_text.DB_VALUE_PREPROCESSING,
        verbose_name="DB Value Preprocessing",
    )

    #: Whether the created inputs instances should be passed to interface's
    #: class at initialization (False) or upon calling the run method (True).
    run_method_input = models.BooleanField(
        default=False, help_text=help_text.RUN_METHOD_INPUT
    )

    #: If this input's value references the value of a field in the database,
    #: this references the field's model.
    content_type = models.ForeignKey(
        ContentType, on_delete=models.CASCADE, blank=True, null=True
    )

    #: If this input's value references the value of a field in the database,
    #: this references the field's name within the :att:`content_type` model.
    field_name = models.CharField(max_length=255, blank=True, null=True)

    #: Each definition should override this class attribute in order to allow
    #: for Input instances creation.
    input_class = None

    objects = InputDefinitionManager()

    class Meta:
        ordering = ("key",)

    def __str__(self) -> str:
        """
        Returns the string representation of this instance.

        Returns
        -------
        str
            String representation of this instance
        """
        try:
            input_type = self.input_class.__name__.replace("Input", "")
        except AttributeError:
            return self.key
        else:
            return f"{self.key:<25}\t{input_type:<15}"

    def extract_nested_value(self, obj: Any, location: str) -> Any:
        """
        Extract some nested attribute within an object.

        Parameters
        ----------
        obj : Any
            The object containing the nested value
        location : str
            Address of nested attribute within object

        Returns
        -------
        Any
            Nested attribute value
        """
        parts = location.split(".")
        for part in parts:
            obj = getattr(obj, part)
        return obj() if callable(obj) else obj

    def check_input_class_definition(self) -> None:
        """
        Checks the validity of the assigned :attr:`input_class`.

        Raises
        ------
        ValidationError
            Invalid :attr:`input_class` definition
        """
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

    def get_db_value(self, value: Any) -> Any:
        """
        Returns the appropriate DB value for inputs in which
        :attr:`db_value_preprocessing` is defined.

        Parameters
        ----------
        value : Any
            The object containing the nested value

        Returns
        -------
        Any
            Nested attribute value

        Raises
        ------
        ValueError
            Value extraction failure
        """
        path_field = self.db_value_preprocessing == "path"
        if value and self.db_value_preprocessing:
            location = self.db_value_preprocessing
            if isinstance(value, list):
                return [
                    self.extract_nested_value(element, location)
                    for element in value
                ]
            return self.extract_nested_value(value, location)
        elif value and path_field:
            if isinstance(value, Path) or Path(value).is_file():
                return str(value)
            else:
                try:
                    return str(value.path)
                except AttributeError:
                    raise ValueError(
                        f"Failed to infer path from {value} for {self.key}!"
                    )
        return value

    def get_or_create_input_instance(self, **kwargs) -> Input:
        """
        Creates an instance of the appropriate
        :class:`django_analyses.models.input.input.Input` subclass.

        Returns
        -------
        Input
            Created instance
        """
        kwargs["value"] = self.get_db_value(kwargs.get("value"))
        try:
            return self.input_class.objects.get_or_create(
                definition=self, **kwargs
            )
        except AttributeError:
            self.check_input_class_definition()
            raise

    def validate(self) -> None:
        """
        Validates input definition instances before calling :func:`save`.
        This method should be overridden by subclasses that require some kind
        of custom validation.
        """
        if self.content_type:
            Model = self.content_type.model_class()
            field_name = self.field_name or "id"
            # Raise FieldDoesNotExist if field name is invalid.
            Model._meta.get_field(field_name)

    def save(self, *args, **kwargs):
        """
        Overrides the model's :meth:`~django.db.models.Model.save` method to
        provide custom functionality.
        """
        self.validate()
        super().save(*args, **kwargs)
