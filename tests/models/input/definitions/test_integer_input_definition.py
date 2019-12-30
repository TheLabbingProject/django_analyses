from django.core.exceptions import ValidationError
from django.test import TestCase
from django_analyses.models.input.types.integer_input import IntegerInput
from django_analyses.models.input.definitions.input_definitions import InputDefinitions
from django_analyses.models.input.definitions.integer_input_definition import (
    IntegerInputDefinition,
)
from tests.factories.input.definitions.integer_input_definition import (
    IntegerInputDefinitionFactory,
)


class IntegerInputDefinitionTestCase(TestCase):
    """
    Tests for the
    :class:`~django_analyses.models.input.definitions.integer_input_definition.IntegerInputDefinition`
    model.
    
    """

    def setUp(self):
        """
        Adds the created instances to the tests' contexts.
        For more information see unittest's :meth:`~unittest.TestCase.setUp` method.

        """

        self.integer_input_definition = IntegerInputDefinitionFactory()

    ##########
    #  Meta  #
    ##########

    def test_input_class_attribute(self):
        """
        Test the `input_class` attribute is set to
        :class:`~django_analyses.models.input.types.integer_input.IntegerInput`

        """

        self.assertEqual(IntegerInputDefinition.input_class, IntegerInput)

    ##########
    # Fields #
    ##########

    def test_default_blank_and_null(self):
        """
        Tests that the *default* field may be blank or null.

        """

        field = self.integer_input_definition._meta.get_field("default")
        self.assertTrue(field.blank)
        self.assertTrue(field.null)

    def test_min_value_blank_and_null(self):
        """
        Tests that the *min_value* field may be blank or null.

        """

        field = self.integer_input_definition._meta.get_field("min_value")
        self.assertTrue(field.blank)
        self.assertTrue(field.null)

    def test_max_value_blank_and_null(self):
        """
        Tests that the *max_value* field may be blank or null.

        """

        field = self.integer_input_definition._meta.get_field("max_value")
        self.assertTrue(field.blank)
        self.assertTrue(field.null)

    ###########
    # Methods #
    ###########

    def test_get_type(self):
        """
        Tests the
        :meth:`~django_analyses.models.input.definitions.integer_input_definition.IntegerInputDefinition.get_type`
        method returns the expected value.

        """

        value = self.integer_input_definition.get_type()
        self.assertEqual(value, InputDefinitions.INT)

    def test_min_value_validation(self):
        """
        Tests that a ValidationError is raised if the default value is
        lesser than the `min_value` definition.

        """

        invalid_value = self.integer_input_definition.min_value - 1
        self.integer_input_definition.default = invalid_value
        with self.assertRaises(ValidationError):
            self.integer_input_definition.save()

    def test_max_value_validation(self):
        """
        Tests that a ValidationError is raised if the default value is
        greater than the `max_value` definition.

        """

        invalid_value = self.integer_input_definition.max_value + 1
        self.integer_input_definition.default = invalid_value
        with self.assertRaises(ValidationError):
            self.integer_input_definition.save()

    def test_default_may_be_nulled(self):
        """
        Tests that the *default* field may be set to null without raising
        a ValidationError or any other exception.
        
        """

        self.integer_input_definition.default = None
        try:
            self.integer_input_definition.save()
        except Exception:
            self.fail("Failed to set default value to null!")

    def test_min_value_may_be_nulled(self):
        """
        Tests that the *min_value* field may be set to null without raising
        a ValidationError or any other exception.
        
        """

        self.integer_input_definition.min_value = None
        try:
            self.integer_input_definition.save()
        except Exception:
            self.fail("Failed to set min_value to null!")

    def test_max_value_may_be_nulled(self):
        """
        Tests that the *max_value* field may be set to null without raising
        a ValidationError or any other exception.
        
        """

        self.integer_input_definition.max_value = None
        try:
            self.integer_input_definition.save()
        except Exception:
            self.fail("Failed to set min_value to null!")
