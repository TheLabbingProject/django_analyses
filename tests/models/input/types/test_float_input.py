from django.core.exceptions import ValidationError
from django.test import TestCase
from django_analyses.models.input.types.input_types import InputTypes
from tests.factories.input.definitions.float_input_definition import (
    FloatInputDefinitionFactory,
)
from tests.factories.input.types.float_input import FloatInputFactory


class FloatInputTestCase(TestCase):
    """
    Tests for the :class:`~django_analyses.models.input.types.float_input.FloatInput` model.

    """

    def setUp(self):
        """
        Adds the created instances to the tests' contexts.
        For more information see unittest's :meth:`~unittest.TestCase.setUp` method.

        """

        self.float_input_definition = FloatInputDefinitionFactory(
            min_value=-1000, max_value=1000
        )
        self.float_input = FloatInputFactory(definition=self.float_input_definition)

    ###########
    # Methods #
    ###########

    def test_string(self):
        value = str(self.float_input)
        expected = f"'{self.float_input.key}' = {self.float_input.value}"
        self.assertEqual(value, expected)

    def test_none_value_if_required_raises_validation_error(self):
        self.float_input.definition.required = True
        self.float_input.definition.save()
        self.float_input.value = None
        with self.assertRaises(ValidationError):
            self.float_input.save()

    def test_get_type(self):
        value = self.float_input.get_type()
        self.assertEqual(value, InputTypes.FLT)

    def test_validate_min_value_raises_validation_error(self):
        self.float_input.value = -1000.01
        with self.assertRaises(ValidationError):
            self.float_input.save()

    def test_validate_max_value_raises_validation_error(self):
        self.float_input.value = 1000.01
        with self.assertRaises(ValidationError):
            self.float_input.save()
