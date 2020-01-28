from django.test import TestCase
from django_analyses.models.analysis import Analysis
from django_analyses.models.analysis_version import AnalysisVersion
from django_analyses.models.run import Run
from tests.factories.pipeline.node import NodeFactory
from tests.factories.pipeline.pipe import PipeFactory
from tests.factories.pipeline.pipeline import PipelineFactory
from django_analyses.pipeline_runner import PipelineRunner
from tests.fixtures import ANALYSES


class PipelineRunnerTestCase(TestCase):
    """
    Tests for the :class:`~django_analyses.pipeline_runner.PipelineRunner` model.
    
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

        self.pipeline_runner = PipelineRunner(pipeline=self.pipeline)

    def test_get_incoming_pipes(self):
        addition_incoming = self.pipeline_runner.get_incoming_pipes(self.addition_node)
        self.assertFalse(addition_incoming)
        norm_incoming = self.pipeline_runner.get_incoming_pipes(self.norm_node)
        self.assertFalse(norm_incoming)
        power_incoming = self.pipeline_runner.get_incoming_pipes(self.power_node)
        self.assertEqual(len(power_incoming), 2)
        self.assertIn(self.addition_to_power_pipe, power_incoming)
        self.assertIn(self.norm_to_power_pipe, power_incoming)

    def test_run_entry_nodes(self):
        inputs = {
            self.addition_node: {"x": 1, "y": 2},
            self.norm_node: {"x": [1, 2, 3]},
        }
        self.pipeline_runner.run_entry_nodes(inputs)
        addition_run = self.pipeline_runner.runs[self.addition_node]
        self.assertIsInstance(addition_run, Run)
        addition_result = addition_run.output_set.first().value
        self.assertEqual(addition_result, 3)
        norm_run = self.pipeline_runner.runs[self.norm_node]
        norm_result = norm_run.output_set.first().value
        self.assertIsInstance(norm_run, Run)
        self.assertAlmostEqual(norm_result, 3.74165738677)

    def test_has_required_runs_with_no_runs_returns_false(self):
        self.assertFalse(self.pipeline_runner.has_required_runs(self.power_node))

    def test_has_required_runs_with_partial_runs_returns_false(self):
        self.pipeline_runner.runs[self.addition_node] = self.addition_node.run(
            {"x": 1, "y": 2}
        )
        self.assertFalse(self.pipeline_runner.has_required_runs(self.power_node))

    def test_has_required_runs_with_runs_returns_true(self):
        inputs = {
            self.addition_node: {"x": 1, "y": 2},
            self.norm_node: {"x": [1, 2, 3]},
        }
        self.pipeline_runner.run_entry_nodes(inputs)
        self.assertTrue(self.pipeline_runner.has_required_runs(self.power_node))

    def test_get_destination_kwarg(self):
        inputs = {
            self.addition_node: {"x": 1, "y": 2},
            self.norm_node: {"x": [6, 8]},
        }
        self.pipeline_runner.run_entry_nodes(inputs)
        power_base_kwarg = self.pipeline_runner.get_destination_kwarg(
            self.addition_to_power_pipe
        )
        self.assertDictEqual(power_base_kwarg, {"base": 3})
        power_exponent_kwarg = self.pipeline_runner.get_destination_kwarg(
            self.norm_to_power_pipe
        )
        self.assertDictEqual(power_exponent_kwarg, {"exponent": 10})

    def test_get_node_inputs(self):
        inputs = {
            self.addition_node: {"x": 1, "y": 2},
            self.norm_node: {"x": [6, 8]},
        }
        self.pipeline_runner.run_entry_nodes(inputs)
        power_kwargs = self.pipeline_runner.get_node_inputs(self.power_node)
        self.assertDictEqual(power_kwargs, {"base": 3, "exponent": 10})

    def test_run_node(self):
        inputs = {
            self.addition_node: {"x": 1, "y": 2},
            self.norm_node: {"x": [6, 8]},
        }
        self.pipeline_runner.run_entry_nodes(inputs)
        self.pipeline_runner.run_node(self.power_node)
        power_run = self.pipeline_runner.runs[self.power_node]
        self.assertIsInstance(power_run, Run)
        result = power_run.output_set.first().value
        self.assertEqual(result, 3 ** 10)

    def test_run(self):
        inputs = {
            self.addition_node: {"x": 1, "y": 2},
            self.norm_node: {"x": [6, 8]},
        }
        runs = self.pipeline_runner.run(inputs)
        self.assertEqual(len(runs), 3)
        self.assertIsInstance(runs[self.addition_node], Run)
        self.assertEqual(runs[self.addition_node].output_set.first().value, 3)
        self.assertIsInstance(runs[self.norm_node], Run)
        self.assertEqual(runs[self.norm_node].output_set.first().value, 10)
        self.assertIsInstance(runs[self.power_node], Run)
        self.assertEqual(runs[self.power_node].output_set.first().value, 3 ** 10)
