from django.core.exceptions import ValidationError
from django.test import TestCase
from django_analyses.models.output.definitions.output_definition import OutputDefinition
from django_analyses.models.output.types.file_output import FileOutput
from django_analyses.models.managers.output_definition import OutputDefinitionManager
from django_analyses.models.input.definitions.file_input_definition import (
    FileInputDefinition,
)
from tests.factories.output.definitions.output_definition import OutputDefinitionFactory


class OutputDefinitionTestCase(TestCase):
    """
    Tests for the
    :class:`~django_analyses.models.output.definitions.output_definition.OutputDefinition`
    model.

    """

    def setUp(self):
        """
        Adds the created instances to the tests' contexts.
        For more information see unittest's :meth:`~unittest.TestCase.setUp` method.

        """

        self.output_definition = OutputDefinitionFactory()

    ##########
    #  Meta  #
    ##########

    def test_ordering(self):
        """
        Test the `ordering`.

        """

        self.assertTupleEqual(OutputDefinition._meta.ordering, ("key",))

    def test_output_class_is_none(self):
        """
        Tests that the *output_class* class attribute is set to None. This is
        meant to be overriden by a
        :class:`~django_analyses.models.output.output.Output` instance.

        """

        self.assertIsNone(OutputDefinition.output_class)

    def test_custom_manager_is_assigned(self):
        """
        Tests that the manager is assigned to be the custom
        :class:`~django_analyses.models.managers.output_definition.OutputDefinitionManager`
        class.

        """

        self.assertIsInstance(OutputDefinition.objects, OutputDefinitionManager)

    ##########
    # Fields #
    ##########

    # key
    def test_key_max_length(self):
        """
        Test the max_length of the *key* field.

        """

        field = self.output_definition._meta.get_field("key")
        self.assertEqual(field.max_length, 50)

    def test_key_is_not_unique(self):
        """
        Tests that the *key* field is not unique.

        """

        field = self.output_definition._meta.get_field("key")
        self.assertFalse(field.unique)

    def test_key_blank_and_null(self):
        """
        Tests that the *key* field may not be blank or null.

        """

        field = self.output_definition._meta.get_field("key")
        self.assertFalse(field.blank)
        self.assertFalse(field.null)

    # description
    def test_description_blank_and_null(self):
        """
        Tests that the *description* field may be blank or null.

        """

        field = self.output_definition._meta.get_field("description")
        self.assertTrue(field.blank)
        self.assertTrue(field.null)

    ###########
    # Methods #
    ###########

    def test_string(self):
        """
        Test the string output.

        """

        value = str(self.output_definition)
        expected = self.output_definition.key
        self.assertEqual(value, expected)

    def test_create_output_instance_raises_type_error(self):
        """
        Tests that calling the
        :meth:`~django_analyses.models.output.definitions.output_definition.OutputDefinition.create_output_instance`
        raises a ValidationError. This is the expected behavior as long as the
        output_class attribute is not defined (or ill defined).

        """

        with self.assertRaises(ValidationError):
            self.output_definition.create_output_instance()

    def test_create_output_instance_with_non_model_value_raises_type_error(self):
        """
        Tests that calling the
        :meth:`~django_analyses.models.output.definitions.output_definition.OutputDefinition.create_output_instance`
        with a non-model value raises a ValidationError.

        """

        self.output_definition.output_class = str
        with self.assertRaises(ValidationError):
            self.output_definition.create_output_instance()

    def test_create_output_instance_with_non_output_subclass_value_raises_type_error(
        self,
    ):
        """
        Tests that calling the
        :meth:`~django_analyses.models.output.definitions.output_definition.OutputDefinition.create_output_instance`
        with a non-:class:`~django_analyses.models.output.output.Output`
        model subclass value raises a ValidationError.

        """

        self.output_definition.output_class = FileInputDefinition
        with self.assertRaises(ValidationError):
            self.output_definition.check_output_class_definition()

    def test_resetting_output_class_to_valid_output_subclass(self):
        """
        Tests that the
        :meth:`~django_analyses.models.output.definitions.output_definition.OutputDefinition.check_output_class_definition`
        method does not raise a ValidationError when setting *output_class* to
        some valid Output model subclass.
        
        """

        self.output_definition.output_class = FileOutput
        try:
            self.output_definition.check_output_class_definition()
        except ValidationError:
            self.fail(
                "Failed to set output_definition output_class to a valid Output subclass!"
            )

    def test_create_output_instance_reraises_uncaught_exception(self):
        """
        Tests that calling the
        :meth:`~django_analyses.models.output.definitions.output_definition.OutputDefinition.create_output_instance`
        method when *output_class* is properly set but invalid kwargs still
        raises an exception.

        """

        self.output_definition.output_class = FileOutput
        with self.assertRaises(ValueError):
            self.output_definition.create_output_instance()
