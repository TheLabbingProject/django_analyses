"""
Definition of the base :class:`Input` model.
"""

from typing import Any

from django.core.exceptions import ValidationError
from django.db import models
from model_utils.managers import InheritanceManager


class Input(models.Model):
    """
    This model serves as a base class for different types of inputs.
    """

    #: The :class:`~django_analyses.models.run.Run` instance in which this
    #: input was included.
    run = models.ForeignKey(
        "django_analyses.Run",
        on_delete=models.CASCADE,
        related_name="base_input_set",
    )

    #: The *value* field is meant to be overriden by subclasses according to
    #: the type of data provided as input.
    value = None

    #: The *definition* class attribute is meant to be overriden by subclasses
    #: and reference the appropriate
    #: :class:`~django_analyses.models.input.definition.input_definition.InputDefinition`
    #: subclass.
    #:
    # flake8: noqa: E501
    definition = None

    objects = InheritanceManager()

    class Meta:
        ordering = ("run",)

    def __str__(self) -> str:
        """
        Returns the string representation of this instance.

        Returns
        -------
        str
            String representation
        """

        return f"'{self.key}' = {self.value}"

    def raise_required_error(self):
        """
        Raises ValidationError to indicate this input is required.

        Raises
        ------
        ValidationError
            Required input not provided
        """

        raise ValidationError(f"{self.key} is required!")

    def pre_save(self) -> None:
        """
        If this input class's :attr:`value` is a
        :class:`~django.db.models.ForeignKey` field, fix it in cases it is
        provided as :obj:`int` (the instance's primary key).

        Note
        ----
        This method may be overridden by subclasses to implement custom
        functionality before saving. However, be sure to include:

        .. code-block:: python

            super().pre_save()

        within your custom function.

        """

        if self.value_is_foreign_key and isinstance(self.value, int):
            self.value = self.value.related_model.get(id=self.value)

    def validate(self) -> None:
        """
        Run any custom validations before saving the model.

        Note
        ----
        This method may be overridden by subclasses to implement custom
        functionality before saving. However, be sure to include:

        .. code-block:: python

            super().pre_save()

        within your custom function.
        """

        if self.definition.required and self.value is None:
            self.raise_required_error()

    def save(self, *args, **kwargs):
        """
        Overrides the model's :meth:`~django.db.models.Model.save` method to
        provide custom functionality.

        Hint
        ----
        For more information, see Django's documentation on `overriding model
        methods`_.

        .. _overriding model methods:
           https://docs.djangoproject.com/en/3.0/topics/db/models/#overriding-model-methods
        """

        self.pre_save()
        self.validate()
        super().save(*args, **kwargs)

    def get_argument_value(self) -> Any:
        """
        Returns the input's *value* after applying any manipulations specified
        by the associated :attr:`definition`.
        This method is used to bridge database-compatible values with
        non-database-compatible values required by interfaces.

        Returns
        -------
        Any
            Input value as expected by the interface
        """

        value = self.value
        if self.definition.value_attribute:
            location = self.definition.value_attribute
            return self.definition.extract_nested_value(value, location)
        return value

    @property
    def key(self) -> str:
        """
        Returns the *key* of the associated :attr:`definition`.

        Returns
        -------
        str
            Input definition key
        """

        if self.definition:
            return self.definition.key

    @property
    def argument_value(self) -> Any:
        """
        Returns the value of the input as expected by the interface.

        Returns
        -------
        Any
            Input value as expected by the interface
        """

        return self.get_argument_value()

    @property
    def value_is_foreign_key(self) -> bool:
        """
        Checks whether the :attr:`value` attribute is a
        :class:`~django.db.models.ForeignKey` field.

        Returns
        -------
        bool
            :attr:`value` is foreign key or not
        """

        value_field = self._meta.get_field("value")
        return isinstance(value_field, models.ForeignKey)
