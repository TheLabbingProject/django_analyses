from django.test import TestCase
from django_analyses.models.output.definitions.file_output_definition import (
    FileOutputDefinition,
)
from django_analyses.models.output.definitions.output_definitions import (
    OutputDefinitions,
)
from django_analyses.models.output.types.file_output import FileOutput
from tests.factories.output.definitions.file_output_definition import (
    FileOutputDefinitionFactory,
)


class FileOutputDefinitionTestCase(TestCase):
    """
    Tests for the
    :class:`~django_analyses.models.output.definitions.file_output_definition.FileOutputDefinition`
    model.
    
    """

    def setUp(self):
        """
        Adds the created instances to the tests' contexts.
        For more information see unittest's :meth:`~unittest.TestCase.setUp` method.

        """

        self.file_output_definition = FileOutputDefinitionFactory()

    ##########
    #  Meta  #
    ##########

    def test_output_class_attribute(self):
        """
        Test the `output_class` attribute is set to
        :class:`~django_analyses.models.output.types.file_output.FileOutput`.

        """

        self.assertEqual(FileOutputDefinition.output_class, FileOutput)

    ##########
    # Fields #
    ##########

    ###########
    # Methods #
    ###########

    def test_get_type(self):
        """
        Tests the
        :meth:`~django_analyses.models.output.definitions.file_output_definition.FileOutputDefinition.get_type`
        method returns the expected value.

        """

        value = self.file_output_definition.get_type()
        self.assertEqual(value, OutputDefinitions.FIL)
