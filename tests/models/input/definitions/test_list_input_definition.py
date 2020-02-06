from django.core.exceptions import ValidationError
from django.test import TestCase
from django_analyses.models.input.types.list_input import ListInput
from django_analyses.models.input.definitions.input_definitions import InputDefinitions
from django_analyses.models.input.definitions.list_input_definition import (
    ListInputDefinition,
)
from tests.factories.input.definitions.list_input_definition import (
    ListInputDefinitionFactory,
)


class ListInputDefinitionTestCase(TestCase):
    """
    Tests for the
    :class:`~django_analyses.models.input.definitions.list_input_definition.ListInputDefinition`
    model.
    
    """

    def setUp(self):
        """
        Adds the created instances to the tests' contexts.
        For more information see unittest's :meth:`~unittest.TestCase.setUp` method.

        """

        self.list_input_definition = ListInputDefinitionFactory()
        self.list_input_definition.element_type = "INT"
        self.list_input_definition.save()

    ##########
    #  Meta  #
    ##########

    def test_input_class_attribute(self):
        """
        Test the `input_class` attribute is set to
        :class:`~django_analyses.models.input.types.list_input.ListInput`

        """

        self.assertEqual(ListInputDefinition.input_class, ListInput)

    ##########
    # Fields #
    ##########

    def test_default_blank_and_null(self):
        """
        Tests that the *default* field may be blank or null.

        """

        field = self.list_input_definition._meta.get_field("default")
        self.assertTrue(field.blank)
        self.assertTrue(field.null)

    def test_min_length_blank_and_null(self):
        """
        Tests that the *min_length* field may be blank or null.

        """

        field = self.list_input_definition._meta.get_field("min_length")
        self.assertTrue(field.blank)
        self.assertTrue(field.null)

    def test_max_length_blank_and_null(self):
        """
        Tests that the *max_length* field may be blank or null.

        """

        field = self.list_input_definition._meta.get_field("max_length")
        self.assertTrue(field.blank)
        self.assertTrue(field.null)

    ###########
    # Methods #
    ###########

    def test_get_type(self):
        """
        Tests the
        :meth:`~django_analyses.models.input.definitions.list_input_definition.ListInputDefinition.get_type`
        method returns the expected length.

        """

        length = self.list_input_definition.get_type()
        self.assertEqual(length, InputDefinitions.LST)

    def test_min_length_validation(self):
        """
        Tests that a ValidationError is raised if the default's length is
        lesser than the `min_length` definition.

        """

        self.list_input_definition.default = [1]
        with self.assertRaises(ValidationError):
            self.list_input_definition.save()

    def test_max_length_validation(self):
        """
        Tests that a ValidationError is raised if the default's length is
        greater than the `max_length` definition.

        """

        self.list_input_definition.default = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
        with self.assertRaises(ValidationError):
            self.list_input_definition.save()

    def test_resetting_default_to_valid_value(self):
        """
        Tests that setting the default value to a different value that is
        valid does not raise a ValidationError.

        """

        self.list_input_definition.default = [0, 0, 0, 0, 0]
        try:
            self.list_input_definition.save()
        except Exception:
            self.fail("Failed to set default value to a different valid value!")

    def test_wrong_element_type_raises_validation_error(self):
        """
        Tests that a ValidationError is raised if the default's element
        type does not match the *element_type* field value.

        """

        # String
        self.list_input_definition.default = ["c", 0, 1]
        with self.assertRaises(ValidationError):
            self.list_input_definition.save()
        # Float
        self.list_input_definition.default = [0, 2.2, 1]
        with self.assertRaises(ValidationError):
            self.list_input_definition.save()
        # Boolean
        self.list_input_definition.default = [0, 1, True]
        with self.assertRaises(ValidationError):
            self.list_input_definition.save()

    def test_setting_default_to_non_list_raises_validation_error(self):
        """
        Tests that setting the default value to a non-list value raises
        a validation error.

        """

        # Integer
        self.list_input_definition.default = 5
        with self.assertRaises(ValidationError):
            self.list_input_definition.save()
        # String
        self.list_input_definition.default = "a"
        with self.assertRaises(ValidationError):
            self.list_input_definition.save()
        # Float
        self.list_input_definition.default = 2.2
        with self.assertRaises(ValidationError):
            self.list_input_definition.save()
        # Boolean
        self.list_input_definition.default = False
        with self.assertRaises(ValidationError):
            self.list_input_definition.save()

