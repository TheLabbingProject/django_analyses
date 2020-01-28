# from django.test import TestCase
# from django_analyses.models.analysis import Analysis
# from django_analyses.models.analysis_version import AnalysisVersion
# from django_analyses.models.run import Run
# from tests.factories.pipeline.node import NodeFactory
# from tests.fixtures import ANALYSES


# class RunManagerTestCase(TestCase):
#     """
#     Tests for the :class:`~django_analyses.models.managers.run.RunManager` class.

#     """

#     @classmethod
#     def setUpTestData(cls):
#         Analysis.objects.from_list(ANALYSES)
#         cls.addition = AnalysisVersion.objects.get(analysis__title="addition")
#         cls.power = AnalysisVersion.objects.get(analysis__title="power")
#         cls.addition_node = NodeFactory(analysis_version=cls.addition)
#         cls.power_node = NodeFactory(analysis_version=cls.power)

#     def setUp(self):
#         """
#         Adds the created instances to the tests' contexts.
#         For more information see unittest's :meth:`~unittest.TestCase.setUp` method.

#         """
#         pass

#     def test_run_with_no_user(self):

