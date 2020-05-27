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
    exponent = AnalysisVersion.objects.get(
        analysis__title="Exponentiation", title="built-in"
    )

    # Creating a 'square' node
    configuration = {"exponent": 2}
    square = Node.objects.create(analysis_version=exponent, configuration=configuration)

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