from django.db.models import QuerySet
from django_analyses.models.pipeline.node import Node
from django_analyses.models.pipeline.pipe import Pipe
from django_analyses.models.pipeline.pipeline import Pipeline
from django_analyses.models.input.definitions.list_input_definition import (
    ListInputDefinition,
)


class PipelineRunner:
    def __init__(self, pipeline: Pipeline):
        self.pipeline = pipeline
        self.runs = {node: None for node in pipeline.node_set}

    def get_incoming_pipes(self, node: Node) -> QuerySet:
        return self.pipeline.pipe_set.filter(destination=node)

    def get_destination_kwarg(self, pipe: Pipe) -> dict:
        source_outputs = self.runs[pipe.source].output_set
        key = pipe.destination_port.key
        value = [
            output.value
            for output in source_outputs
            if output.key == pipe.source_port.key
        ][0]
        return {key: value}

    def get_node_inputs(self, node: Node, user_inputs: dict = None) -> dict:
        input_pipes = self.get_incoming_pipes(node)
        kwargs = user_inputs or {}
        for pipe in input_pipes.order_by("index"):
            kwarg = self.get_destination_kwarg(pipe)
            key, value = list(kwarg.items())[0]
            if isinstance(pipe.destination_port, ListInputDefinition):
                try:
                    kwargs[key].append(value)
                except KeyError:
                    kwargs[key] = [value]
            else:
                kwargs[key] = value
        return kwargs

    def run_entry_nodes(self, inputs: dict) -> None:
        for node in self.pipeline.entry_nodes:
            node_inputs = inputs.get(node, inputs)
            self.runs[node] = node.run(node_inputs)

    def has_required_runs(self, node: Node) -> bool:
        required_runs = [
            self.runs[required_node] for required_node in node.required_nodes
        ]
        return all(required_runs)

    def run_node(self, node: Node, user_inputs: dict = None) -> None:
        node_inputs = self.get_node_inputs(node, user_inputs)
        self.runs[node] = node.run(node_inputs)

    def run(self, inputs: dict):
        self.run_entry_nodes(inputs)
        while self.pending_nodes:
            for node in self.pending_nodes:
                if self.has_required_runs(node):
                    user_inputs = inputs.get(node)
                    self.run_node(node, user_inputs)
        return self.runs

    @property
    def pending_nodes(self) -> list:
        return [key for key in self.runs if not self.runs[key]]
