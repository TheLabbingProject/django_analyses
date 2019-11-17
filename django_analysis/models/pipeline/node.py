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

    def get_required_nodes(self) -> models.QuerySet:
        node_ids = self.pipe_destination_set.values_list("source", flat=True)
        return Node.objects.filter(id__in=list(node_ids))

    def get_requiring_nodes(self) -> models.QuerySet:
        node_ids = self.pipe_source_set.values_list("destination", flat=True)
        return Node.objects.filter(id__in=list(node_ids))

    @property
    def required_nodes(self) -> models.QuerySet:
        return self.get_required_nodes() or None

    @property
    def requiring_nodes(self) -> models.QuerySet:
        return self.get_requiring_nodes() or None
