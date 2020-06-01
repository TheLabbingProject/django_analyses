Simplified Example
==================

As a simple example for a pipeline generation flow, we will reuse the
:class:`ExponentCalculator` from the
:ref:`user_guide/analysis_integration/simplified_example:Simplified Analysis Integration Example`
to create a pipeline which which computes :math:`3^{x^2}` (where :math:`x`
is the provided input).

Nodes
-----

A :class:`~django_analyses.models.pipeline.node.Node` instance provides a
reference to a particular configuration of some analysis version.

First we need to create a :obj:`square` node:

.. code-block:: python

    >>> from django_analyses.models import AnalysisVersion, Node

    # Querying the database for our desired analysis version
    >>> exponent_calculation = AnalysisVersion.objects.get(
    >>>     analysis__title="Exponentiation", title="built-in"
    >>> )

    # Creating a 'square' node
    >>> configuration = {"exponent": 2}
    >>> square = Node.objects.create(
    >>>     analysis_version=exponent_calculation, configuration=configuration
    >>> )

Now, we could use our :obj:`square` node to calculate :math:`2^2`:

.. code-block:: python

    >>> run_1 = square.run(inputs={"base": 2})
    >>> run_1
    <Run: #1 Exponentiation vbuilt-in run from 2020-01-01 00:00:00.000000>
    >>> run_1.output_set.get(key='result').value
    4

Each run will be recorded in the database and returned whenver we call
:class:`ExponentCalculator` with the same parameters.

.. code-block:: python

    >>> run_2 = square.run(inputs={"base": 2})
    >>> run_1 == run_2
    # True

We also need a :obj:`raise_3` node for our pipeline:

.. code-block:: python

    >>> raise_3 = Node.objects.create(analysis_version=exponent_calculation, configuration={"base": 3})

Pipes
-----

A :class:`~django_analyses.models.pipeline.pipe.Pipe` instance is used to stream data
across runs by associating one given node's output with another's input.

In our case, the required pipe is represented by the arrow connecting :obj:`square`\'s
result and :obj:`raise_3`\'s exponent.

.. image:: ../../_static/simple-pipeline.png

First we create the :class:`~django_analyses.models.pipeline.pipeline.Pipeline`
instance:

.. code-block:: python

    >>> from django_analyses.models import Pipeline
    >>> pipeline = Pipeline.objects.create(
    >>>     title="Simple Pipeline", description="A simple pipeline."
    >>> )

And then we can lay down the pipe:

.. code-block:: python

    >>> from django_analyses.models import Pipe

    # Querying the required InputDefinition instances
    >>> square_output = exponent_calculation.output_definitions.get(key="result")
    >>> raise_3_input = exponent_calculation.input_definitions.get(key="exponent")

    # Create the pipe
    >>> pipe = Pipe.objects.create(
    >>>     pipeline=pipeline,
    >>>     source=square,
    >>>     base_source_port=square_output,
    >>>     destination=raise_3,
    >>>     base_destination_port=raise_3_input,
    >>> )

Pipeline Execution
------------------

Pipelines are executed using a :class:`~django_analyses.pipeline_runner.PipelineRunner`
instance, which wraps-up all the required logic.

We will now use our brand new *"Simple Pipeline"* to calculate :math:`3^{2^2}`.

.. code-block:: python

    >>> from django_analyses.pipeline_runner import PipelineRunner
    >>> pipeline = Pipeline.objects.get(title="Simple Pipeline")
    >>> pipeline_runner = PipelineRunner(pipeline)
    >>> runs = pipeline_runner.run(inputs={"base": 2})

The returned :obj:`runs` variable is a :obj:`dict` instance containing the pipeline's
nodes as keys and runs as values. Examining :obj:`runs` will show that :math:`2^2`
returned :obj:`Run #1`, the same run created the beginning of this tutorial, whereas
:math:`3^4` was a novel calculation and therefore a new run has been was created.

Finally, to view our output:

.. code-block:: python

    >>> runs[raise_3].output_set.get(key="result").value
    81