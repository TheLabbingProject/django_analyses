from django.core.exceptions import ValidationError
from django.test import TestCase
from tests.factories.analysis import AnalysisFactory
from tests.factories.analysis_version import AnalysisVersionFactory
from tests.factories.input.definitions.float_input_definition import (
    FloatInputDefinitionFactory,
)
from tests.factories.input.input_specification import InputSpecificationFactory
from tests.test_interface import Power


class AnalysisVersionTestCase(TestCase):
    """
    Tests for the :class:`~django_analyses.models.analysis_version.AnalysisVersion` model.    
    
    """

    def setUp(self):
        """
        Adds the created instances to the tests' contexts.
        For more information see unittest's :meth:`~unittest.TestCase.setUp` method.

        """

        self.addition_analysis = AnalysisFactory(title="addition")
        self.addition_analysis_version = AnalysisVersionFactory(
            analysis=self.addition_analysis, title="1.0", run_method_key="calculate"
        )

        power_base_definition = FloatInputDefinitionFactory(key="base", required=True)
        power_exp_definition = FloatInputDefinitionFactory(
            key="exponent", required=True
        )
        self.power_analysis = AnalysisFactory(title="power")
        self.power_spec = InputSpecificationFactory(
            analysis=self.power_analysis,
            base_input_definitions=[power_base_definition, power_exp_definition],
        )
        self.power_analysis_version = AnalysisVersionFactory(
            analysis=self.power_analysis,
            title="1.0",
            input_specification=self.power_spec,
        )

        self.division_analysis = AnalysisFactory(title="division")
        dividend_definition = FloatInputDefinitionFactory(key="dividend", required=True)
        divisor_definition = FloatInputDefinitionFactory(
            key="divisor", required=False, default=2.0
        )
        self.division_spec = InputSpecificationFactory(
            analysis=self.division_analysis,
            base_input_definitions=[dividend_definition, divisor_definition],
        )
        self.division_analysis_version = AnalysisVersionFactory(
            analysis=self.division_analysis,
            title="1.0",
            input_specification=self.division_spec,
            nested_results_attribute="results",
        )
        self.analysis_version_without_interface = AnalysisVersionFactory()

    ##########
    #  Meta  #
    ##########

    def test_ordering(self):
        """
        Validate the `ordering`_ of the model.

        .. _ordering: https://docs.djangoproject.com/en/2.2/ref/models/options/#ordering
        """

        value = self.power_analysis_version._meta.ordering
        self.assertTupleEqual(value, ("-title",))

    ###########
    # Methods #
    ###########

    def test_string(self):
        """
        Test the string method of the model.

        """

        self.assertIsInstance(self.power_analysis_version.__str__(), str)

    def test_get_interface_without_interface_raises_exception(self):
        with self.assertRaises(NotImplementedError):
            self.analysis_version_without_interface.get_interface()

    def test_get_interface_with_interface(self):
        interface = self.power_analysis_version.get_interface()
        self.assertEqual(interface, Power)

    def test_run_inteface(self):
        run = self.power_analysis_version.run_interface(base=5, exponent=2)
        self.assertEqual(run["result"], 25)

    def test_run_inteface_with_custom_run_method_key(self):
        run = self.addition_analysis_version.run_interface(x=1, y=2, z=3)
        self.assertEqual(run["result"], 6)

    def test_extract_results_without_nested_attribute(self):
        run = self.power_analysis_version.run_interface(base=5, exponent=2)
        results = self.power_analysis_version.extract_results(run)
        self.assertDictEqual(run, results)

    def test_extract_results_with_nested_attribute(self):
        run = self.division_analysis_version.run_interface(dividend=9.3, divisor=3)
        results = self.division_analysis_version.extract_results(run)
        self.assertDictEqual(run.results, results)

    def test_run_with_invalid_kwarg_keys(self):
        kwargs = {"base": 2, "exp": 10}
        with self.assertRaises(ValidationError):
            self.power_analysis_version.run(**kwargs)

    def test_run_with_missing_required(self):
        with self.assertRaises(ValidationError):
            self.power_analysis_version.run(base=2)

    def test_run_with_valid_arguments(self):
        result = self.power_analysis_version.run(base=2, exponent=10)
        self.assertEqual(result["result"], 1024)

    def test_update_input_with_defaults(self):
        inputs = {"dividend": 20}
        configuration = self.division_analysis_version.update_input_with_defaults(
            **inputs
        )
        inputs.update(divisor=2)
        self.assertDictEqual(configuration, inputs)

    def test_run_with_default_value(self):
        result = self.division_analysis_version.run(dividend=12)["result"]
        self.assertEqual(result, 6)
