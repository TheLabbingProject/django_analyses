.. _queryset-processing:

``QuerySet`` Processing
=======================

Minimal Exmaple
---------------

.. role:: raw-html(raw)
    :format: html

This section details the recommended procedure for creating an interface to
easily run some node in batch over a default or provided queryset of some
data-representing model.

The :class:`~django_analyses.runner.queryset_runner.QuerySetRunner` base class
provides a reusable abstraction for the general process of executing some
:class:`~django_analyses.model.pipeline.node.Node` instance with inputs
generated from a queryset.

For example, let us assume a ``Scan`` model storing data scans in the database,
and a ``"Scan Preprocessing"`` analysis of version ``"1.0"`` we would like to
routinely run with the configuration: :raw-html:`<br />`
``{"harder": True, "better": 100, "stronger": "faster"}``. :raw-html:`<br />`
In addition, we know the analysis receives the ``Scan`` model's ``path``
field's value as its ``"input_file"``.
The resulting subclass will look like:

.. code-block:: python

    from django_analyses.runner import QuerySetRunner
    from myapp.models.scan import Scan

    class ScanPreprocessingRunner(QuerySetRunner):
        DATA_MODEL = Scan
        ANALYSIS = "Scan Preprocessing"
        ANALYSIS_VERSION = "1.0"
        ANALYSIS_CONFIGURATION = {
            "harder": True,
            "better": 100,
            "stronger": "faster",
        }
        INPUT_KEY = "input_file"

        def get_instance_representation(self, instance: Scan) -> str:
            return str(instance.path)

And that's it!

.. note::

    The
    :func:`~django_analyses.runner.queryset_runner.QuerySetRunner.get_instance_representation`
    method will, if not overriden, return the instance as it is.

    Using model instances as inputs is a fairly advanced usage scenario and
    outside the scope of this tutorial, therefore, the minimal example includes
    this modification.

To run the specified node over all ``Scan`` instance in the database:

.. code-block:: python

    >>> runner = ScanPreprocessingRunner()
    >>> runner.run()
    Scan Preprocessing v1.0: Batch Execution

    🔎 Default execution queryset generation:
    Querying Scan instances...
    1000 instances found.

    ⚖ Checking execution status for the input queryset:
    Filtering existing runs...
    20 existing runs found.
    980 instances pending execution.

    🔀 Generating input specifications:
    980 input specifications prepared.

    🚀Successfully started Scan Preprocessing v1.0 execution over 980 Scan instances🚀

:class:`~django_analyses.runner.queryset_runner.QuerySetRunner` took care of
querying all instances of the ``Scan`` model, checking for pending runs,
generating the required input specifications, and running them in the
background.

To run over a particular queryset, simply pass the queryset to the
:func:`~django_analyses.runner.queryset_runner.QuerySetRunner.run` method.

Default ``QuerySet`` Filtering
------------------------------

To apply custom filtering to the data model's queryset, override the
:func:`~django_analyses.runner.queryset_runner.QuerySetRunner.filter_queryset`
method. For example, if we would like to process only scans with
``"anatomical"`` in their description:

.. code-block:: python
    :emphasize-lines: 16, 20-28

    import logging
    from django.db.models import QuerySet
    from django_analyses.runner import QuerySetRunner
    from myapp.models.scan import Scan

    class ScanPreprocessingRunner(QuerySetRunner):
        DATA_MODEL = Scan
        ANALYSIS = "Scan Preprocessing"
        ANALYSIS_VERSION = "1.0"
        ANALYSIS_CONFIGURATION = {
            "harder": True,
            "better": 100,
            "stronger": "faster",
        }
        INPUT_KEY = "input_file"
        FILTER__QUERYSET_START = "Filtering anatomical scans..."

        def get_instance_representation(self, instance: Scan) -> str:
            return str(instance.path)

        def filter_queryset(self,
            queryset: QuerySet, log_level: int = logging.INFO
        ) -> QuerySet:
            queryset = super().filter_queryset(queryset, log_level=log_level)
            self.log_filter_start(log_level)
            queryset = queryset.filter(description__icontains="anatomical")
            self.log_filter_end(n_candidates=queryset.count(), log_level=log_level)
            return queryset

This time, when we run ``ScanPreprocessingRunner``, we get the result:

.. code-block:: python
    :emphasize-lines: 8-9

    >>> runner = ScanPreprocessingRunner()
    >>> runner.run()
    Scan Preprocessing v1.0: Batch Execution

    🔎 Default execution queryset generation:
    Querying Scan instances...
    1000 instances found.
    Filtering anatomical scans...
    500 execution candidates found.

    ⚖ Checking execution status for the input queryset:
    Filtering existing runs...
    20 existing runs found.
    480 instances pending execution.

    🔀 Generating input specifications:
    480 input specifications prepared.

    🚀Successfully started Scan Preprocessing v1.0 execution over 480 Scan instances🚀

.. note::
    * Filtering is applied to provided querysets as well, not just the default.
    * ``super().filter_queryset(queryset)`` is called to apply any preceding
      filtering.
    * The log message is replaced by overriding the
      :attr:`~django_analyses.runner.queryset_runner.QuerySetRunner.FILTER_QUERYSET_START`
      class attribute (which is used automatically by
      :func:`~django_analyses.runner.queryset_runner.QuerySetRunner.filter_queryset`
      to log the filtering of the input queryset.

The :class:`~django_analyses.runner.queryset_runner.QuerySetRunner` class
provides a wide range of utility attributes and functions that enable the
automation of highly customized queryset processing. For more information,
simply follow the
:class:`~django_analyses.runner.queryset_runner.QuerySetRunner` hyperlink to
the class's reference.
