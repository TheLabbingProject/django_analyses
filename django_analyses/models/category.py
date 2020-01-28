from django.db import models
from django_extensions.db.models import TitleDescriptionModel, TimeStampedModel


class Category(TitleDescriptionModel, TimeStampedModel):
    title = models.CharField(max_length=255, unique=True)
    parent = models.ForeignKey(
        "self", on_delete=models.CASCADE, null=True, related_name="subcategories",
    )

    class Meta:
        verbose_name_plural = "Categories"
        ordering = ("title",)

    def __str__(self) -> str:
        return self.title
