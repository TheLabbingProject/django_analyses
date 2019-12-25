from django.db import models
from django_analyses.models.category import Category
from django_analyses.models.managers.analysis import AnalysisManager
from django_extensions.db.models import TitleDescriptionModel, TimeStampedModel


class Analysis(TitleDescriptionModel, TimeStampedModel):
    title = models.CharField(max_length=255, unique=True)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)

    objects = AnalysisManager()

    class Meta:
        verbose_name_plural = "Analyses"
        ordering = ("title",)

    def __str__(self) -> str:
        return self.title
