"""
Definition of the :class:`~django_analyses.models.category.Category` class.
"""

from django.db import models
from django_extensions.db.models import TimeStampedModel, TitleDescriptionModel


class Category(TitleDescriptionModel, TimeStampedModel):
    """
    A :class:`~django.db.models.Model` representing a category of analyses in
    the databse.
    """

    #: Title of this category of analyses.
    title = models.CharField(max_length=255, unique=True)

    #: If this is a nested category, this field holds the association with
    #: the parent.
    parent = models.ForeignKey(
        "self",
        on_delete=models.CASCADE,
        null=True,
        related_name="subcategories",
    )

    class Meta:
        verbose_name_plural = "Categories"
        ordering = ("title",)

    def __str__(self) -> str:
        """
        Returns the string representation of the instance.

        Returns
        -------
        str
            This instance's string representation
        """

        return self.title
