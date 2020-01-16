from django.db import models
from django_analyses.models.input.definitions.input_definition import InputDefinition
from django_analyses.models.output.definitions.output_definition import OutputDefinition


class Pipe(models.Model):
    pipeline = models.ForeignKey("django_analyses.Pipeline", on_delete=models.CASCADE)

    source = models.ForeignKey(
        "django_analyses.Node", on_delete=models.PROTECT, related_name="pipe_source_set"
    )
    base_source_port = models.ForeignKey(
        "django_analyses.OutputDefinition", on_delete=models.PROTECT
    )

    destination = models.ForeignKey(
        "django_analyses.Node",
        on_delete=models.PROTECT,
        related_name="pipe_destination_set",
    )
    base_destination_port = models.ForeignKey(
        "django_analyses.InputDefinition", on_delete=models.PROTECT
    )

    def __str__(self) -> str:
        source_analysis = self.source.analysis_version.analysis
        source_key = self.base_source_port.key
        destination_analysis = self.destination.analysis_version.analysis
        destination_key = self.base_destination_port.key
        return f"{source_analysis} [{source_key}] --> [{destination_key}] {destination_analysis}"

    @property
    def source_port(self) -> OutputDefinition:
        return OutputDefinition.objects.select_subclasses().get(
            id=self.base_source_port.id
        )

    @property
    def destination_port(self) -> InputDefinition:
        return InputDefinition.objects.select_subclasses().get(
            id=self.base_destination_port.id
        )
