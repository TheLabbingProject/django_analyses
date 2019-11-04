from django.db import models


class InputSpecification(models.Model):
    analysis = models.ForeignKey("django_analysis.Analysis", on_delete=models.CASCADE)

