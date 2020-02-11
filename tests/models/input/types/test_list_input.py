from django.core.exceptions import ValidationError
from django.test import TestCase
from django_analyses.models.input.types.input_types import InputTypes
from django_analyses.models.input.utils import ListElementTypes
from tests.factories.input.definitions.list_input_definition import (
    ListInputDefinitionFactory,
)
from tests.factories.input.types.list_input import ListInputFactory


class ListInputTestCase(TestCase):
    """
    Tests for the :class:`~django_analyses.models.input.types.list_input.ListInput` model.

    """

    def setUp(self):
        """
        Adds the created instances to the tests' contexts.
        For more information see unittest's :meth:`~unittest.TestCase.setUp` method.

        """

        self.list_input_definition = ListInputDefinitionFactory(
            min_length=2, max_length=5, element_type=ListElementTypes.INT.name,
        )
        self.list_input = ListInputFactory(
            definition=self.list_input_definition, value=[1, 2, 3, 4],
        )

    ###########
    # Methods #
    ###########

    def test_string(self):
        value = str(self.list_input)
        expected = f"'{self.list_input.key}' = {self.list_input.value}"
        self.assertEqual(value, expected)

    def test_none_value_if_required_raises_validation_error(self):
        self.list_input.definition.required = True
        self.list_input.definition.save()
        self.list_input.value = None
        with self.assertRaises(ValidationError):
            self.list_input.save()

    def test_get_type(self):
        value = self.list_input.get_type()
        self.assertEqual(value, InputTypes.LST)

    def test_min_length_raises_validation_error(self):
        self.list_input.value = [0]
        with self.assertRaises(ValidationError):
            self.list_input.save()

    def test_max_length_raises_validation_error(self):
        self.list_input.value += [5, 6]
        with self.assertRaises(ValidationError):
            self.list_input.save()

    def test_non_list_values_raise_validation_error(self):
        self.list_input.value = 0
        with self.assertRaises(ValidationError):
            self.list_input.save()
        self.list_input.value = 0.4
        with self.assertRaises(ValidationError):
            self.list_input.save()
        self.list_input.value = "a"
        with self.assertRaises(ValidationError):
            self.list_input.save()
        self.list_input.value = False
        with self.assertRaises(ValidationError):
            self.list_input.save()
        self.list_input.value = True
        with self.assertRaises(ValidationError):
            self.list_input.save()

    def test_wrong_type_elements_raise_validation_error(self):
        self.list_input.value = ["a", "b", "c"]
        with self.assertRaises(ValidationError):
            self.list_input.save()
        self.list_input.value = [0, 1, "c"]
        with self.assertRaises(ValidationError):
            self.list_input.save()
        self.list_input.value = [True, 0, 1]
        with self.assertRaises(ValidationError):
            self.list_input.save()
        self.list_input.value = [False, 0, 1]
        with self.assertRaises(ValidationError):
            self.list_input.save()
        self.list_input.value = [0, 1, 1.1]
        with self.assertRaises(ValidationError):
            self.list_input.save()
        self.list_input.value = [0, 1, []]
        with self.assertRaises(ValidationError):
            self.list_input.save()
        self.list_input.value = [0, {}, 1]
        with self.assertRaises(ValidationError):
            self.list_input.save()
