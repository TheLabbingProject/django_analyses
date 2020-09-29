from django.test import TestCase
from django_analyses.models.analysis import Analysis
from django_analyses.models.analysis_version import AnalysisVersion
from django_analyses.models.pipeline.node import Node
from django_analyses.models.pipeline.pipeline import Pipeline
from django_analyses.models.run import Run
from tests.factories.pipeline.node import NodeFactory
from tests.factories.pipeline.pipe import PipeFactory
from tests.factories.pipeline.pipeline import PipelineFactory
from django_analyses.pipeline_runner import PipelineRunner
from tests.fixtures import ANALYSES, PIPELINES


class PipelineRunnerTestCase(TestCase):
    """
    Tests for the :class:`~django_analyses.pipeline_runner.PipelineRunner`
    model.

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

    def setUp(self):
        """
        For more information see unittest's :meth:`~unittest.TestCase.setUp`
        method.

        """

        self.pipeline_runner = PipelineRunner(
            pipeline=self.pipeline, quiet=True
        )

    def test_get_incoming_pipes(self):
        addition_incoming = self.pipeline_runner.get_incoming_pipes(
            self.addition_node, run_index=0
        )
        self.assertFalse(addition_incoming)
        norm_incoming = self.pipeline_runner.get_incoming_pipes(
            self.norm_node, run_index=0
        )
        self.assertFalse(norm_incoming)
        power_incoming = self.pipeline_runner.get_incoming_pipes(
            self.power_node, run_index=0
        )
        self.assertEqual(len(power_incoming), 2)
        self.assertIn(self.addition_to_power_pipe, power_incoming)
        self.assertIn(self.norm_to_power_pipe, power_incoming)

    def test_run_entry_nodes(self):
        inputs = {
            self.addition_node: [{"x": 1, "y": 2}],
            self.norm_node: [{"x": [1, 2, 3]}],
        }
        self.pipeline_runner.run_entry_nodes(inputs)
        addition_runs = self.pipeline_runner.runs[self.addition_node]
        self.assertIsInstance(addition_runs, list)
        self.assertEqual(len(addition_runs), 1)
        self.assertIsInstance(addition_runs[0], Run)
        addition_result = addition_runs[0].output_set.first().value
        self.assertEqual(addition_result, 3)
        norm_runs = self.pipeline_runner.runs[self.norm_node]
        self.assertIsInstance(norm_runs, list)
        self.assertEqual(len(norm_runs), 1)
        self.assertIsInstance(norm_runs[0], Run)
        norm_result = norm_runs[0].output_set.first().value
        self.assertAlmostEqual(norm_result, 3.74165738677)

    def test_has_required_runs_with_no_runs_returns_false(self):
        self.assertFalse(
            self.pipeline_runner.has_required_runs(
                self.power_node, run_index=0
            )
        )

    def test_has_required_runs_with_partial_runs_returns_false(self):
        self.pipeline_runner.runs[self.addition_node] = self.addition_node.run(
            {"x": 1, "y": 2}
        )
        self.assertFalse(
            self.pipeline_runner.has_required_runs(
                self.power_node, run_index=0
            )
        )

    def test_has_required_runs_with_runs_returns_true(self):
        inputs = {
            self.addition_node: [{"x": 1, "y": 2}],
            self.norm_node: [{"x": [1, 2, 3]}],
        }
        self.pipeline_runner.run_entry_nodes(inputs)
        self.assertTrue(
            self.pipeline_runner.has_required_runs(
                self.power_node, run_index=0
            )
        )

    def test_get_destination_kwarg(self):
        inputs = {
            self.addition_node: [{"x": 1, "y": 2}],
            self.norm_node: [{"x": [6, 8]}],
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
            self.addition_node: [{"x": 1, "y": 2}],
            self.norm_node: [{"x": [6, 8]}],
        }
        self.pipeline_runner.run_entry_nodes(inputs)
        power_kwargs = self.pipeline_runner.get_node_inputs(
            self.power_node, inputs, 0
        )
        self.assertDictEqual(power_kwargs, {"base": 3, "exponent": 10})

    def test_run_node(self):
        inputs = {
            self.addition_node: [{"x": 1, "y": 2}],
            self.norm_node: [{"x": [6, 8]}],
        }
        self.pipeline_runner.run_entry_nodes(inputs)
        self.pipeline_runner.run_node(self.power_node, inputs)
        power_run = self.pipeline_runner.runs[self.power_node]
        self.assertIsInstance(power_run, list)
        self.assertEqual(len(power_run), 1)
        self.assertIsInstance(power_run[0], Run)
        result = power_run[0].output_set.first().value
        self.assertEqual(result, 3 ** 10)

    def test_run(self):
        inputs = {
            self.addition_node: [{"x": 1, "y": 2}],
            self.norm_node: [{"x": [6, 8]}],
        }
        runs = self.pipeline_runner.run(inputs)
        self.assertEqual(len(runs), 3)
        self.assertIsInstance(runs[self.addition_node], list)
        self.assertEqual(len(runs[self.addition_node]), 1)
        self.assertIsInstance(runs[self.addition_node][0], Run)
        self.assertEqual(
            runs[self.addition_node][0].output_set.first().value, 3
        )
        self.assertIsInstance(runs[self.norm_node], list)
        self.assertEqual(len(runs[self.norm_node]), 1)
        self.assertIsInstance(runs[self.norm_node][0], Run)
        self.assertEqual(runs[self.norm_node][0].output_set.first().value, 10)
        self.assertIsInstance(runs[self.power_node], list)
        self.assertEqual(len(runs[self.power_node]), 1)
        self.assertIsInstance(runs[self.power_node][0], Run)
        self.assertEqual(
            runs[self.power_node][0].output_set.first().value, 3 ** 10
        )

    def test_pipeline_with_two_identical_nodes(self):
        pipeline = Pipeline.objects.get(title="Test Pipeline 0")
        runner = PipelineRunner(pipeline=pipeline, quiet=True)
        results = runner.run(inputs=[{"x": 1, "y": 1}, {"y": 1}])
        addition_results = results[self.addition_node]
        self.assertIsInstance(addition_results, list)
        self.assertEqual(len(addition_results), 2)
        self.assertIsInstance(addition_results[0], Run)
        self.assertIsInstance(addition_results[1], Run)
        result = addition_results[1].get_output("result")
        expected = 3
        self.assertEqual(result, expected)

    def test_interleaved_pipeline(self):
        pipeline = Pipeline.objects.get(title="Test Pipeline 1")
        runner = PipelineRunner(pipeline=pipeline, quiet=True)
        square_node = Node.objects.get(
            analysis_version=self.power, configuration={"exponent": 2}
        )
        inputs = {
            self.addition_node: [{"x": 1, "y": 1}, {"x": 1, "y": 1}],
            square_node: [{"base": 1}],
        }
        results = runner.run(inputs=inputs)
        self.assertIsInstance(results, dict)
        self.assertEqual(len(results), 3)
        addition_results = results[self.addition_node]
        power_results = results[square_node]
        norm_results = results[self.norm_node]
        self.assertIsInstance(addition_results, list)
        self.assertIsInstance(power_results, list)
        self.assertIsInstance(norm_results, list)
        self.assertEqual(len(addition_results), 3)
        self.assertEqual(len(power_results), 2)
        self.assertEqual(len(norm_results), 1)
        for run in addition_results + power_results + norm_results:
            self.assertIsInstance(run, Run)
        first_addition_results = addition_results[0].get_output("result")
        second_addition_results = addition_results[1].get_output("result")
        third_addition_results = addition_results[2].get_output("result")
        first_addition_expected = 2.0
        second_addition_expected = 2.0
        third_addition_expected = 6.0
        self.assertEqual(first_addition_results, first_addition_expected)
        self.assertEqual(second_addition_results, second_addition_expected)
        self.assertEqual(third_addition_results, third_addition_expected)
        first_power_results = power_results[0].get_output("result")
        second_power_results = power_results[1].get_output("result")
        first_power_expected = 1.0
        second_power_expected = 4.0
        self.assertEqual(first_power_results, first_power_expected)
        self.assertEqual(second_power_results, second_power_expected)
        norm_result = norm_results[0].get_output("norm")
        norm_expected = 6.082762530298219
        self.assertAlmostEqual(norm_result, norm_expected)
