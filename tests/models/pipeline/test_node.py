from django.core.exceptions import ValidationError
from django.db.models import QuerySet
from django.test import TestCase
from django_analyses.models.analysis import Analysis
from django_analyses.models.analysis_version import AnalysisVersion
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
        expected = f"\nNode #{self.node.id}\n{self.node.analysis_version}\nConfiguration: [{self.node.configuration}]\n"
        self.assertEqual(value, expected)

    def test_node_validation_with_no_configuration_returns_none(self):
        self.assertIsNone(self.node.validate())

    def test_node_validation_with_valid_configuration_keys_returns_none(self):
        definitions = self.node.analysis_version.input_specification.input_definitions
        for definition in definitions:
            self.node.configuration[definition.key] = "value"
        self.assertIsNone(self.node.validate())

    def test_node_validation_with_invalid_configuration_keys_raises_validation_error(
        self,
    ):
        self.node.configuration["some_invalid_definition_key!"] = "value"
        with self.assertRaises(ValidationError):
            self.node.validate()

    def test_get_full_configuration_with_defaults_only(self):
        defaults = self.node.analysis_version.input_specification.default_configuration
        configuration = self.node.get_full_configuration({})
        self.assertDictEqual(defaults, configuration)

    def test_get_full_configuration_with_defaults_and_node_configuration(self):
        defaults = self.node.analysis_version.input_specification.default_configuration
        node_configuration = {"a": "b", "c": "d"}
        self.node.configuration = node_configuration
        configuration = self.node.get_full_configuration({})
        expected = {**defaults, **node_configuration}
        self.assertDictEqual(configuration, expected)

    def test_get_full_configuration_with_defaults_and_node_configuration_and_inputs(
        self,
    ):
        defaults = self.node.analysis_version.input_specification.default_configuration
        node_configuration = {"a": "b", "c": "d"}
        inputs = {"e": "f", "g": "h"}
        self.node.configuration = node_configuration
        configuration = self.node.get_full_configuration(inputs)
        expected = {**defaults, **node_configuration, **inputs}
        self.assertDictEqual(configuration, expected)

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
        self.assertEqual(list(required_nodes), [self.addition_node])

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
        requiring_nodes = self.addition_node.get_requiring_nodes()
        self.assertEqual(list(requiring_nodes), [self.power_node])

    def test_check_configuration_sameness_for_default_value_returns_true(self):
        same = self.norm_node.check_configuration_sameness("order", None)
        self.assertTrue(same)

    def test_check_configuration_sameness_for_same_configuration_returns_true(self):
        self.norm_node.configuration = {"order": "inf"}
        same = self.norm_node.check_configuration_sameness("order", "inf")
        self.assertTrue(same)

    def test_check_configuration_sameness_for_non_configuration_returns_true(self):
        same = self.norm_node.check_configuration_sameness("x", [1, 2, 3, 4])
        self.assertTrue(same)

    def test_check_configuration_sameness_for_non_default_when_key_not_configured_returns_false(
        self,
    ):
        same = self.norm_node.check_configuration_sameness("order", "-inf")
        self.assertFalse(same)

    def test_check_configuration_sameness_for_not_same_configuration_returns_false(
        self,
    ):
        self.norm_node.configuration = {"order": "inf"}
        same = self.norm_node.check_configuration_sameness("order", "-inf")
        self.assertFalse(same)

    def test_check_run_configuration_sameness_for_not_same_configuration_returns_false(
        self,
    ):
        run = self.norm_node.run({"x": [1, 2, 3, 4]})
        another_node = NodeFactory(
            analysis_version=self.norm, configuration={"order": "-1"}
        )
        same = another_node.check_run_configuration_sameness(run)
        self.assertFalse(same)

    def test_check_run_configuration_sameness_for_same_configuration_returns_true(
        self,
    ):
        run = self.norm_node.run({"x": [1, 2, 3, 4]})
        same = self.norm_node.check_run_configuration_sameness(run)
        self.assertTrue(same)

    def test_get_run_set(self):
        run1 = self.norm_node.run({"x": [1, 2, 3]})
        run2 = self.norm_node.run({"x": [1, 2, 3, 4]})
        different_node = NodeFactory(
            analysis_version=self.norm, configuration={"order": -2}
        )
        different_node_run = different_node.run({"x": [1, 2, 3]})
        runs = self.norm_node.get_run_set()
        self.assertIn(run1, runs)
        self.assertIn(run2, runs)
        self.assertNotIn(different_node_run, runs)

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
        self.assertListEqual(required_nodes, [self.addition_node])

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
        self.assertListEqual(requiring_nodes, [self.power_node])

    def test_run_set(self):
        """
        Tests the :attr:`~django_analyses.models.pipline.node.Node.run_set` property
        return the expected :class:`~django.db.models.QuerySet`.
        """

        # Note: map(repr, qs) is required for QuerySet comparison,
        # see https://stackoverflow.com/a/14189017/4416932.
        value = self.norm_node.run_set
        expected = self.norm_node.get_run_set()
        self.assertQuerysetEqual(value, map(repr, expected))
        self.norm_node.run({"x": [10, 11, 12, 13]})
        value = self.norm_node.run_set
        expected = self.norm_node.get_run_set()
        self.assertEqual(len(value), 1)
        self.assertQuerysetEqual(value, map(repr, expected))
