from django.db.models import QuerySet
from django_analysis.models.pipeline.node import Node
from django_extensions.db.models import TitleDescriptionModel, TimeStampedModel


class Pipeline(TitleDescriptionModel, TimeStampedModel):
    pass

    def get_node_set(self) -> QuerySet:
        source_node_ids = list(self.pipe_set.values_list("source", flat=True))
        destination_node_ids = list(self.pipe_set.values_list("destination", flat=True))
        node_ids = set(source_node_ids + destination_node_ids)
        return Node.objects.filter(id__in=node_ids)

    def get_entry_nodes(self) -> Node:
        return [node for node in self.node_set if node.required_nodes is None]

    def run(self, inputs: dict):
        runs = {node: None for node in self.node_set}
        for node in self.entry_nodes:
            node_inputs = inputs.get(node, inputs)
            runs[node] = node.run(node_inputs)
        while not all(runs.values()):
            pending = {key: value for key, value in runs.items() if not value}
            for node in pending:
                required_runs = [
                    runs[required_node] for required_node in node.required_nodes
                ]
                if all(required_runs):
                    input_pipes = self.pipe_set.filter(destination=node)
                    node_inputs = {
                        pipe.destination_port.key: [
                            output.value
                            for output in runs[pipe.source].output_set
                            if output.definition.key == pipe.source_port.key
                        ][0]
                        for pipe in input_pipes
                    }
                    runs[node] = node.run(node_inputs)
        return runs

    @property
    def node_set(self) -> QuerySet:
        return self.get_node_set()

    @property
    def entry_nodes(self) -> list:
        return self.get_entry_nodes()
