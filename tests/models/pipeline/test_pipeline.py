from django.test import TestCase
from django_analyses.models.analysis import Analysis
from django_analyses.models.analysis_version import AnalysisVersion
from tests.factories.pipeline.node import NodeFactory
from tests.factories.pipeline.pipe import PipeFactory
from tests.factories.pipeline.pipeline import PipelineFactory
from tests.fixtures import ANALYSES


class PipelineTestCase(TestCase):
    """
    Tests for the :class:`~django_analyses.models.pipeline.Pipeline` model.    
    
    """

    @classmethod
    def setUpTestData(cls):
        cls.pipeline = PipelineFactory()
        Analysis.objects.from_list(ANALYSES)
        cls.addition = AnalysisVersion.objects.get(analysis__title="addition")
        cls.power = AnalysisVersion.objects.get(analysis__title="power")
        cls.norm = AnalysisVersion.objects.get(analysis__title="norm")
        cls.addition_node = NodeFactory(analysis_version=cls.addition)
        cls.power_node = NodeFactory(analysis_version=cls.power)
        cls.norm_node = NodeFactory(analysis_version=cls.norm)
        norm_output = cls.norm.output_definitions.get(key="norm")
        addition_output = cls.addition.output_definitions.get(key="result")
        power_base_input = cls.power.input_definitions.get(key="base")
        power_exponent_input = cls.power.input_definitions.get(key="exponent")
        cls.norm_to_power_pipe = PipeFactory(
            pipeline=cls.pipeline,
            source=cls.norm_node,
            base_source_port=norm_output,
            destination=cls.power_node,
            base_destination_port=power_exponent_input,
        )
        cls.addition_to_power_pipe = PipeFactory(
            pipeline=cls.pipeline,
            source=cls.addition_node,
            base_source_port=addition_output,
            destination=cls.power_node,
            base_destination_port=power_base_input,
        )

    def setUp(self):
        """
        For more information see unittest's :meth:`~unittest.TestCase.setUp` method.

        """
        pass

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

    def test_get_node_set(self):
        nodes = list(self.pipeline.get_node_set())
        self.assertEqual(len(nodes), 3)
        self.assertIn(self.addition_node, nodes)
        self.assertIn(self.norm_node, nodes)
        self.assertIn(self.power_node, nodes)

    def test_get_entry_nodes(self):
        entry_nodes = list(self.pipeline.get_entry_nodes())
        self.assertEqual(len(entry_nodes), 2)
        self.assertIn(self.addition_node, entry_nodes)
        self.assertIn(self.norm_node, entry_nodes)

    ##############
    # Properties #
    ##############

    def test_node_set(self):
        expected = self.pipeline.get_node_set()
        self.assertQuerysetEqual(
            self.pipeline.node_set, expected, transform=lambda x: x
        )

    def test_entry_nodes(self):
        expected = self.pipeline.get_entry_nodes()
        self.assertQuerysetEqual(
            self.pipeline.entry_nodes, expected, transform=lambda x: x
        )

