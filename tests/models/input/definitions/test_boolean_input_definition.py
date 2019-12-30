from django.test import TestCase
from django_analyses.models.input.types.boolean_input import BooleanInput
from django_analyses.models.input.definitions.boolean_input_definition import (
    BooleanInputDefinition,
)
from django_analyses.models.input.definitions.input_definitions import InputDefinitions
from tests.factories.input.definitions.boolean_input_definition import (
    BooleanInputDefinitionFactory,
)


class BooleanInputDefinitionTestCase(TestCase):
    """
    Tests for the
    :class:`~django_analyses.models.input.definitions.boolean_input_definition.BooleanInputDefinition`
    model.
    
    """

    def setUp(self):
        """
        Adds the created instances to the tests' contexts.
        For more information see unittest's :meth:`~unittest.TestCase.setUp` method.

        """

        self.boolean_input_definition = BooleanInputDefinitionFactory()

    ##########
    #  Meta  #
    ##########

    def test_input_class_attribute(self):
        """
        Test the `input_class` attribute is set to
        :class:`~django_analyses.models.input.types.boolean_input.BooleanInput`

        """

        self.assertEqual(BooleanInputDefinition.input_class, BooleanInput)

    ##########
    # Fields #
    ##########

    def test_default_blank_and_null(self):
        """
        Tests that the *default* field may be blank or null.

        """

        field = self.boolean_input_definition._meta.get_field("default")
        self.assertTrue(field.blank)
        self.assertTrue(field.null)

    ###########
    # Methods #
    ###########

    def test_get_type(self):
        """
        Tests the
        :meth:`~django_analyses.models.input.definitions.boolean_input_definition.BooleanInputDefinition.get_type`
        return the expected value.

        """

        value = self.boolean_input_definition.get_type()
        self.assertEqual(value, InputDefinitions.BLN)
