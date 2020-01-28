from django.db.models import QuerySet
from django.test import TestCase
from django_analyses.models.output.definitions.file_output_definition import (
    FileOutputDefinition,
)

from tests.factories.output.output_specification import OutputSpecificationFactory


class OutputSpecificationTestCase(TestCase):
    """
    Tests for the
    :class:`~django_analyses.models.output.output_specification.OutputSpecification`
    model.
    
    """

    def setUp(self):
        """
        Adds the created instances to the tests' contexts.
        For more information see unittest's :meth:`~unittest.TestCase.setUp` method.

        """

        self.output_specification = OutputSpecificationFactory()

    ##########
    #  Meta  #
    ##########

    ###########
    # Methods #
    ###########

    # __str__
    def test_string(self):
        self.assertIsInstance(self.output_specification.__str__(), str)

    ##############
    # Properties #
    ##############

    # output_definitions
    def test_output_definitions_property_return_type(self):
        value = self.output_specification.output_definitions
        self.assertIsInstance(value, QuerySet)

    def test_output_definitions_property_returns_subclasses(self):
        value = self.output_specification.output_definitions
        subclasses = [type(definition) for definition in value]
        self.assertIn(FileOutputDefinition, subclasses)
