from django.test import TestCase
from django_analyses.models.pipeline import Pipeline
from tests.factories.pipeline.pipeline import PipelineFactory


class PipelineManagerTestCase(TestCase):
    """
    Tests for the :class:`~django_analyses.models.managers.pipeline.PipelineManager`
    class.

    """

    def setUp(self):
        """
        Adds the created instances to the tests' contexts.
        For more information see unittest's :meth:`~unittest.TestCase.setUp` method.

        """
        self.pipeline = PipelineFactory()

    def test_from_dict(self):
        # pipeline = Pipeline.objects.from_dict()
        self.assertIsInstance(self.pipeline, Pipeline)
