from django.db import models
from django_analysis.models.analysis import Analysis


class InputSpecificationManager(models.Manager):
    def from_dict(self, analysis: Analysis, specification: dict) -> tuple:
        instance = self.model(analysis)
        for key, value in specification.items():
            input_type = value["type"]
            kwargs = {key: value for key, value in value.items() if key != "type"}
            input_definition, _ = input_type.objects.get_or_create(key=key, **kwargs)
            instance.input_definitions.add(input_definition)
        print(instance)
        # TODO: Fix unique creation
        return instance


class InputSpecification(models.Model):
    analysis = models.ForeignKey("django_analysis.Analysis", on_delete=models.CASCADE)
    input_definitions = models.ManyToManyField("django_analysis.InputDefinition")

    objects = InputSpecificationManager()
