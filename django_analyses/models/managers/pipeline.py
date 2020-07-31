from django.db import models, transaction
from django_analyses.models.pipeline.pipe import Pipe


class PipelineManager(models.Manager):
    def from_dict(self, definition: dict):
        with transaction.atomic():
            pipeline = self.create(
                title=definition["title"],
                description=definition["description"],
            )
            pipes = definition.get("pipes", [])
            _ = Pipe.objects.from_list(pipeline, pipes)
        return pipeline

    def from_list(self, definitions: list) -> list:
        return [self.from_dict(definition) for definition in definitions]
