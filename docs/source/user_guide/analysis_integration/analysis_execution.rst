Analysis Execution
==================

One-off Execution
-----------------

To execute the `ExponentCalculator` interface we created in the
:ref:`user_guide/analysis_integration/simplified_example:Simplified Analysis Integration Example`,
we could run:

.. code-block:: python

    >>> analysis = Analysis.objects.get(title="Exponentiation")
    >>> analysis_version = analysis.version_set.get(title="built-in")
    >>> kwargs = {"base": 2, "exponent": 10}
    >>> results = analysis_version.run(**kwargs)
    >>> results
    {'result': 1024.0}

This will run the associated interface, however, it will not create any record
of this run in the database.

Node Execution
--------------

To execute a particular analysis version and record the run (as well as any
inputs and outputs) in the database, we must run it as a node. Again, we will
use a node previously created in the
:ref:`user_guide/pipeline_generation/simplified_example:Simplified Pipeline Generation Example`:

.. code-block:: python

    >>> configuration = {"exponent": 2}
    >>> node = Node.objects.get(
    ...     analysis_version=analysis_version,
    ...     configuration=configuration,
    ... )
    >>> inputs = {"base": 4.5}
    >>> results = node.run(inputs=inputs)

This time, our `results` are a :class:`~django_analyses.models.run.Run` instance
which is associated with all the recorded inputs and outputs:

.. code-block:: python

    >>> results
    <Run: #1 Exponentiation vbuilt-in run from 2020-01-01 00:00:00.000000>
    >>> results.input_set
    <InheritanceQuerySet [<FloatInput: 'base' = 4.5>, <FloatInput: 'exponent' = 2.0>]>
    >>> results.output_set
    <InheritanceQuerySet [<FloatOutput: 'result' = 20.25>]>
    >>> results.get_output("result")
    20.25

Node Iteration
..............

To run a node multiple types, simply provide the
:meth:`~django_analyses.models.pipeline.node.Node.run` method's `inputs`
parameter a list or tuple of input dictionaries, e.g.:

.. code-block:: python

    >>> inputs = [{"base": 1}, {"base": 2}, {"base": 3}]
    >>> results = node.run(inputs=inputs)
    >>> results
    [<Run: #2 Exponentiation vbuilt-in run from 2020-01-01 00:00:01.000000>,
     <Run: #3 Exponentiation vbuilt-in run from 2020-01-01 00:00:02.000000>,
     <Run: #4 Exponentiation vbuilt-in run from 2020-01-01 00:00:03.000000>]
