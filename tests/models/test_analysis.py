from django.test import TestCase
from django_analyses.models.analysis import Analysis
from tests.factories.analysis import AnalysisFactory
from tests.factories.category import CategoryFactory


class AnalysisTestCase(TestCase):
    """
    Tests for the :class:`~django_analyses.models.analysis.Analysis` model.
    
    """

    def setUp(self):
        """
        Adds the created instances to the tests' contexts.
        For more information see unittest's :meth:`~unittest.TestCase.setUp` method.

        """

        self.analysis = AnalysisFactory()
        self.category = CategoryFactory()

    ##########
    #  Meta  #
    ##########

    def test_verbose_name_plural(self):
        """
        Test the `verbose name plural`_ of the
        :class:`~django_analyses.models.analysis.Analysis` model.

        .. _verbose name plural: https://docs.djangoproject.com/en/2.2/ref/models/options/#verbose-name-plural
        """

        self.assertEqual(Analysis._meta.verbose_name_plural, "Analyses")

    def test_ordering(self):
        """
        Test the `ordering`_ of the
        :class:`~django_analyses.models.analysis.Analysis` model.

        .. _ordering: https://docs.djangoproject.com/en/2.2/ref/models/options/#ordering
        """

        self.assertTupleEqual(Analysis._meta.ordering, ("title",))

    ##########
    # Fields #
    ##########

    # title
    def test_title_max_length(self):
        """
        Test the max_length of the *title* field.
        
        """

        field = self.analysis._meta.get_field("title")
        self.assertEqual(field.max_length, 255)

    def test_title_is_unique(self):
        """
        Tests that the *title* field is unique.

        """

        field = self.analysis._meta.get_field("title")
        self.assertTrue(field.unique)

    def test_title_blank_and_null(self):
        """
        Tests that the *title* field may not be blank or null.

        """

        field = self.analysis._meta.get_field("title")
        self.assertFalse(field.blank)
        self.assertFalse(field.null)

    # description
    def test_description_is_not_unique(self):
        """
        Tests that the *description* field is not set to unique.

        """

        field = self.analysis._meta.get_field("description")
        self.assertFalse(field.unique)

    def test_description_blank_and_null(self):
        """
        Tests that the *description* field may be blank or null.

        """

        field = self.analysis._meta.get_field("description")
        self.assertTrue(field.blank)
        self.assertTrue(field.null)

    # category
    def test_category_is_nullable(self):
        """
        Tests that the *category* field is nullable.

        """

        field = self.analysis._meta.get_field("category")
        self.assertTrue(field.null)

    ###########
    # Methods #
    ###########

    def test_string(self):
        """
        Test the string output of the
        :class:`~django_analyses.models.analysis.Analysis` model.

        """

        self.assertEqual(str(self.analysis), self.analysis.title)
