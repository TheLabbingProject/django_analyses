from django.db import models
from django_analysis.models.input_specification import InputSpecification
from django_analysis.models.output_specification import OutputSpecification
from django_extensions.db.models import TitleDescriptionModel, TimeStampedModel


class AnalysisVersionManager(models.Manager):
    def from_dict(self, analysis, definition: dict):
        input_specification, created_input_spec = InputSpecification.objects.from_dict(
            analysis, definition["input"]
        )
        (
            output_specification,
            created_output_spec,
        ) = OutputSpecification.objects.from_dict(analysis, definition["output"])
        return self.get_or_create(
            analysis=analysis,
            title=definition.get("title", "1.0.0"),
            description=definition.get("description"),
            input_specification=input_specification,
            output_specification=output_specification,
            nested_results_attribute=definition.get("nested_results_attribute"),
        )

    def from_list(self, analysis, definitions: list) -> dict:
        results = {}
        for version_definition in definitions:
            version, created = self.from_dict(analysis, version_definition)
            results[version.title] = {"model": version, "created": created}
        return results


class AnalysisVersion(TitleDescriptionModel, TimeStampedModel):
    analysis = models.ForeignKey(
        "django_analysis.Analysis",
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        related_name="version_set",
    )
    input_specification = models.ForeignKey(
        "django_analysis.InputSpecification",
        on_delete=models.PROTECT,
        blank=True,
        null=True,
        related_name="analysis_version_set",
    )
    output_specification = models.ForeignKey(
        "django_analysis.OutputSpecification",
        on_delete=models.PROTECT,
        blank=True,
        null=True,
        related_name="analysis_version_set",
    )
    run_method_key = models.CharField(max_length=100, default="run")
    nested_results_attribute = models.CharField(max_length=100, blank=True, null=True)

    objects = AnalysisVersionManager()

    class Meta:
        unique_together = ("analysis", "title")

    def __str__(self) -> str:
        return f"{self.analysis.title} v{self.title}"

    def run(self, *args, **kwargs):
        raise NotImplementedError

    def get_input_definitions_for_kwargs(self, **kwargs) -> models.QuerySet:
        return self.input_specification.get_definitions_for_kwargs(**kwargs)

    def get_output_definitions_for_results(self, **results) -> models.QuerySet:
        return self.output_specification.get_definitions_for_results(**results)
