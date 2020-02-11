from django.core.exceptions import ValidationError
from django.test import TestCase
from django_analyses.models.input.types.input_types import InputTypes
from tests.factories.input.types.file_input import FileInputFactory


class FileInputTestCase(TestCase):
    """
    Tests for the :class:`~django_analyses.models.input.types.file_input.FileInput` model.

    """

    def setUp(self):
        """
        Adds the created instances to the tests' contexts.
        For more information see unittest's :meth:`~unittest.TestCase.setUp` method.

        """

        self.file_input = FileInputFactory()

    ###########
    # Methods #
    ###########

    def test_string(self):
        value = str(self.file_input)
        expected = f"'{self.file_input.key}' = {self.file_input.value}"
        self.assertEqual(value, expected)

    def test_none_value_if_required_raises_validation_error(self):
        self.file_input.definition.required = True
        self.file_input.definition.save()
        self.file_input.value = None
        with self.assertRaises(ValidationError):
            self.file_input.save()

    def test_get_type(self):
        value = self.file_input.get_type()
        self.assertEqual(value, InputTypes.FIL)
