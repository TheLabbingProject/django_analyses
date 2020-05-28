Simplified Analysis Integration Example
---------------------------------------

In this example we will add an :class:`ExponentCalculator` class and integrate it into
*django_analyses*.

Interface Creation
..................

By default, interfaces are expected to be classes and expose a :meth:`run()` method which
returns a dictionary of output keys and values. Therefore, an :class:`ExponentCalculator`
class might look something like this:

.. code-block:: python
    :caption: exponent_calculator.py

    class ExponentCalculator:
        def __init__(self, base: float, exponent: float):
            self.base = base
            self.exponent = exponent

        def run(self) -> dict:
            return {"result": self.base ** self.exponent}


Analysis Creation
.................

The :class:`ExponentCalculator` class is one possible implementation of exponentiation.
Let's define this procedure as a new available analysis:

.. code-block:: python

    >>> from django_analyses.models import Analysis
    >>> definition = {
    >>>     "title": "Exponentiation",
    >>>     "description": "Calculate <base> in the power of <exponent>.",
    >>> }
    >>> analysis = Analysis.objects.create(**definition)

Analysis Version Creation
.........................

Now, we can create an :class:`~django_analyses.models.analysis_version.AnalysisVersion`
instance to represent the :class:`ExponentCalculator` class we've created:

.. code-block:: python

    >>> from django_analyses.models import AnalysisVersion
    >>> definition = {
    >>>     "title": "built-in",
    >>>     "description": "Calculate the exponent of a number using Python's built-in power operator.",
    >>> }
    >>> analysis_version = AnalysisVersion.objects.create(**definition)


Input Specification
...................

The :class:`ExponentCalculator` class expects two :obj:`float` type input values which are
assigned in its initialization: :attr:`base` and :attr:`exponent`.

:class:`~django_analyses.models.input.input_specification.InputSpecification` instances are
created with an association to a specific :class:`~django_analyses.models.analysis.Analysis`
(this prevents name clashes between input or output definitions for different analyses)
and may be used for a number of its
:class:`~django_analyses.models.analysis_version.AnalysisVersion` instances.

.. code-block:: python

    >>> from django_analyses.models import FloatInputDefinition, InputSpecification
    >>> definition = {
    >>>     "base": {
    >>>         "type": FloatInputDefinition,
    >>>         "required": True,
    >>>         "description": "Floating point number to be raised by <exponent>.",
    >>>     },
    >>>     "exponent": {
    >>>         "type": FloatInputDefinition,
    >>>         "required": True,
    >>>         "description": "Floating point number to raise <base> by.",
    >>>     },
    >>> }
    >>> analysis = Analysis.objects.get(title="Exponentiation")
    >>> input_specification, created = InputSpecification.objects.from_dict(analysis, definition)
    >>> input_specification
    <InputSpecification:
    [Exponentiation]
        base                                    Float
        exponent                                Float
    >
    >>> created
    True

Output Specification
....................

The :class:`~django_analyses.models.output.output_specification.OutputSpecification`
may be created very similarly:

.. code-block:: python

    >>> from django_analyses.models import FloatOutputDefinition, OutputSpecification
    >>> definition = {
    >>>     "result": {
    >>>         "type": FloatOutputDefinition,
    >>>         "description": "Product of <base> multiplied <exponent> times.",
    >>>     }
    >>> }
    >>> analysis = Analysis.objects.get(title="Exponentiation")
    >>> output_specification, created = OutputSpecification.objects.from_dict(analysis, definition)
    >>> output_specification
    <OutputSpecification
    [Exponentiation]
        result                                  Float
    >
    >>> created
    True

Interface Integration
.....................

At this stage our new analysis is ready to be "plugged-in". Interfaces are queried from
the :code:`ANALYSIS_INTERFACES` dictionary in the project's *settings.py*. Analyses are
expected to be registered as
:code:`ANALYSIS_INTERFACES["analysis_title"]["analysis_version_title"]`, so in our case:

.. code-block:: python
    :caption: settings.py

    from exponent_calculator import ExponentCalculator

    ...

    ANALYSIS_INTERFACES = {"Exponentiation": {"built-in": ExponentCalculator}}