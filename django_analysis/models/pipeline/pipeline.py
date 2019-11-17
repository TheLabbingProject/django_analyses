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

    def execute_node(self, node: Node, inputs: dict):
        run = node.run(inputs)
        output_pipes = self.pipe_set.filter(source=node)
        next_nodes = set(output_pipes.values_list("destination", flat=True))
        for node_id in next_nodes:
            node = Node.objects.get(id=node_id)
            node_pipes = output_pipes.filter(destination=node)
            node_inputs = {
                pipe.destination_port.key: [
                    o
                    for o in run.output_set
                    if o.definition.key == pipe.source_port.key
                ][0].value
                for pipe in node_pipes
            }
            self.execute_node(node, node_inputs)
        return run

    def new_run(self, inputs: dict):
        runs = {node.id: None for node in self.node_set}
        for node in self.entry_nodes:
            node_inputs = inputs.get(node.id, inputs)
            runs[node.id] = node.run(node_inputs)
        while not all(runs.values()):
            pending = {key: value for key, value in runs.items() if not value}
            for node_id in pending:
                node = Node.objects.get(id=node_id)
                input_pipes = self.pipe_set.filter(destination=node)
                node_inputs = {
                    pipe.destination_port.key: [
                        output.value
                        for output in runs[pipe.source.id].output_set
                        if output.definition.key == pipe.source_port.key
                    ][0]
                    for pipe in input_pipes
                }
                has_dependencies = all(
                    [runs[required_node.id] for required_node in node.required_nodes]
                )
                if has_dependencies:
                    pass

    def run(self, inputs: dict):
        for node in self.entry_nodes:
            node_inputs = inputs.get(node.id, inputs)
            run = self.execute_node(node, node_inputs)
        return run

    @property
    def node_set(self) -> QuerySet:
        return self.get_node_set()

    @property
    def entry_nodes(self) -> list:
        return self.get_entry_nodes()
