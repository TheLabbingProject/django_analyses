from django.core.exceptions import ValidationError
from django.test import TestCase
from django_analyses.models.input.types.string_input import StringInput
from django_analyses.models.input.definitions.input_definitions import InputDefinitions
from django_analyses.models.input.definitions.string_input_definition import (
    StringInputDefinition,
)
from tests.factories.input.definitions.string_input_definition import (
    StringInputDefinitionFactory,
)


class StringInputDefinitionTestCase(TestCase):
    """
    Tests for the
    :class:`~django_analyses.models.input.definitions.string_input_definition.StringInputDefinition`
    model.
    
    """

    def setUp(self):
        """
        Adds the created instances to the tests' contexts.
        For more information see unittest's :meth:`~unittest.TestCase.setUp` method.

        """

        self.string_input_definition = StringInputDefinitionFactory()

    ##########
    #  Meta  #
    ##########

    def test_input_class_attribute(self):
        """
        Test the `input_class` attribute is set to
        :class:`~django_analyses.models.input.types.string_input.StringInput`

        """

        self.assertEqual(StringInputDefinition.input_class, StringInput)

    ##########
    # Fields #
    ##########

    def test_default_blank_and_null(self):
        """
        Tests that the *default* field may be blank or null.

        """

        field = self.string_input_definition._meta.get_field("default")
        self.assertTrue(field.blank)
        self.assertTrue(field.null)

    def test_default_max_length(self):
        """
        Tests the *default* field's max_length value.

        """

        field = self.string_input_definition._meta.get_field("default")
        self.assertEqual(field.max_length, 500)

    def test_min_length_blank_and_null(self):
        """
        Tests that the *min_length* field may be blank or null.

        """

        field = self.string_input_definition._meta.get_field("min_length")
        self.assertTrue(field.blank)
        self.assertTrue(field.null)

    def test_max_length_blank_and_null(self):
        """
        Tests that the *max_length* field may be blank or null.

        """

        field = self.string_input_definition._meta.get_field("max_length")
        self.assertTrue(field.blank)
        self.assertTrue(field.null)

    def test_choices_blank_and_null(self):
        """
        Tests that the *choices* field may be blank or null.

        """

        field = self.string_input_definition._meta.get_field("choices")
        self.assertTrue(field.blank)
        self.assertTrue(field.null)

    def test_is_output_path_blank_and_null(self):
        """
        Tests that the *is_output_path* field may be blank or null.

        """

        field = self.string_input_definition._meta.get_field("is_output_path")
        self.assertFalse(field.blank)
        self.assertFalse(field.null)

    def test_is_output_path_default_value(self):
        """
        Tests the *is_output_path* field's default value.

        """

        field = self.string_input_definition._meta.get_field("is_output_path")
        self.assertFalse(field.default)

    ###########
    # Methods #
    ###########

    def test_get_type(self):
        """
        Tests the
        :meth:`~django_analyses.models.input.definitions.string_input_definition.StringInputDefinition.get_type`
        method returns the expected value.

        """

        value = self.string_input_definition.get_type()
        self.assertEqual(value, InputDefinitions.STR)

    def test_validation_without_default_and_without_choices(self):
        """
        Tests the
        :meth:`~django_analyses.models.input.definitions.string_input_definition.StringInputDefinition.validate`
        methods does not raise a ValidationError if the `choices` and
        `default` fields are null.

        """

        self.string_input_definition.default = None
        self.assertIsNone(self.string_input_definition.validate())

    def test_validation_with_default_and_without_choices(self):
        """
        Tests the
        :meth:`~django_analyses.models.input.definitions.string_input_definition.StringInputDefinition.validate`
        methods does not raise a ValidationError if the `choices` field
        is null when `default` is set.

        """

        self.assertIsNotNone(self.string_input_definition.default)
        self.assertIsNone(self.string_input_definition.validate())

    def test_validation_with_default_from_choices(self):
        """
        Tests the
        :meth:`~django_analyses.models.input.definitions.string_input_definition.StringInputDefinition.validate`
        methods does not raise a ValidationError if the `choices` field
        is set and contains the `default` value.

        """

        choices = ["a", "b", "c"]
        choices.append(self.string_input_definition.default)
        self.string_input_definition.choices = choices
        self.assertIsNone(self.string_input_definition.validate())

    def test_validation_with_default_not_from_choices(self):
        """
        Tests the
        :meth:`~django_analyses.models.input.definitions.string_input_definition.StringInputDefinition.validate`
        methods raises a ValidationError if the `choices` field is set
        and does not contains the `default` value.

        """

        choices = ["a", "b", "c"]
        self.string_input_definition.choices = choices
        with self.assertRaises(ValidationError):
            self.string_input_definition.validate()
