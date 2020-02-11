from django.test import TestCase
from django_analyses.models.output.types.output_types import OutputTypes
from tests.factories.output.definitions.file_output_definition import (
    FileOutputDefinitionFactory,
)
from tests.factories.output.types.file_output import FileOutputFactory


class FileOutputTestCase(TestCase):
    """
    Tests for the :class:`~django_analyses.models.output.types.file_output.FileOutput` model.

    """

    def setUp(self):
        """
        Adds the created instances to the tests' contexts.
        For more information see unittest's :meth:`~unittest.TestCase.setUp` method.

        """

        file_output_definition = FileOutputDefinitionFactory(validate_existence=False)
        self.file_output = FileOutputFactory(definition=file_output_definition)

    ###########
    # Methods #
    ###########

    def test_string(self):
        value = str(self.file_output)
        expected = f"'{self.file_output.key}' = {self.file_output.value}"
        self.assertEqual(value, expected)

    def test_get_type(self):
        value = self.file_output.get_type()
        self.assertEqual(value, OutputTypes.FIL)

    ##############
    # Properties #
    ##############

    def test_key(self):
        value = self.file_output.key
        expected = self.file_output.definition.key
        self.assertEqual(value, expected)
