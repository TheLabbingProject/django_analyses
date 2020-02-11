from django.conf import settings
from django.contrib.postgres.fields import JSONField
from django.db import models
from django_analyses.models.managers.analysis_version import AnalysisVersionManager
from django_extensions.db.models import TitleDescriptionModel, TimeStampedModel


class AnalysisVersion(TitleDescriptionModel, TimeStampedModel):
    analysis = models.ForeignKey(
        "django_analyses.Analysis",
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        related_name="version_set",
    )
    input_specification = models.ForeignKey(
        "django_analyses.InputSpecification",
        on_delete=models.PROTECT,
        blank=True,
        null=True,
        related_name="analysis_version_set",
    )
    output_specification = models.ForeignKey(
        "django_analyses.OutputSpecification",
        on_delete=models.PROTECT,
        blank=True,
        null=True,
        related_name="analysis_version_set",
    )
    run_method_key = models.CharField(max_length=100, default="run")
    fixed_run_method_kwargs = JSONField(default=dict)
    nested_results_attribute = models.CharField(max_length=100, blank=True, null=True)

    objects = AnalysisVersionManager()

    class Meta:
        unique_together = "analysis", "title"
        ordering = ("-title",)

    def __str__(self) -> str:
        return f"{self.analysis.title} v{self.title}"

    def get_interface(self):
        try:
            return settings.ANALYSIS_INTERFACES[self.analysis.title][self.title]
        except KeyError:
            raise NotImplementedError(f"No interface detected for {self}!")

    def get_interface_initialization_kwargs(self, **kwargs) -> dict:
        return {
            key: value
            for key, value in kwargs.items()
            if not self.input_definitions.get(key=key).run_method_input
        }

    def get_run_method_kwargs(self, **kwargs) -> dict:
        return {
            key: value
            for key, value in kwargs.items()
            if self.input_definitions.get(key=key).run_method_input
        }

    def run_interface(self, **kwargs):
        interface = self.get_interface()
        init_kwargs = self.get_interface_initialization_kwargs(**kwargs)
        instance = interface(**init_kwargs)
        run_method = getattr(instance, self.run_method_key)
        run_method_kwargs = {
            **self.fixed_run_method_kwargs,
            **self.get_run_method_kwargs(**kwargs),
        }
        if run_method_kwargs:
            return run_method(**run_method_kwargs)
        return run_method()

    def extract_results(self, results) -> dict:
        for nested_attribute in self.nested_results_parts:
            results = getattr(results, nested_attribute)
        return results if isinstance(results, dict) else results()

    def run(self, **kwargs) -> dict:
        self.input_specification.validate_kwargs(**kwargs)
        raw_results = self.run_interface(**kwargs)
        return self.extract_results(raw_results)

    def update_input_with_defaults(self, **kwargs) -> dict:
        configuration = self.input_specification.default_configuration.copy()
        configuration.update(kwargs)
        return configuration

    @property
    def nested_results_parts(self) -> list:
        return (
            self.nested_results_attribute.split(".")
            if self.nested_results_attribute
            else []
        )

    @property
    def input_definitions(self) -> models.QuerySet:
        return self.input_specification.input_definitions

    @property
    def output_definitions(self) -> models.QuerySet:
        return self.output_specification.output_definitions
