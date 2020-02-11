from django.core.exceptions import ValidationError
from django.test import TestCase
from django_analyses.models.input.types.input_types import InputTypes
from tests.factories.input.definitions.integer_input_definition import (
    IntegerInputDefinitionFactory,
)
from tests.factories.input.types.integer_input import IntegerInputFactory


class IntegerInputTestCase(TestCase):
    """
    Tests for the :class:`~django_analyses.models.input.types.integer_input.IntegerInput` model.

    """

    def setUp(self):
        """
        Adds the created instances to the tests' contexts.
        For more information see unittest's :meth:`~unittest.TestCase.setUp` method.

        """

        self.integer_input_definition = IntegerInputDefinitionFactory(
            min_value=-100, max_value=100
        )
        self.integer_input = IntegerInputFactory(
            definition=self.integer_input_definition
        )

    ###########
    # Methods #
    ###########

    def test_string(self):
        value = str(self.integer_input)
        expected = f"'{self.integer_input.key}' = {self.integer_input.value}"
        self.assertEqual(value, expected)

    def test_none_value_if_required_raises_validation_error(self):
        self.integer_input.definition.required = True
        self.integer_input.definition.save()
        self.integer_input.value = None
        with self.assertRaises(ValidationError):
            self.integer_input.save()

    def test_get_type(self):
        value = self.integer_input.get_type()
        self.assertEqual(value, InputTypes.INT)

    def test_validate_min_value_raises_validation_error(self):
        self.integer_input.value = -101
        with self.assertRaises(ValidationError):
            self.integer_input.save()

    def test_validate_max_value_raises_validation_error(self):
        self.integer_input.value = 101
        with self.assertRaises(ValidationError):
            self.integer_input.save()
