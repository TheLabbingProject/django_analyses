from django_analysis.models.pipeline.node import Node
from django_extensions.db.models import TitleDescriptionModel, TimeStampedModel


class Pipeline(TitleDescriptionModel, TimeStampedModel):
    pass

    def get_origin(self) -> Node:
        sources = list(self.pipe_set.values_list("source", flat=True))
        possible = [
            source for source in sources if not self.pipe_set.filter(destination=source)
        ]
        return Node.objects.get(id=possible[0])

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

    def run(self, inputs: dict):
        origin = self.get_origin()
        return self.execute_node(origin, inputs)
