from django.db import models
from django_analyses.models.analysis_version import AnalysisVersion
from django_analyses.models.managers import messages
from django_analyses.models.pipeline.node import Node


class PipeManager(models.Manager):
    def get_node_from_dict_definition(self, definition: dict) -> tuple:
        try:
            string_id = definition["analysis_version"]
        except KeyError:
            message = messages.NODE_DEFINITION_MISSING_ANALYSIS_VERSION.format(
                definition=definition
            )
            raise KeyError(message)
        analysis_version = AnalysisVersion.objects.get_by_string_id(string_id)
        return Node.objects.get_or_create(
            analysis_version=analysis_version,
            configuration=definition["configuration"],
        )

    def from_dict(self, pipeline, definition: dict):
        print(definition["source"])
        source, _ = self.get_node_from_dict_definition(definition["source"])
        source_port = source.analysis_version.output_definitions.get(
            key=definition["source_port"]
        )
        destination, _ = self.get_node_from_dict_definition(
            definition["destination"]
        )
        destination_port = destination.analysis_version.input_definitions.get(
            key=definition["destination_port"]
        )
        return self.create(
            pipeline=pipeline,
            source=source,
            base_source_port=source_port,
            destination=destination,
            base_destination_port=destination_port,
        )

    def from_list(self, pipeline, definitions: list):
        return [
            self.from_dict(pipeline, definition) for definition in definitions
        ]
