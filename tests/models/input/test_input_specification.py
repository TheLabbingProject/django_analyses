from django.core.exceptions import ValidationError
from django.db.models import QuerySet
from django.test import TestCase
from django_analyses.models.input.definitions.boolean_input_definition import (
    BooleanInputDefinition,
)
from django_analyses.models.input.definitions.file_input_definition import (
    FileInputDefinition,
)
from django_analyses.models.input.definitions.float_input_definition import (
    FloatInputDefinition,
)
from django_analyses.models.input.definitions.integer_input_definition import (
    IntegerInputDefinition,
)
from django_analyses.models.input.definitions.list_input_definition import (
    ListInputDefinition,
)
from django_analyses.models.input.definitions.string_input_definition import (
    StringInputDefinition,
)

from tests.factories.input.input_specification import InputSpecificationFactory


class InputSpecificationTestCase(TestCase):
    """
    Tests for the
    :class:`~django_analyses.models.input.input_specification.InputSpecification`
    model.
    
    """

    def setUp(self):
        """
        Adds the created instances to the tests' contexts.
        For more information see unittest's :meth:`~unittest.TestCase.setUp` method.

        """

        self.input_specification = InputSpecificationFactory()

    ##########
    #  Meta  #
    ##########

    ###########
    # Methods #
    ###########

    # __str__
    def test_string(self):
        self.assertIsInstance(self.input_specification.__str__(), str)

    # validate_keys
    def test_validate_keys_with_valid_keys(self):
        kwargs = {
            definition.key: "value"
            for definition in self.input_specification.input_definitions
        }
        try:
            self.input_specification.validate_keys(**kwargs)
        except ValidationError:
            self.fail("ValidatioError raised with valid keys!")

    def test_validate_keys_with_an_invalid_key(self):
        kwargs = {
            definition.key: "value"
            for definition in self.input_specification.input_definitions
        }
        kwargs["invalid_key"] = "check"
        with self.assertRaises(ValidationError):
            self.input_specification.validate_keys(**kwargs)

    # validate_required
    def test_validate_required_with_valid_kwargs(self):
        required = {
            definition.key: "value"
            for definition in self.input_specification.input_definitions
            if definition.required
        }
        try:
            self.input_specification.validate_required(**required)
        except ValidationError:
            self.fail("ValidationError raised with all required fields provided!")

    def test_validate_required_with_a_missing_kwarg(self):
        required_keys = [
            definition.key
            for definition in self.input_specification.input_definitions
            if definition.required
        ]
        required = {key: "value" for key in required_keys}
        required.pop(required_keys[0])
        with self.assertRaises(ValidationError):
            self.input_specification.validate_required(**required)

    # validate_kwargs
    def test_validate_kwargs_with_valid_kwargs(self):
        kwargs = {
            definition.key: "value"
            for definition in self.input_specification.input_definitions
        }
        try:
            self.input_specification.validate_kwargs(**kwargs)
        except ValidationError:
            self.fail("ValidationError raised with valid kwargs!")

    def test_validate_kwargs_with_a_missing_required_key(self):
        required_keys = [
            definition.key
            for definition in self.input_specification.input_definitions
            if definition.required
        ]
        kwargs = {
            definition.key: "value"
            for definition in self.input_specification.input_definitions
        }
        kwargs.pop(required_keys[0])
        with self.assertRaises(ValidationError):
            self.input_specification.validate_kwargs(**kwargs)

    def test_validate_kwargs_with_an_invalid_key(self):
        kwargs = {
            definition.key: "value"
            for definition in self.input_specification.input_definitions
        }
        kwargs["invalid_key"] = "check"
        with self.assertRaises(ValidationError):
            self.input_specification.validate_kwargs(**kwargs)

    ##############
    # Properties #
    ##############

    # default_configuration
    def test_default_configuration_property(self):
        value = self.input_specification.default_configuration
        expected = {
            definition.key: definition.default
            for definition in self.input_specification.input_definitions
            if definition.default is not None
        }
        self.assertDictEqual(value, expected)

    # input_definitions
    def test_input_definitions_property_return_type(self):
        value = self.input_specification.input_definitions
        self.assertIsInstance(value, QuerySet)

    def test_input_definitions_property_returns_subclasses(self):
        value = self.input_specification.input_definitions
        subclasses = [type(definition) for definition in value]
        self.assertIn(BooleanInputDefinition, subclasses)
        self.assertIn(FileInputDefinition, subclasses)
        self.assertIn(FloatInputDefinition, subclasses)
        self.assertIn(IntegerInputDefinition, subclasses)
        self.assertIn(ListInputDefinition, subclasses)
        self.assertIn(StringInputDefinition, subclasses)
