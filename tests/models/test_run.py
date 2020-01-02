from django.test import TestCase
from tests.factories.input.input_specification import InputSpecificationFactory
from tests.factories.output.output_specification import OutputSpecificationFactory


class RunTestCase(TestCase):
    """
    Tests for the :class:`~django_analyses.models.run.Run` model.    
    
    """

    def setUp(self):
        """
        Adds the created instances to the tests' contexts.
        For more information see unittest's :meth:`~unittest.TestCase.setUp` method.

        """

        self.output_specification = OutputSpecificationFactory()
        self.input_specification = InputSpecificationFactory()
