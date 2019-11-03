from django.contrib.postgres.fields import ArrayField
from django.db import models
from model_utils.managers import InheritanceManager


class InputConfiguration(models.Model):
    analysis = models.ForeignKey("django_analysis.Analysis", on_delete=models.CASCADE)
    key = models.CharField(max_length=50)
    required = models.BooleanField()

    objects = InheritanceManager()


class IntegerInputConfiguration(InputConfiguration):
    min_value = models.IntegerField(blank=True, null=True)
    max_value = models.IntegerField(blank=True, null=True)
    default = models.IntegerField(blank=True, null=True)


class FloatInputConfiguration(InputConfiguration):
    min_value = models.FloatField(blank=True, null=True)
    max_value = models.FloatField(blank=True, null=True)
    default = models.FloatField(blank=True, null=True)


class StringInputConfiguration(InputConfiguration):
    min_length = models.IntegerField(blank=True, null=True)
    max_length = models.IntegerField(blank=True, null=True)
    default = models.CharField(max_length=500, blank=True, null=True)
    choices = ArrayField(
        models.CharField(max_length=255, blank=True, null=True), blank=True, null=True
    )
