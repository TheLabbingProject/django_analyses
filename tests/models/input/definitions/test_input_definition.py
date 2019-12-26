from django.test import TestCase
from django_analyses.models.managers.input_definition import InputDefinitionManager
from tests.factories.input.definitions.input_definition import InputDefinitionFactory


class BooleanInputDefinitionTestCase(TestCase):
    """
    Tests for the
    :class:`~django_analyses.models.input.definitions.input_definition.InputDefinition`
    model.
    
    """

    def setUp(self):
        """
        Adds the created instances to the tests' contexts.
        For more information see unittest's :meth:`~unittest.TestCase.setUp` method.

        """

        self.input_definition = InputDefinitionFactory()

    ##########
    #  Meta  #
    ##########

    def test_ordering(self):
        """
        Test the `ordering`_.

        """

        self.assertTupleEqual(self.input_definition._meta.ordering, ("key",))

    def test_input_class_is_none(self):
        """
        Tests that the *input_class* class attribute is set to None. This is
        meant to be overriden by a
        :class:`~django_analyses.models.input.input.Input` instance.        

        """

        self.assertIsNone(self.input_definition.input_class)

    def test_custom_manager_is_assigned(self):
        """
        Tests that the manager is assigned to be the custom
        :class:`~django_analyses.models.managers.input_definition.InputDefinitionManager`
        class.

        """

        model = type(self.input_definition)
        self.assertIsInstance(model.objects, InputDefinitionManager)

    ##########
    # Fields #
    ##########

    # key
    def test_key_max_length(self):
        """
        Test the max_length of the *key* field.
        
        """

        field = self.input_definition._meta.get_field("key")
        self.assertEqual(field.max_length, 50)

    def test_key_is_unique(self):
        """
        Tests that the *key* field is not unique.

        """

        field = self.input_definition._meta.get_field("key")
        self.assertFalse(field.unique)

    def test_key_blank_and_null(self):
        """
        Tests that the *key* field may not be blank or null.

        """

        field = self.input_definition._meta.get_field("key")
        self.assertFalse(field.blank)
        self.assertFalse(field.null)

    # required
    def test_required_default_value(self):
        """
        Test the default value of the *required* field.
        
        """

        field = self.input_definition._meta.get_field("required")
        self.assertFalse(field.default)

    # description
    def test_description_blank_and_null(self):
        """
        Tests that the *description* field may be blank or null.

        """

        field = self.input_definition._meta.get_field("description")
        self.assertTrue(field.blank)
        self.assertTrue(field.null)

    # is_configuration
    def test_is_configuration_default_value(self):
        """
        Test the default value of the *is_configuration* field.
        
        """

        field = self.input_definition._meta.get_field("is_configuration")
        self.assertTrue(field.default)

    # default
    def test_default_field_is_none(self):
        """
        Tests that the *default* field is set to None. This field is
        meant to be overriden by a :class:`~django.db.models.Field` instance.        

        """

        self.assertIsNone(self.input_definition.default)

    ###########
    # Methods #
    ###########

    def test_string(self):
        """
        Test the string output.

        """

        value = str(self.input_definition)
        expected = self.input_definition.key
        self.assertEqual(value, expected)

    def test_create_input_instance_raises_type_error(self):
        """
        Tests that calling the
        :meth:`~django_analyses.models.input.definitions.input_definition.InputDefinition.create_input_instance`
        raises a TypeError. This is the expected behavior as long as the
        input_class attribute is not defined (or ill defined).
        
        """

        with self.assertRaises(TypeError):
            self.input_definition.create_input_instance()

    def test_create_input_instance_with_non_model_value_raises_type_error(self):
        """
        Tests that calling the
        :meth:`~django_analyses.models.input.definitions.input_definition.InputDefinition.create_input_instance`
        with a non-model value raises a TypeError.
        
        """

        self.input_definition.input_class = str
        with self.assertRaises(TypeError):
            self.input_definition.create_input_instance()

    def test_create_input_instance_with_non_input_subclass_value_raises_type_error(
        self,
    ):
        """
        Tests that calling the
        :meth:`~django_analyses.models.input.definitions.input_definition.InputDefinition.create_input_instance`
        with a non-input model subclass value raises a TypeError.
        
        """
        # TODO:
        self.input_definition.input_class = str
        with self.assertRaises(TypeError):
            self.input_definition.create_input_instance()
