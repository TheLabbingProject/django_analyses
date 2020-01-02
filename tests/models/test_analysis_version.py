from django.test import TestCase
from tests.factories.analysis import AnalysisFactory
from tests.factories.analysis_version import AnalysisVersionFactory
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
        self.power_analysis = AnalysisFactory(title="power")
        self.power_analysis_version = AnalysisVersionFactory(
            analysis=self.power_analysis, title="1.0"
        )
        self.division_analysis = AnalysisFactory(title="division")
        self.division_analysis_version = AnalysisVersionFactory(
            analysis=self.division_analysis,
            title="1.0",
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
