"""
Definition of the :class:`PipelineRunner` class.
"""

import json
from typing import Any, Dict, List, Union

from django.db.models import QuerySet
from django_analyses.models.input.definitions.list_input_definition import \
    ListInputDefinition
from django_analyses.models.pipeline.node import Node
from django_analyses.models.pipeline.pipe import Pipe
from django_analyses.models.pipeline.pipeline import Pipeline
from django_analyses.utils.messages import (BAD_SOURCE_PORT,
                                            BAD_USER_INPUT_KEYS,
                                            BAD_USER_NODE_INPUT_TYPE,
                                            FAILED_NODE_RUN,
                                            MISSING_ENTRY_POINT_INPUTS,
                                            NODE_RUN_FINISHED, NODE_RUN_START)


class PipelineRunner:
    """
    Manages the execution of pipelines.
    """

    _RUN_SEP = "─" * 20

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
        self.quiet = quiet
        self.reset_runs_dict()

    def reset_runs_dict(self) -> None:
        """
        Resets the :attr:`runs` dictionary before a new execution.
        """

        self.runs = {node: [] for node in self.pipeline.node_set}

    def standardize_user_input(
        self,
        user_input: Union[List[Dict[str, Any]], Dict[Union[str, Node], Any]],
    ) -> Dict[Node, List[Dict[str, Any]]]:
        """
        Standardizes user input to conform with the desired format (a
        dictionary with nodes as keys and list of input dictionaries as
        values).

        Parameters
        ----------
        user_input : Union[List[Dict[str, Any]], Dict[Union[str, Node], Any]]
            User input as either a dictionary of nodes and their input
            dictionaries, or an input dictionary (or list of input
            dictionaries) specified for a singular entry node

        Returns
        -------
        Dict[Node, List[Dict[str, Any]]]
            Standardized user input
        """

        inputs = {}
        if isinstance(user_input, dict):
            node_keys = self.validate_user_input_keys(user_input)
            if node_keys:
                for node, node_inputs in user_input.items():
                    # Convert node IDs to nodes.
                    if isinstance(node, int):
                        node = Node.objects.get(id=node)
                    # Standardize as a list of input dictionaries.
                    if isinstance(node_inputs, dict):
                        inputs[node] = [node_inputs]
                    elif isinstance(node_inputs, list):
                        inputs[node] = node_inputs
                    else:
                        raise TypeError(BAD_USER_NODE_INPUT_TYPE)
            else:
                # Handles an input dictionary passed to a single entry node.
                entry_nodes = self.pipeline.entry_nodes
                if len(entry_nodes) == 1:
                    inputs = {entry_nodes[0]: [inputs]}
                else:
                    message = MISSING_ENTRY_POINT_INPUTS.format(
                        entry_points=entry_nodes
                    )
                    raise ValueError(message)
        elif isinstance(user_input, list):
            # Handles a list of input dictionaries passed to a single entry
            # node.
            entry_nodes = self.pipeline.entry_nodes
            if len(entry_nodes) == 1:
                inputs[entry_nodes[0]] = user_input
            else:
                message = MISSING_ENTRY_POINT_INPUTS.format(
                    entry_points=entry_nodes
                )
                raise ValueError(message)
        return inputs

    def validate_user_input_keys(
        self, user_input: Dict[Union[str, Node], Any]
    ) -> bool:
        """
        Validates all keys of a user input dictionary are either nodes or
        strings. Return `True` if all are nodes, `False` if all are strings,
        and raises a `ValueError` in any other case.

        Parameters
        ----------
        user_input : Dict[Union[str, Node], Any]
            User input dictionary

        Returns
        -------
        bool
            True of all keys are nodes, False if all keys are strings
        """

        keys = list(user_input.keys())
        all_nodes = all([isinstance(key, (Node, int)) for key in keys])
        if not all_nodes:
            all_strings = all([isinstance(key, str) for key in keys])
            if all_strings:
                return False
            else:
                message = BAD_USER_INPUT_KEYS.format(keys=keys)
                raise ValueError(message)
        else:
            return True

    def get_node_user_inputs(
        self,
        user_inputs: Dict[Node, List[Dict[str, Any]]],
        node: Node,
        run_index: int,
    ) -> Dict[str, Any]:
        """
        Returns the input configuration dictionary provided by the user for
        the specified node's execution.

        Parameters
        ----------
        user_inputs : Dict[Node, List[Dict[str, Any]]]
            User provided input configurations
        node : Node
            The node to look for
        run_index : int
            The index of the requested node's execution

        Returns
        -------
        Dict[str, Any]
            User provided input configuration
        """

        if node in user_inputs:
            try:
                return user_inputs[node][run_index]
            except IndexError:
                pass
        return {}

    def get_incoming_pipes(self, node: Node, run_index: int) -> QuerySet:
        """
        Returns all pipes in the pipeline that declare the given node instance
        as their destination.

        Parameters
        ----------
        node : Node
            Destination node
        run_index : int
            The desired run index of the specified node

        Returns
        -------
        QuerySet
            Pipes with the provided node as destination
        """

        return self.pipeline.pipe_set.filter(
            destination=node, destination_run_index=run_index
        )

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

        run = self.runs[pipe.source][pipe.source_run_index]
        key = pipe.destination_port.key
        # Find the source node's output the will be used as the destination
        # node's input.
        try:
            value = [
                output.value
                for output in run.output_set
                if output.key == pipe.source_port.key
            ][0]
        except IndexError:
            message = BAD_SOURCE_PORT.format(
                key=key, source=pipe.source, output_set=run.output_set
            )
            raise RuntimeError(message)
        # Return as keyword argument.
        return {key: value}

    def get_node_inputs(
        self,
        node: Node,
        user_inputs: Dict[Node, List[Dict[str, Any]]],
        run_index: int,
    ) -> dict:
        """
        Returns the node's input configuration, including inputs specified by
        the user and preceding nodes' outputs.

        Parameters
        ----------
        node : Node
            Node for which to compose an input configuration
        user_inputs : Dict[Node, List[Dict[str, Any]]]
            User provided input configurations

        Returns
        -------
        dict
            Input configuration
        """

        kwargs = self.get_node_user_inputs(user_inputs, node, run_index)
        input_pipes = self.get_incoming_pipes(node, run_index=run_index)
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

    def generate_user_inputs_string(self, user_inputs: dict) -> str:
        """
        Formats the user provided input dictionary as a readable string.

        Parameters
        ----------
        user_inputs : dict
            Standardized user provided inputs

        Returns
        -------
        str
            Formatted user provided input dictionary
        """

        formatted_user_inputs = {
            node.id: inputs for node, inputs in user_inputs.items()
        }
        return json.dumps(formatted_user_inputs, indent=4, sort_keys=True)

    def report_node_execution_start(
        self, node: Node, run_index: int, inputs: dict, first: bool = False,
    ) -> None:
        """
        Reports the start of a *node*'s execution.

        Parameters
        ----------
        node : Node
            The executed node
        run_index : int
            The index of the node's run in this pipeline
        inputs : dict
            The node's input configuration dictionary
        first : bool, optional
            Whether this is the first execution of this pipeline, by default
            False
        """

        formatted_inputs = json.dumps(inputs, indent=4)
        message = NODE_RUN_START.format(
            analysis_version=node.analysis_version,
            run_index=run_index,
            inputs=formatted_inputs,
        )
        if not first:
            message = self._RUN_SEP + message
        print(message, flush=True)

    def report_node_execution_end(self, run) -> None:
        """
        Reports the end of a *node*'s execution.

        Parameters
        ----------
        run : :class:`~django_analyses.models.run.Run`
            The created run instance
        """

        outputs = run.get_results_json()
        formatted_outputs = json.dumps(outputs, indent=4, sort_keys=True)
        message = NODE_RUN_FINISHED.format(outputs=formatted_outputs)
        print(message + self._RUN_SEP)

    def report_node_execution_failure(
        self, node: Node, user_inputs: dict, node_inputs: dict, exception: str
    ) -> None:
        """
        Reports a failure in a *node*'s execution.

        Parameters
        ----------
        node : Node
            The executed node
        user_inputs : dict
            Standardized user provided inputs
        node_inputs : dict
            The complete input configuration for this node's execution
        exception : str
            The raised exception

        Raises
        ------
        RuntimeError
            [description]
        """

        formatted_user_inputs = self.generate_user_inputs_string(user_inputs)
        formatted_node_inputs = json.dumps(
            node_inputs, indent=4, sort_keys=True
        )
        message = FAILED_NODE_RUN.format(
            node_id=node.id,
            analysis_version=node.analysis_version,
            run_index=0,
            exception=exception,
            user_inputs=formatted_user_inputs,
            node_inputs=formatted_node_inputs,
        )
        raise RuntimeError(message)

    def run_entry_nodes(
        self, user_inputs: Dict[Node, List[Dict[str, Any]]],
    ) -> None:
        """
        Runs the "entry" nodes of the pipeline, i.e. nodes that are not the
        destination of any other node.

        Parameters
        ----------
        user_inputs : Dict[Node, List[Dict[str, Any]]]
            User provided input configurations
        """

        first = True
        for node in self.pipeline.entry_nodes:
            # Get input configuration.
            node_inputs = self.get_node_user_inputs(user_inputs, node, 0)
            # Report execution start.
            if not self.quiet:
                self.report_node_execution_start(node, 0, node_inputs, first)
            # Execute.
            try:
                run = node.run(node_inputs)
            except Exception as e:
                # Report exception.
                self.report_node_execution_failure(
                    node, user_inputs, node_inputs, e
                )
            # Report execution end.
            self.runs[node].append(run)
            if not self.quiet:
                self.report_node_execution_end(run)

    def has_required_runs(self, node: Node, run_index: int) -> bool:
        """
        Checks whether the provided node is ready to be run by evaluating
        the execution state of the nodes it requires (nodes that generate
        output meant to be piped to it).

        Parameters
        ----------
        node : Node
            Node to evaluate
        run_index : int
            Filter by the index of the node's run

        Returns
        -------
        bool
            Whether all required nodes have been executed or not
        """

        preceding_nodes = node.get_required_nodes(
            pipeline=self.pipeline, run_index=run_index
        )
        for preceding_node in preceding_nodes:
            node_id = preceding_node["source"]
            run_index = preceding_node["source_run_index"]
            node = Node.objects.get(id=node_id)
            try:
                _ = self.runs[node][run_index]
            except IndexError:
                return False
        return True

    def run_node(
        self, node: Node, user_inputs: Dict[Node, List[Dict[str, Any]]],
    ) -> None:
        """
        Runs the provided node and stores the created
        :class:`~django_analyses.models.run.Run` instances in the class's
        :attr:`runs` attribute.

        Parameters
        ----------
        node : Node
            Node to be executed
        user_inputs : Dict[Node, List[Dict[str, Any]]]
            User provided input configurations
        """

        run_index = len(self.runs[node])
        node_inputs = self.get_node_inputs(node, user_inputs, run_index)
        if not self.quiet:
            self.report_node_execution_start(node, run_index, node_inputs)
        try:
            run = node.run(node_inputs)
        except Exception as e:
            self.report_node_execution_failure(
                node, user_inputs, node_inputs, e
            )
        self.runs[node].append(run)
        if not self.quiet:
            self.report_node_execution_end(run)

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

        self.reset_runs_dict()
        inputs = self.standardize_user_input(inputs)
        self.run_entry_nodes(inputs)
        while self.pending_nodes:
            for node in self.pending_nodes:
                run_index = len(self.runs[node])
                if self.has_required_runs(node, run_index):
                    self.run_node(node, inputs)
        return self.runs

    def get_safe_results(self) -> dict:
        """
        Returns a JSON-serializable dictionary of the pipeline's outputs.

        Returns
        -------
        dict
            Results dictionary with node IDs as keys a list of result
            dictionaries for each run of that node
        """

        return {
            node.id: [run.get_results_json() for run in node_runs]
            for node, node_runs in self.runs.items()
        }

    @property
    def pending_nodes(self) -> list:
        """
        Nodes that were not yet executed.

        Returns
        -------
        list
            Pending nodes
        """

        return [
            node
            for node in self.runs
            if len(self.runs[node]) != self.pipeline.count_node_runs(node)
        ]
