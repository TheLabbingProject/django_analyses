from django.test import TestCase
from django_analyses.models.analysis import Analysis
from tests.models.managers.fixtures import ANALYSIS_0, ANALYSIS_1, VERSIONLESS_ANALYSIS


class AnalysisManagerTestCase(TestCase):
    """
    Tests for the :class:`~django_analyses.models.managers.analysis.AnalysisManager` class.

    """

    def setUp(self):
        """
        Adds the created instances to the tests' contexts.
        For more information see unittest's :meth:`~unittest.TestCase.setUp` method.

        """
        pass

    def test_from_dict_without_versions(self):
        analysis, created, versions = Analysis.objects.from_dict(VERSIONLESS_ANALYSIS)
        self.assertIsInstance(analysis, Analysis)
        self.assertTrue(created)
        self.assertDictEqual(versions, {})

    def test_from_dict_with_versions(self):
        analysis, created, versions = Analysis.objects.from_dict(ANALYSIS_0)
        self.assertIsInstance(analysis, Analysis)
        self.assertTrue(created)
        self.assertEqual(len(versions), 3)

    def test_from_list(self):
        results = Analysis.objects.from_list([ANALYSIS_0, ANALYSIS_1])
        self.assertIsInstance(results, dict)
        self.assertIsInstance(results[ANALYSIS_0["title"]]["model"], Analysis)
        self.assertIsInstance(results[ANALYSIS_1["title"]]["model"], Analysis)
        self.assertTrue(results[ANALYSIS_0["title"]]["created"])
        self.assertTrue(results[ANALYSIS_1["title"]]["created"])
        self.assertEqual(len(results[ANALYSIS_0["title"]]["versions"]), 3)
        self.assertEqual(len(results[ANALYSIS_1["title"]]["versions"]), 1)

    def test_from_list_with_existing_analysis(self):
        analysis_0, _, _ = Analysis.objects.from_dict(ANALYSIS_0)
        results = Analysis.objects.from_list([ANALYSIS_0, ANALYSIS_1])
        self.assertFalse(results[ANALYSIS_0["title"]]["created"])
        self.assertEqual(results[ANALYSIS_0["title"]]["model"], analysis_0)
