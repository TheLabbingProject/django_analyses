Pipeline Generation
===================

:class:`~django_analyses.models.pipeline.pipeline.Pipeline` instances represent
a distinct association pattern between the outputs and inputs of pre-configured
analyses.

Nodes
-----

A :class:`~django_analyses.models.pipeline.node.Node` instance provides a
reference to a particular configuration of some analysis version.

As an example, let's use the :class:`ExponentCalculator` from the
:doc:`analysis_integration` tutorial to create a :obj:`square` node.

.. code-block:: python

    from django_analyses.models import AnalysisVersion, Node

    # Querying the database for our desired analysis version
    exponent_calculation = AnalysisVersion.objects.get(
        analysis__title="Exponentiation", title="built-in"
    )

    # Creating a 'square' node
    configuration = {"exponent": 2}
    square = Node.objects.create(
        analysis_version=exponent_calculation, configuration=configuration
    )

Let's use our :obj:`square` node to calculate :math:`2^2`:

.. code-block:: python

    run_1 = square.run(inputs={"base": 2})

    run_1
    # <Run: #1 Exponentiation vbuilt-in run from 2020-01-01 00:00:00.000000>

    run_1.output_set.get(key='result').value
    # 4

Now that we've created the :obj:`square` node, each run will be recorded in the database
and returned whenver we call :class:`ExponentCalculator` with the same parameters.

.. code-block:: python

    run_2 = square.run(inputs={"base": 2})

    run_1 == run_2
    # True

Pipelines
---------

A :class:`~django_analyses.models.pipeline.pipe.Pipe` instance is used to stream data
across runs by associating one given node's output with another's input. To keep this
example as simple as possible, we will reuse :class:`ExponentCalculator` to calculate
:math:`3^{x^2}` (where :math:`x` is the provided input).

.. image:: ../_static/simple-pipeline.png

First we'll create the pipeline and then add the pipe (that arrow connecting
:obj:`square`\s result and :obj:`raise_3`\s exponent):

.. code-block:: python

    from django_analyses.models import AnalysisVersion, Node, Pipe, Pipeline

    # Create a Pipeline instance
    pipeline = Pipeline.objects.create(
        title="Simple Pipeline", description="A simple pipeline."
    )

    # Querying the database for our desired analysis version
    exponent_calculation = AnalysisVersion.objects.get(
        analysis__title="Exponentiation", title="built-in"
    )

    # Retrieving previously create 'square' node
    square = Node.objects.get(
        analysis_version=exponent_calculation, configuration__exponent=2
    )

    # Creating new 3^<exponent> node
    raise_3 = Node.objects.create(analysis_version=exponent_calculation, configuration={"base": 3})

    # Querying the required InputDefinition instances
    square_output = exponent.output_definitions.get(key="result")
    raise_3_input = exponent.input_definitions.get(key="exponent")

    # Creating the pipe
    pipe = Pipe.objects.create(
        pipeline=pipeline,
        source=square,
        base_source_port=square_output,
        destination=raise_3,
        base_destination_port=raise_3_input,
    )
