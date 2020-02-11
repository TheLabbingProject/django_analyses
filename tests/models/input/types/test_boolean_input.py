from django.core.exceptions import ValidationError
from django.test import TestCase
from django_analyses.models.input.types.input_types import InputTypes
from tests.factories.input.types.boolean_input import BooleanInputFactory


class BooleanInputTestCase(TestCase):
    """
    Tests for the :class:`~django_analyses.models.input.types.boolean_input.BooleanInput` model.

    """

    def setUp(self):
        """
        Adds the created instances to the tests' contexts.
        For more information see unittest's :meth:`~unittest.TestCase.setUp` method.

        """

        self.boolean_input = BooleanInputFactory()

    ###########
    # Methods #
    ###########

    def test_string(self):
        value = str(self.boolean_input)
        expected = f"'{self.boolean_input.key}' = {self.boolean_input.value}"
        self.assertEqual(value, expected)

    def test_none_value_if_required_raises_validation_error(self):
        self.boolean_input.definition.required = True
        self.boolean_input.definition.save()
        self.boolean_input.value = None
        with self.assertRaises(ValidationError):
            self.boolean_input.save()

    def test_get_type(self):
        value = self.boolean_input.get_type()
        self.assertEqual(value, InputTypes.BLN)
