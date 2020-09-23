"""
Definition of the :class:`PipelineRunner` class.
"""

from django.db.models import QuerySet
from django_analyses.models.pipeline.node import Node
from django_analyses.models.pipeline.pipe import Pipe
from django_analyses.models.pipeline.pipeline import Pipeline
from django_analyses.models.input.definitions.list_input_definition import (
    ListInputDefinition,
)


class PipelineRunner:
    """
    Manages the execution of pipelines.
    """

    def __init__(self, pipeline: Pipeline, quiet: bool = False):
        """
        Moderates the execution of a pipeline by iterating through the nodes
        and checking whether all required inputs are available.

        Parameters
        ----------
        pipeline : Pipeline
            The pipeline to be executed
        quiet : bool
            Whether to print node execution start and end to the console or not
        """

        self.pipeline = pipeline
        self.runs = {node: None for node in self.pipeline.node_set}
        self.quiet = quiet

    def get_incoming_pipes(self, node: Node) -> QuerySet:
        """
        Returns all pipes in the pipeline that declare the given node instance
        as their destination.

        Parameters
        ----------
        node : Node
            Destination node

        Returns
        -------
        QuerySet
            Pipes with the provided node as destination
        """

        return self.pipeline.pipe_set.filter(destination=node)

    def get_destination_kwarg(self, pipe: Pipe) -> dict:
        """
        Composes a keyword argument to include in a destination node's
        configuration.

        Parameters
        ----------
        pipe : Pipe
            A pipe with an existing run matching its source node

        Returns
        -------
        dict
            Destination node keyword argument
        """

        source_outputs = self.runs[pipe.source].output_set
        key = pipe.destination_port.key
        # Find the source node's output the will be used as the destination
        # node's input.
        try:
            value = [
                output.value
                for output in source_outputs
                if output.key == pipe.source_port.key
            ][0]
        except IndexError:
            raise RuntimeError(
                f"Failed to find {key} in source node outputs!\nSource node:{pipe.source}\nSource outputs: {source_outputs}"
            )
        # Return as keyword argument.
        return {key: value}

    def get_node_inputs(self, node: Node, user_inputs: dict = None) -> dict:
        """
        Returns the node's input configuration, including inputs specified by
        the user and preceding nodes' outputs.

        Parameters
        ----------
        node : Node
            Node for which to compose an input configuration
        user_inputs : dict, optional
            Inputs provided by the user, by default None

        Returns
        -------
        dict
            Input configuration
        """

        input_pipes = self.get_incoming_pipes(node)
        kwargs = user_inputs or {}
        # In case there are destination ports that expect a list of separately
        # generated inputs, pipes are ordered by the (optional) *index* field.
        for pipe in input_pipes.order_by("index"):
            kwarg = self.get_destination_kwarg(pipe)
            key, value = list(kwarg.items())[0]
            # Handle list inputs by creating or appending to a list.
            if isinstance(pipe.destination_port, ListInputDefinition):
                try:
                    kwargs[key].append(value)
                except KeyError:
                    kwargs[key] = [value]
            # Otherwise just update the input configuration.
            else:
                kwargs[key] = value
        return kwargs

    def run_entry_nodes(self, inputs: dict) -> None:
        """
        Runs the "entry" nodes of the pipeline, i.e. nodes that are not the
        destination of any other node.

        Parameters
        ----------
        inputs : dict
            Input configurations to be passed to the nodes, this may either be
            provided as a dictionary with nodes as keys and configurations as
            values or simply an input configuration if there's only one entry
            node
        """

        for node in self.pipeline.entry_nodes:
            node_inputs = inputs.get(node, inputs)
            if isinstance(node_inputs, list):
                self.runs[node] = []
                for i, inputs in enumerate(node_inputs):
                    if not self.quiet:
                        message = f"Running {node.analysis_version} ({i})".ljust(
                            80, "."
                        )
                        print(message, end="", flush=True)
                    self.runs[node].append(node.run(inputs))
                    if not self.quiet:
                        print("done!")
            else:
                if not self.quiet:
                    message = f"Running {node.analysis_version}".ljust(80, ".")
                    print(message, end="", flush=True)
                self.runs[node] = node.run(node_inputs)
                if not self.quiet:
                    print("done!")

    def has_required_runs(self, node: Node) -> bool:
        """
        Checks whether the provided node is ready to be run by evaluating
        the execution state of the nodes it requires (nodes that generate
        output meant to be piped to it).

        Parameters
        ----------
        node : Node
            Node to evaluate

        Returns
        -------
        bool
            Whether all required nodes have been executed or not
        """

        required_runs = [
            self.runs[required_node] for required_node in node.required_nodes
        ]
        return all(required_runs)

    def run_node(self, node: Node, user_inputs: dict = None) -> None:
        """
        Runs the provided node and stores the created
        :class:`~django_analyses.models.run.Run` instances in the class's
        :attr:`runs` attribute.

        Parameters
        ----------
        node : Node
            Node to be executed
        user_inputs : dict, optional
            Inputs provided by the user at execution, by default None
        """

        node_inputs = self.get_node_inputs(node, user_inputs)
        if not self.quiet:
            message = f"Running {node.analysis_version}".ljust(80, ".")
            print(message, end="", flush=True)
        self.runs[node] = node.run(node_inputs)
        if not self.quiet:
            print("done!")

    def run(self, inputs: dict) -> dict:
        """
        Runs :attr:`pipeline` with the provided *inputs*.

        Parameters
        ----------
        inputs : dict
            Input configurations to be passed to the nodes, this may either be
            provided as a dictionary with nodes as keys and configurations as
            values or simply an input configuration if there's only one entry
            node

        Returns
        -------
        dict
            Resulting run instances
        """

        self.runs = {node: None for node in self.pipeline.node_set}
        self.run_entry_nodes(inputs)
        while self.pending_nodes:
            for node in self.pending_nodes:
                if self.has_required_runs(node):
                    user_inputs = inputs.get(node)
                    self.run_node(node, user_inputs)
        return self.runs

    @property
    def pending_nodes(self) -> list:
        """
        Nodes that were not yet executed.

        Returns
        -------
        list
            Pending nodes
        """

        return [key for key in self.runs if not self.runs[key]]
