from django.test import TestCase
from django_analyses.models.output.types.output_types import OutputTypes
from tests.factories.output.types.float_output import FloatOutputFactory


class FloatOutputTestCase(TestCase):
    """
    Tests for the :class:`~django_analyses.models.output.types.float_output.FloatOutput` model.

    """

    def setUp(self):
        """
        Adds the created instances to the tests' contexts.
        For more information see unittest's :meth:`~unittest.TestCase.setUp` method.

        """

        self.float_output = FloatOutputFactory()

    ###########
    # Methods #
    ###########

    def test_string(self):
        value = str(self.float_output)
        expected = f"'{self.float_output.key}' = {self.float_output.value}"
        self.assertEqual(value, expected)

    def test_get_type(self):
        value = self.float_output.get_type()
        self.assertEqual(value, OutputTypes.FLT)

    ##############
    # Properties #
    ##############

    def test_key(self):
        value = self.float_output.key
        expected = self.float_output.definition.key
        self.assertEqual(value, expected)
