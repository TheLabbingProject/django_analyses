import math

from celery import group, shared_task
from django_analyses.models.pipeline.node import Node
from django_analyses.models.pipeline.pipeline import Pipeline
from django_analyses.pipeline_runner import PipelineRunner
from typing import List, Union


@shared_task(name="django_analyses.node-execution")
def execute_node(
    node_id: int, inputs: Union[list, dict]
) -> Union[int, List[int]]:
    """
    Execute a :class:`~django_analyses.models.pipeline.node.Node` in a
    dedicated, separate process.

    Parameters
    ----------
    node_id : int
        The Node instance ID to execute
    inputs : Union[list, dict]
        Inputs to pass the node

    Returns
    -------
    int, List[int]
        The created :class:`~django_analyses.models.run.Run` instance ID or IDs
    """

    node = Node.objects.get(id=node_id)

    # Handle single or multiple execution inputs.
    if isinstance(inputs, dict):
        # If a input dictionary is provided, simply run the node and return
        # the ID of the resulting run if created.
        run, created = node.run(inputs=inputs, return_created=True)
        if created:
            return run.id
    else:
        # If a list of input dictionaries is provided, run in parallel.
        max_parallel = node.analysis_version.max_parallel
        try:
            # Calculate the number of chunks according to the analysis
            # version's *max_parallel* attribute.
            n_chunks = math.ceil(len(inputs) / max_parallel)
        except ZeroDivisionError:
            # If `max_parallel` is set to 0, run all in parallel.
            return group(
                execute_node.s(node_id, input_dict) for input_dict in inputs
            )()
        else:
            # Create the inputs for each separate execution and run in chunks.
            inputs = ((node_id, input_dict) for input_dict in inputs)
            return execute_node.chunks(inputs, n_chunks)()


@shared_task(name="django_analyses.pipeline-execution")
def execute_pipeline(pipeline_id: int, inputs: dict):
    pipeline = Pipeline.objects.get(id=pipeline_id)
    runner = PipelineRunner(pipeline=pipeline)
    runner.run(inputs=inputs)
    return runner.get_safe_results()
