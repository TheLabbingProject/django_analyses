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

    def __str__(self) -> str:
        definitions = self.input_definitions.select_subclasses()
        formatted_definitions = "\n\t".join(
            [str(definition) for definition in definitions]
        )
        return f"\n[{self.analysis}]\n\t{formatted_definitions}\n"

    def get_default_input_configurations(self) -> dict:
        return {
            definition.key: definition.default
            for definition in self.input_definitions.select_subclasses()
            if definition.default is not None
        }

    def get_definitions_for_kwargs(self, **kwargs) -> QuerySet:
        return self.input_definitions.filter(key__in=kwargs).select_subclasses()

    @property
    def default_configuration(self) -> dict:
        return self.get_default_input_configurations()
