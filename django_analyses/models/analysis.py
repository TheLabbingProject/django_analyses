"""
Definition of the :class:`~django_analyses.models.analysis.Analysis` class.

"""

from django.db import models
from django_analyses.models.category import Category
from django_analyses.models.managers.analysis import AnalysisManager
from django_extensions.db.models import TitleDescriptionModel, TimeStampedModel


class Analysis(TitleDescriptionModel, TimeStampedModel):
    """
    :class:`~django.db.models.Model` representing a single analysis in the database.

    """

    # Override TitleDescriptionModel's title definition to specify `unique=True`
    title = models.CharField(max_length=255, unique=True)

    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)

    objects = AnalysisManager()

    class Meta:
        verbose_name_plural = "Analyses"
        ordering = ("title",)

    def __str__(self) -> str:
        """
        Returns the string representation of an
        :class:`~django_analyses.models.analysis.Analysis` instance.

        Returns
        -------
        str
            Instance string representation
        """

        return self.title
