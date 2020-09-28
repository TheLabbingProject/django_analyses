Pipeline Execution
==================

Pipelines are executed using a :class:`~django_analyses.pipeline_runner.PipelineRunner`
instance, which wraps-up all the required logic.

We will use the *"Simple Pipeline"* created in the
:ref:`user_guide/pipeline_generation/simplified_example:Simplified Pipeline Generation Example`
to calculate :math:`3^{2^2}`.

.. code-block:: python

    >>> from django_analyses.pipeline_runner import PipelineRunner
    >>> pipeline = Pipeline.objects.get(title="Simple Pipeline")
    >>> pipeline_runner = PipelineRunner(pipeline)
    >>> runs = pipeline_runner.run(inputs={"base": 2})

The returned :obj:`runs` variable is a :obj:`dict` instance containing the
pipeline's nodes as keys and runs as values. Examining :obj:`runs` will show
that :math:`2^2` returned :obj:`Run #1` (which was created at the beginning of
the pipeline generation tutorial), whereas :math:`3^4` was a novel calculation
and therefore a new run has been was created.

Finally, to view our output:

.. code-block:: python

    >>> from django_analyses.models.analysis_version import AnalysisVersion
    >>> raise_3 = AnalysisVersion.objects.get(analysis__title="Exponentiation").first()
    >>> runs[raise_3].get_output("result")
    81