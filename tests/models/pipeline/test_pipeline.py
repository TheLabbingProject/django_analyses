from django.test import TestCase
from tests.factories.pipeline.pipeline import PipelineFactory


class PipelineTestCase(TestCase):
    """
    Tests for the :class:`~django_analyses.models.pipeline.Pipeline` model.    
    
    """

    def setUp(self):
        """
        Adds the created instances to the tests' contexts.
        For more information see unittest's :meth:`~unittest.TestCase.setUp` method.

        """
        self.pipeline = PipelineFactory()

    ##########
    #  Meta  #
    ##########

    ###########
    # Methods #
    ###########

    def test_string(self):
        value = str(self.pipeline)
        expected = self.pipeline.title
        self.assertEqual(value, expected)

    ##############
    # Properties #
    ##############

