from django.db import models
from django_analysis.models.input.input import Input


class BooleanInput(Input):
    value = models.BooleanField()
