from django.test import TestCase
from django_analyses.models.input.definitions.file_input_definition import (
    FileInputDefinition,
)
from django_analyses.models.input.definitions.input_definitions import InputDefinitions
from django_analyses.models.input.types.file_input import FileInput
from tests.factories.input.definitions.file_input_definition import (
    FileInputDefinitionFactory,
)


class FileInputDefinitionTestCase(TestCase):
    """
    Tests for the
    :class:`~django_analyses.models.input.definitions.file_input_definition.FileInputDefinition`
    model.
    
    """

    def setUp(self):
        """
        Adds the created instances to the tests' contexts.
        For more information see unittest's :meth:`~unittest.TestCase.setUp` method.

        """

        self.file_input_definition = FileInputDefinitionFactory()

    ##########
    #  Meta  #
    ##########

    def test_input_class_attribute(self):
        """
        Test the `input_class` attribute is set to
        :class:`~django_analyses.models.input.types.file_input.FileInput`.

        """

        self.assertEqual(FileInputDefinition.input_class, FileInput)

    def test_default_is_none(self):
        """
        The
        :class:`~django_analyses.models.input.definitions.file_input_definition.FileInputDefinition`
        does not currently support a default value definition and therefore is
        expected to be None.
        
        """

        FileInputDefinition.default = None

    ##########
    # Fields #
    ##########

    ###########
    # Methods #
    ###########

    def test_get_type(self):
        """
        Tests the
        :meth:`~django_analyses.models.input.definitions.file_input_definition.FileInputDefinition.get_type`
        method returns the expected value.

        """

        value = self.file_input_definition.get_type()
        self.assertEqual(value, InputDefinitions.FIL)
