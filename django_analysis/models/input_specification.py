from django.db import models
from django.db.models import Count
from django_analysis.models.analysis import Analysis
from django_analysis.models.input.definitions.input_definition import InputDefinition


class InputSpecificationManager(models.Manager):
    def from_dict(self, analysis: Analysis, specification: dict) -> tuple:
        input_definitions = []
        for key, definition in specification.items():
            input_type_model = definition.pop("type")
            input_type_instance, _ = input_type_model.objects.get_or_create(
                key=key, **definition
            )
            input_definitions += [input_type_instance]
        instance = self.annotate(
            input_definitions__count=Count("input_definitions")
        ).filter(
            analysis=analysis,
            input_definitions__in=input_definitions,
            input_definitions__count=len(input_definitions),
        )
        print(instance)
        # TODO: Fix unique creation
        return instance, input_definitions


class InputSpecification(models.Model):
    analysis = models.ForeignKey("django_analysis.Analysis", on_delete=models.CASCADE)
    input_definitions = models.ManyToManyField("django_analysis.InputDefinition")

    objects = InputSpecificationManager()
