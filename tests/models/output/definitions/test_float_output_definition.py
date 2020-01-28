from django.test import TestCase
from django_analyses.models.output.definitions.float_output_definition import (
    FloatOutputDefinition,
)
from django_analyses.models.output.definitions.output_definitions import (
    OutputDefinitions,
)
from django_analyses.models.output.types.float_output import FloatOutput
from tests.factories.output.definitions.float_output_definition import (
    FloatOutputDefinitionFactory,
)


class FloatOutputDefinitionTestCase(TestCase):
    """
    Tests for the
    :class:`~django_analyses.models.output.definitions.float_output_definition.FloatOutputDefinition`
    model.
    
    """

    def setUp(self):
        """
        Adds the created instances to the tests' contexts.
        For more information see unittest's :meth:`~unittest.TestCase.setUp` method.

        """

        self.float_output_definition = FloatOutputDefinitionFactory()

    ##########
    #  Meta  #
    ##########

    def test_output_class_attribute(self):
        """
        Test the `output_class` attribute is set to
        :class:`~django_analyses.models.output.types.float_output.FloatOutput`.

        """

        self.assertEqual(FloatOutputDefinition.output_class, FloatOutput)

    ##########
    # Fields #
    ##########

    ###########
    # Methods #
    ###########

    def test_get_type(self):
        """
        Tests the
        :meth:`~django_analyses.models.output.definitions.float_output_definition.FloatOutputDefinition.get_type`
        method returns the expected value.

        """

        value = self.float_output_definition.get_type()
        self.assertEqual(value, OutputDefinitions.FLT)
