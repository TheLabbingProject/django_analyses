from django.core.exceptions import ObjectDoesNotExist
from django.db import models
from django_analyses.models.input.input_specification import InputSpecification
from django_analyses.models.output.output_specification import OutputSpecification


class AnalysisVersionManager(models.Manager):
    def get_by_string_id(self, string_id: str):
        n_parts = len(string_id.split("."))
        if n_parts == 1:
            versions = self.filter(analysis__title=string_id)
            if versions:
                return versions.first()
            raise self.model.DoesNotExist(
                f"No versions found for analysis {string_id}."
            )
        elif n_parts == 2:
            analysis_title, title = string_id.split(".")
            return self.get(analysis__title=analysis_title, title=title)

    def get_kwargs_from_definition(self, analysis, definition: dict) -> dict:
        (
            input_specification,
            created_input_spec,
        ) = InputSpecification.objects.from_dict(analysis, definition["input"])
        (
            output_specification,
            created_output_spec,
        ) = OutputSpecification.objects.from_dict(analysis, definition["output"])
        return {
            "analysis": analysis,
            "title": definition.get("title", "1.0.0"),
            "description": definition.get("description"),
            "input_specification": input_specification,
            "output_specification": output_specification,
            "run_method_key": definition.get("run_method_key", "run"),
            "fixed_run_method_kwargs": definition.get("fixed_run_method_kwargs", {}),
            "nested_results_attribute": definition.get("nested_results_attribute"),
        }

    def from_dict(self, analysis, definition: dict):
        title = definition.get("title", "1.0.0")
        kwargs = self.get_kwargs_from_definition(analysis, definition)
        try:
            existing = self.get(analysis=analysis, title=title)
        except ObjectDoesNotExist:
            return self.create(**kwargs), True
        else:
            updated = False
            for key, value in kwargs.items():
                if getattr(existing, key) != value:
                    setattr(existing, key, value)
                    updated = True
            if updated:
                existing.save()
            return existing, False

    def from_list(self, analysis, definitions: list) -> dict:
        results = {}
        for version_definition in definitions:
            version, created = self.from_dict(analysis, version_definition)
            results[version.title] = {"model": version, "created": created}
        return results
