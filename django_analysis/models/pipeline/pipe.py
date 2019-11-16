from django.db import models


class Pipe(models.Model):
    pipeline = models.ForeignKey("django_analysis.Pipeline", on_delete=models.CASCADE)

    source = models.ForeignKey(
        "django_analysis.Node", on_delete=models.PROTECT, related_name="pipe_source_set"
    )
    source_port = models.ForeignKey(
        "django_analysis.OutputDefinition", on_delete=models.PROTECT
    )

    destination = models.ForeignKey(
        "django_analysis.Node",
        on_delete=models.PROTECT,
        related_name="pipe_destination_set",
    )
    destination_port = models.ForeignKey(
        "django_analysis.InputDefinition", on_delete=models.PROTECT
    )

