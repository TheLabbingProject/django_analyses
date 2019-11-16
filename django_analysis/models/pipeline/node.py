from django.contrib.postgres.fields import JSONField
from django.db import models
from django_analysis.models.run import Run


class Node(models.Model):
    analysis_version = models.ForeignKey(
        "django_analysis.AnalysisVersion", on_delete=models.PROTECT
    )
    configuration = JSONField()

    def run(self, inputs: dict) -> Run:
        run_configuration = self.configuration.copy()
        run_configuration.update(inputs)
        return Run.objects.get_or_execute(self.analysis_version, **run_configuration)
