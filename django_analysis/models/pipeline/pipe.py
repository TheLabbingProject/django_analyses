from django.db import models
from django_analysis.models.input.definitions.input_definition import InputDefinition
from django_analysis.models.output.definitions.output_definition import OutputDefinition


class Pipe(models.Model):
    pipeline = models.ForeignKey("django_analysis.Pipeline", on_delete=models.CASCADE)

    source = models.ForeignKey(
        "django_analysis.Node", on_delete=models.PROTECT, related_name="pipe_source_set"
    )
    base_source_port = models.ForeignKey(
        "django_analysis.OutputDefinition", on_delete=models.PROTECT
    )

    destination = models.ForeignKey(
        "django_analysis.Node",
        on_delete=models.PROTECT,
        related_name="pipe_destination_set",
    )
    base_destination_port = models.ForeignKey(
        "django_analysis.InputDefinition", on_delete=models.PROTECT
    )

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
