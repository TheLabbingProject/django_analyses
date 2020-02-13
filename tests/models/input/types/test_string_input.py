from django.conf import settings
from django.core.exceptions import ValidationError
from django.test import TestCase
from django_analyses.models.input.types.input_types import InputTypes
from pathlib import Path
from tests.factories.input.definitions.string_input_definition import (
    StringInputDefinitionFactory,
)
from tests.factories.input.types.string_input import StringInputFactory


class StringInputTestCase(TestCase):
    """
    Tests for the :class:`~django_analyses.models.input.types.string_input.StringInput` model.

    """

    def setUp(self):
        """
        Adds the created instances to the tests' contexts.
        For more information see unittest's :meth:`~unittest.TestCase.setUp` method.

        """

        self.string_input_definition = StringInputDefinitionFactory(
            min_length=5, max_length=40
        )
        self.string_input = StringInputFactory(definition=self.string_input_definition)

    ###########
    # Methods #
    ###########

    def test_string(self):
        value = str(self.string_input)
        expected = f"'{self.string_input.key}' = {self.string_input.value}"
        self.assertEqual(value, expected)

    def test_none_value_if_required_raises_validation_error(self):
        self.string_input.definition.required = True
        self.string_input.definition.default = None
        self.string_input.definition.save()
        self.string_input.value = None
        with self.assertRaises(ValidationError):
            self.string_input.save()

    def test_get_type(self):
        value = self.string_input.get_type()
        self.assertEqual(value, InputTypes.STR)

    def test_validate_min_length_raises_validation_error(self):
        self.string_input.value = "a"
        with self.assertRaises(ValidationError):
            self.string_input.save()

    def test_validate_max_length_raises_validation_error(self):
        self.string_input.value = "a" * 41
        with self.assertRaises(ValidationError):
            self.string_input.save()

    def test_invalid_choice_raises_validation_error(self):
        choices = ["AAA", "BBB", "CCC"]
        definition = StringInputDefinitionFactory(
            min_length=3, max_length=3, choices=choices, default="AAA"
        )
        with self.assertRaises(ValidationError):
            StringInputFactory(definition=definition, value="DDD")

    def test_fix_output_path_with_empty_value_and_definition_default(self):
        definition = StringInputDefinitionFactory(
            is_output_path=True, min_length=0, max_length=500
        )
        string_input = StringInputFactory(definition=definition, value="")
        expected = str(
            string_input.default_output_directory / string_input.definition.default
        )
        self.assertEqual(string_input.value, expected)

    def test_fix_output_path_with_empty_value_and_no_definition_default(self):
        definition = StringInputDefinitionFactory(
            is_output_path=True, max_length=500, default=""
        )
        string_input = StringInputFactory(definition=definition, value="")
        expected = str(
            string_input.default_output_directory / string_input.definition.key
        )
        self.assertEqual(string_input.value, expected)

    def test_fix_output_path_with_absolute_path_value(self):
        definition = StringInputDefinitionFactory(is_output_path=True, max_length=500)
        value = "/some/absolute/file/path"
        string_input = StringInputFactory(definition=definition, value=value)
        self.assertEqual(string_input.value, value)

    def test_fix_output_path_with_non_absolute_path_value(self):
        definition = StringInputDefinitionFactory(is_output_path=True, max_length=500)
        string_input = StringInputFactory(
            definition=definition, value="some/relative/file/path"
        )
        expected = str(string_input.default_output_directory / string_input.value)
        self.assertEqual(string_input.value, expected)

    ##############
    # Properties #
    ##############

    def test_default_output_directory(self):
        value = self.string_input.default_output_directory
        expected = Path(settings.ANALYSIS_BASE_PATH) / str(self.string_input.run.id)
        self.assertEqual(value, expected)
