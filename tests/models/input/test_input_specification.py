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
from tests.factories.input.definitions.boolean_input_definition import (
    BooleanInputDefinitionFactory,
)
from tests.factories.input.definitions.file_input_definition import (
    FileInputDefinitionFactory,
)
from tests.factories.input.definitions.float_input_definition import (
    FloatInputDefinitionFactory,
)
from tests.factories.input.definitions.integer_input_definition import (
    IntegerInputDefinitionFactory,
)
from tests.factories.input.definitions.list_input_definition import (
    ListInputDefinitionFactory,
)
from tests.factories.input.definitions.string_input_definition import (
    StringInputDefinitionFactory,
)


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

        boolean_input_definition = BooleanInputDefinitionFactory()
        file_input_definition = FileInputDefinitionFactory()
        float_input_definition = FloatInputDefinitionFactory()
        integer_input_definition = IntegerInputDefinitionFactory()
        list_input_definition = ListInputDefinitionFactory()
        string_input_definition = StringInputDefinitionFactory()
        self.input_definitions = [
            boolean_input_definition,
            file_input_definition,
            float_input_definition,
            integer_input_definition,
            list_input_definition,
            string_input_definition,
        ]
        self.input_specification = InputSpecificationFactory(
            base_input_definition=self.input_definitions
        )

    ##########
    #  Meta  #
    ##########

    ##############
    # Properties #
    ##############

    # input_definitions
    def test_input_definitions_return_type(self):
        value = self.input_specification.input_definitions
        self.assertIsInstance(value, QuerySet)

    def test_input_definitions_returns_subclasses(self):
        value = self.input_specification.input_definitions
        subclasses = [type(definition) for definition in value]
        self.assertIn(BooleanInputDefinition, subclasses)
        self.assertIn(FileInputDefinition, subclasses)
        self.assertIn(FloatInputDefinition, subclasses)
        self.assertIn(IntegerInputDefinition, subclasses)
        self.assertIn(ListInputDefinition, subclasses)
        self.assertIn(StringInputDefinition, subclasses)

    # required_keys
    def test_required_keys(self):
        keys = sorted(self.input_specification.required_keys)
        expected = sorted(
            [
                definition.key
                for definition in self.input_definitions
                if definition.required
            ]
        )
        self.assertListEqual(keys, expected)

