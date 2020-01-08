from django.test import TestCase
from tests.factories.pipeline.node import NodeFactory


class NodeTestCase(TestCase):
    """
    Tests for the :class:`~django_analyses.models.node.Node` model.    
    
    """

    def setUp(self):
        """
        Adds the created instances to the tests' contexts.
        For more information see unittest's :meth:`~unittest.TestCase.setUp` method.

        """
        self.node = NodeFactory()

    ##########
    #  Meta  #
    ##########

    ###########
    # Methods #
    ###########

    def test_string(self):
        value = str(self.node)
        expected = f"{self.node.analysis_version} [{self.node.configuration}]"
        self.assertEqual(value, expected)

    ##############
    # Properties #
    ##############

