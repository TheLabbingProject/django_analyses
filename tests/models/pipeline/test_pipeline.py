from django.test import TestCase
from django_analyses.models.analysis import Analysis
from django_analyses.models.analysis_version import AnalysisVersion
from django_analyses.models.pipeline import Pipeline
from django_analyses.models.pipeline.node import Node
from tests.factories.pipeline.node import NodeFactory
from tests.factories.pipeline.pipe import PipeFactory
from tests.factories.pipeline.pipeline import PipelineFactory
from tests.fixtures import ANALYSES, PIPELINES


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
        Pipeline.objects.from_list(PIPELINES)
        cls.pipeline_0 = Pipeline.objects.get(title="Test Pipeline 0")
        cls.pipeline_1 = Pipeline.objects.get(title="Test Pipeline 1")

    def setUp(self):
        """
        For more information see unittest's :meth:`~unittest.TestCase.setUp`
        method.

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

    def test_interleaved_pipeline_entry_nodes(self):
        square_node = Node.objects.get(
            analysis_version=self.power, configuration={"exponent": 2}
        )
        entry_nodes = self.pipeline_1.get_entry_nodes()
        expected = [self.addition_node, square_node]
        self.assertEqual(len(entry_nodes), 2)
        self.assertIn(expected[0], entry_nodes)
        self.assertIn(expected[1], entry_nodes)

    def test_count_node_runs(self):
        node = self.pipeline_0.node_set.first()
        value = self.pipeline_0.count_node_runs(node)
        expected = 2
        self.assertEqual(value, expected)

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
