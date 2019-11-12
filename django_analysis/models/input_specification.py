from django.db import models
from django.db.models import Count, QuerySet
from django_analysis.models.input.definitions.input_definition import InputDefinition


class InputSpecificationManager(models.Manager):
    def filter_by_definitions(self, analysis, definitions: list) -> QuerySet:
        possibly_same = self.filter(
            analysis=analysis, input_definitions__in=definitions
        )
        return possibly_same.annotate(
            input_definitions__count=Count("input_definitions")
        ).filter(input_definitions__count=len(definitions))

    def from_dict(self, analysis, specification: dict) -> tuple:
        input_definitions = InputDefinition.objects.from_specification_dict(
            specification
        )
        existing_specification = self.filter_by_definitions(analysis, input_definitions)
        if not existing_specification:
            new_specification = self.create(analysis=analysis)
            new_specification.input_definitions.set(input_definitions)
            return new_specification, True
        return existing_specification[0], False


class InputSpecification(models.Model):
    analysis = models.ForeignKey("django_analysis.Analysis", on_delete=models.CASCADE)
    input_definitions = models.ManyToManyField("django_analysis.InputDefinition")

    objects = InputSpecificationManager()
