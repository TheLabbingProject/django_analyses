from django.core.exceptions import ValidationError
from django.db.models import QuerySet
from django.test import TestCase
from django_analyses.models.analysis import Analysis
from django_analyses.models.analysis_version import AnalysisVersion
from django_analyses.models.run import Run
from tests.factories.pipeline.node import NodeFactory
from tests.factories.pipeline.pipe import PipeFactory
from tests.factories.pipeline.pipeline import PipelineFactory
from tests.factories.user import UserFactory
from tests.fixtures import ANALYSES


class NodeTestCase(TestCase):
    """
    Tests for the :class:`~django_analyses.models.node.Node` model.

    """

    @classmethod
    def setUpTestData(cls):
        Analysis.objects.from_list(ANALYSES)
        cls.addition = AnalysisVersion.objects.get(analysis__title="addition")
        cls.power = AnalysisVersion.objects.get(analysis__title="power")
        cls.norm = AnalysisVersion.objects.get(analysis__title="norm")
        cls.addition_node = NodeFactory(analysis_version=cls.addition)
        cls.power_node = NodeFactory(analysis_version=cls.power)
        cls.norm_node = NodeFactory(analysis_version=cls.norm)

    def setUp(self):
        """
        Adds the created instances to the tests' contexts.
        For more information see unittest's :meth:`~unittest.TestCase.setUp`
        method.

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
        expected = f"\nNode #{self.node.id}\n{self.node.analysis_version}\nConfiguration: [{self.node.configuration}]\n"  # noqa: E501
        self.assertEqual(value, expected)

    def test_node_validation_with_no_configuration_returns_none(self):
        self.assertIsNone(self.node.validate())

    def test_node_validation_with_valid_configuration_keys_returns_none(self):
        definitions = (
            self.node.analysis_version.input_specification.input_definitions
        )
        for definition in definitions:
            self.node.configuration[definition.key] = "value"
        self.assertIsNone(self.node.validate())

    def test_node_validation_with_invalid_configuration_keys_raises_validation_error(  # noqa: E501
        self,
    ):
        self.node.configuration["some_invalid_definition_key!"] = "value"
        with self.assertRaises(ValidationError):
            self.node.validate()

    def test_get_full_configuration_with_defaults_only(self):
        defaults = (
            self.node.analysis_version.input_specification.default_configuration  # noqa: E501
        )
        configuration = self.node.get_full_configuration({})
        self.assertDictEqual(defaults, configuration)

    def test_run_with_no_user(self):
        run = self.addition_node.run({"x": 6, "y": 4})
        self.assertEqual(run.output_set.count(), 1)
        self.assertEqual(run.output_set.first().value, 10)
        self.assertIsNone(run.user)

    def test_run_with_user(self):
        user = UserFactory()
        run = self.power_node.run({"base": 2, "exponent": 5}, user=user)
        self.assertEqual(run.output_set.count(), 1)
        self.assertEqual(run.output_set.first().value, 32)
        self.assertEqual(run.user, user)

    def test_get_required_nodes_with_no_pipes(self):
        required_nodes = self.addition_node.get_required_nodes()
        self.assertIsInstance(required_nodes, QuerySet)
        self.assertFalse(required_nodes)

    def test_get_required_nodes_with_a_pipe(self):
        pipeline = PipelineFactory()
        addition_output = self.addition.output_definitions.first()
        power_base_definition = self.power.input_definitions.get(key="base")
        PipeFactory(
            pipeline=pipeline,
            source=self.addition_node,
            base_source_port=addition_output,
            destination=self.power_node,
            base_destination_port=power_base_definition,
        )
        required_nodes = self.power_node.get_required_nodes()
        expected = [{"source": self.addition_node.id, "source_run_index": 0}]
        self.assertEqual(list(required_nodes), expected)

    def test_get_requiring_nodes_with_no_pipes(self):
        requiring_nodes = self.addition_node.get_requiring_nodes()
        self.assertIsInstance(requiring_nodes, QuerySet)
        self.assertFalse(requiring_nodes)

    def test_get_requiring_nodes_with_a_pipe(self):
        pipeline = PipelineFactory()
        addition_output = self.addition.output_definitions.first()
        power_base_definition = self.power.input_definitions.get(key="base")
        PipeFactory(
            pipeline=pipeline,
            source=self.addition_node,
            base_source_port=addition_output,
            destination=self.power_node,
            base_destination_port=power_base_definition,
        )
        requiring_nodes = list(self.addition_node.get_requiring_nodes())
        expected = [
            {"destination": self.power_node.id, "destination_run_index": 0}
        ]
        self.assertListEqual(requiring_nodes, expected)

    def test_get_run_set(self):
        run1 = self.norm_node.run({"x": [1, 2, 3]})
        run2 = self.norm_node.run({"x": [1, 2, 3, 4]})
        different_node = NodeFactory(
            analysis_version=self.norm, configuration={"order": "-2"}
        )
        different_node_run = different_node.run({"x": [1, 2, 3]})
        runs = self.norm_node.get_run_set()
        try:
            self.assertIn(run1, runs)
            self.assertIn(run2, runs)
        except AssertionError as e:
            message = str(e)
            message += """
            \nOne or more of the matching runs was not included in the node's
            run set!"""
            message += f"\nNode configuration:\t{self.norm_node.configuration}"
            message += f"\nRun #1 configuration:\t {run1.input_configuration}"
            message += f"\nRun #2 configuration:\t {run2.input_configuration}"
            self.fail(message)
        try:
            self.assertNotIn(different_node_run, runs)
        except AssertionError as e:
            message = str(e)
            message += "\nDifferent configuration run was included in the \
                        node's run set!"
            message += f"\nNode configuration:\t{self.norm_node.configuration}"
            message += f"\nRun configuration:\t\
                {different_node_run.input_configuration}"
            self.fail(message)

    ##############
    # Properties #
    ##############

    def test_required_nodes_with_no_required_returns_none(self):
        self.assertIsNone(self.addition_node.required_nodes)

    def test_required_nodes_with_required(self):
        pipeline = PipelineFactory()
        addition_output = self.addition.output_definitions.first()
        power_base_definition = self.power.input_definitions.get(key="base")
        PipeFactory(
            pipeline=pipeline,
            source=self.addition_node,
            base_source_port=addition_output,
            destination=self.power_node,
            base_destination_port=power_base_definition,
        )
        required_nodes = list(self.power_node.required_nodes)
        expected = [{"source": self.addition_node.id, "source_run_index": 0}]
        self.assertListEqual(required_nodes, expected)

    def test_requiring_nodes_with_no_required_returns_none(self):
        self.assertIsNone(self.power_node.requiring_nodes)

    def test_requiring_nodes_with_required(self):
        pipeline = PipelineFactory()
        addition_output = self.addition.output_definitions.first()
        power_base_definition = self.power.input_definitions.get(key="base")
        PipeFactory(
            pipeline=pipeline,
            source=self.addition_node,
            base_source_port=addition_output,
            destination=self.power_node,
            base_destination_port=power_base_definition,
        )
        requiring_nodes = list(self.addition_node.requiring_nodes)
        expected = [
            {"destination": self.power_node.id, "destination_run_index": 0}
        ]
        self.assertListEqual(requiring_nodes, expected)

    def test_run_with_multiple_inputs_as_list(self):
        inputs = [{"x": 1, "y": 2}, {"x": 3, "y": 4}]
        results = self.addition_node.run(inputs=inputs)
        self.assertIsInstance(results, list)
        for result in results:
            self.assertIsInstance(result, Run)

    def test_run_with_multiple_inputs_as_tuple(self):
        inputs = {"x": 5, "y": 6}, {"x": 7, "y": 8}
        results = self.addition_node.run(inputs=inputs)
        self.assertIsInstance(results, list)
        for result in results:
            self.assertIsInstance(result, Run)
