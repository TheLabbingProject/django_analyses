from django.test import TestCase
from django_analyses.models.category import Category
from tests.factories.category import CategoryFactory


class CategoryTestCase(TestCase):
    """
    Tests for the :class:`~django_analyses.models.category.Category` model.
    
    """

    def setUp(self):
        """
        Adds the created instances to the tests' contexts.
        For more information see unittest's :meth:`~unittest.TestCase.setUp` method.

        """

        self.category = CategoryFactory()

    ##########
    #  Meta  #
    ##########

    def test_verbose_name_plural(self):
        """
        Validate the `verbose name plural`_ of the
        :class:`~django_analyses.models.category.Category` model.

        .. _verbose name plural: https://docs.djangoproject.com/en/2.2/ref/models/options/#verbose-name-plural
        """

        self.assertEqual(Category._meta.verbose_name_plural, "Categories")

    def test_ordering(self):
        """
        Validate the `ordering`_ of the
        :class:`~django_analyses.models.category.Category` model.

        .. _ordering: https://docs.djangoproject.com/en/2.2/ref/models/options/#ordering
        """

        self.assertTupleEqual(Category._meta.ordering, ("title",))

    ##########
    # Fields #
    ##########

    # title
    def test_title_max_length(self):
        """
        Validate the max_length of the *title* field.
        
        """

        field = self.category._meta.get_field("title")
        self.assertEqual(field.max_length, 255)

    def test_title_is_unique(self):
        """
        Validates that the *title* field is unique.

        """

        field = self.category._meta.get_field("title")
        self.assertTrue(field.unique)

    def test_title_blank_and_null(self):
        """
        Validates that the *title* field may not be blank or null.

        """

        field = self.category._meta.get_field("title")
        self.assertFalse(field.blank)
        self.assertFalse(field.null)

    # description
    def test_description_is_not_unique(self):
        """
        Validates that the *description* field is not set to unique.

        """

        field = self.category._meta.get_field("description")
        self.assertFalse(field.unique)

    def test_description_blank_and_null(self):
        """
        Validates that the *description* field may be blank or null.

        """

        field = self.category._meta.get_field("description")
        self.assertTrue(field.blank)
        self.assertTrue(field.null)

    # parent
    def test_parent_is_nullable(self):
        """
        Validates that the *parent* field is nullable.

        """

        field = self.category._meta.get_field("parent")
        self.assertTrue(field.null)

    def test_creation_with_parent_category(self):
        """
        Tests creating a category with an existing category as the parent.
        
        """

        new_category = CategoryFactory(parent=self.category)
        self.assertEqual(new_category.parent, self.category)

    def test_settings_a_parent_category(self):
        """
        Tests setting a parent category.

        """

        parent = CategoryFactory()
        self.category.parent = parent
        self.category.save()
        self.assertEqual(self.category.parent, parent)

    ###########
    # Methods #
    ###########

    def test_string(self):
        """
        Validate the string output of the
        :class:`~django_analyses.models.category.category` model.

        """

        self.assertEqual(str(self.category), self.category.title)
