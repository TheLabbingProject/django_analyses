"""
Definition of the :class:`StringInputDefinition` class.
"""
from django.contrib.postgres.fields import ArrayField
from django.core.exceptions import ValidationError
from django.db import models
from django.utils.translation import gettext_lazy as _
from django_analyses.models.input.definitions.input_definition import (
    InputDefinition,
)
from django_analyses.models.input.types.string_input import StringInput
from django_analyses.models.input.definitions.input_definitions import (
    InputDefinitions,
)


class StringInputDefinition(InputDefinition):
    """
    Represents a single string input definition in the database.
    """

    #: Minimal string length.
    min_length = models.IntegerField(blank=True, null=True)

    #: Maximal string length.
    max_length = models.IntegerField(blank=True, null=True)

    #: Default value.
    default = models.CharField(max_length=500, blank=True, null=True)

    #: Dynamic default value expressed as some formatting template which
    #: requires run-dependent information.
    dynamic_default = models.CharField(max_length=500, blank=True, null=True)

    #: Possible choices for the string input value.
    choices = ArrayField(
        models.CharField(max_length=255, blank=True, null=True),
        blank=True,
        null=True,
    )

    #: Whether this string determines the output path of the analysis.
    is_output_path = models.BooleanField(default=False)

    #: Whether this string determines if some output will be generated or not.
    is_output_switch = models.BooleanField(default=False)

    input_class = StringInput

    def validate(self) -> None:
        """
        Overrides
        :func:`django_analyses.models.input.definitions.input_definition.InputDefinition.validate`
        to validate choices (in cases where :attr:`choices` is defined).

        Raises
        ------
        ValidationError
            Invalid choice
        """

        if self.default and self.choices:
            if self.default not in self.choices:
                raise ValidationError(
                    _(f"{self.default} not in {self.choices}!")
                )

    def get_type(self) -> InputDefinitions:
        return InputDefinitions.STR
