from django.db import models
from django_analysis.models.analysis_version import AnalysisVersion
from django_extensions.db.models import TitleDescriptionModel, TimeStampedModel


class AnalysisManager(models.Manager):
    def from_dict(self, definition: dict) -> tuple:
        # Analysis creation
        title = definition["title"]
        description = definition.get("description")
        analysis, created = self.get_or_create(title=title, description=description)

        # Versions creation
        versions = definition.get("versions", [])
        versions_created = AnalysisVersion.objects.from_list(analysis, versions)

        return analysis, created, versions_created

    def from_list(self, definitions: list) -> dict:
        results = {}
        for analysis_definition in definitions:
            analysis, created, versions = self.from_dict(analysis_definition)
            results[analysis.title] = {
                "model": analysis,
                "created": created,
                "versions": versions,
            }

        return results


class Analysis(TitleDescriptionModel, TimeStampedModel):

    objects = AnalysisManager()

    def __str__(self) -> str:
        return self.title

    def get_latest_version(self) -> AnalysisVersion:
        return self.analysis_version_set.last()
