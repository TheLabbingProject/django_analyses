from django.test import TestCase
from django_analyses.models.input.types.string_input import StringInput
from django_analyses.models.input.definitions.input_definitions import InputDefinitions
from tests.factories.input.definitions.string_input_definition import (
    StringInputDefinitionFactory,
)


class StringInputDefinitionTestCase(TestCase):
    """
    Tests for the
    :class:`~django_analyses.models.input.definitions.string_input_definition.StringInputDefinition`
    model.
    
    """

    def setUp(self):
        """
        Adds the created instances to the tests' contexts.
        For more information see unittest's :meth:`~unittest.TestCase.setUp` method.

        """

        self.string_input_definition = StringInputDefinitionFactory()

    ##########
    #  Meta  #
    ##########

    def test_input_class_attribute(self):
        """
        Test the `input_class` attribute is set to
        :class:`~django_analyses.models.input.types.string_input.StringInput`

        """

        self.assertEqual(self.string_input_definition.input_class, StringInput)

    ##########
    # Fields #
    ##########

    def test_default_blank_and_null(self):
        """
        Tests that the *default* field may be blank or null.

        """

        field = self.string_input_definition._meta.get_field("default")
        self.assertTrue(field.blank)
        self.assertTrue(field.null)

    ###########
    # Methods #
    ###########

    def test_get_type(self):
        """
        Tests the
        :meth:`~django_analyses.models.input.definitions.string_input_definition.StringInputDefinition.get_type`
        return the expected value.

        """

        value = self.string_input_definition.get_type()
        self.assertEqual(value, InputDefinitions.STR)
