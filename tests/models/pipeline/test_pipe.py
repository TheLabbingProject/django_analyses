from django.test import TestCase
from django_analyses.models.input.definitions.float_input_definition import (
    FloatInputDefinition,
)
from django_analyses.models.output.definitions.float_output_definition import (
    FloatOutputDefinition,
)
from tests.factories.input.definitions.float_input_definition import (
    FloatInputDefinitionFactory,
)
from tests.factories.output.definitions.float_output_definition import (
    FloatOutputDefinitionFactory,
)
from tests.factories.pipeline.pipe import PipeFactory


class PipeTestCase(TestCase):
    """
    Tests for the :class:`~django_analyses.models.pipe.Pipe` model.

    """

    def setUp(self):
        """
        Adds the created instances to the tests' contexts.
        For more information see unittest's :meth:`~unittest.TestCase.setUp` method.

        """

        self.source_port = FloatOutputDefinitionFactory()
        self.destination_port = FloatInputDefinitionFactory()
        self.pipe = PipeFactory(
            base_source_port=self.source_port,
            base_destination_port=self.destination_port,
        )

    ##########
    #  Meta  #
    ##########

    ###########
    # Methods #
    ###########

    def test_string(self):
        self.assertIsInstance(str(self.pipe), str)

    ##############
    # Properties #
    ##############

    def test_source_port(self):
        self.assertIsInstance(self.pipe.source_port, FloatOutputDefinition)

    def test_destination_port(self):
        self.assertIsInstance(self.pipe.destination_port, FloatInputDefinition)
