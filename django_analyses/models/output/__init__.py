"""
Definition of all the models required to create an output specification for
some :class:`~django_analyses.models.analysis_version.AnalysisVersion` and
keep track of the outputs associated with some
:class:`~django_analyses.models.run.Run` instance.
"""

from django_analyses.models.output.output_specification import (
    OutputSpecification,
)
from django_analyses.models.output.output import Output
from django_analyses.models.output.definitions import (
    FileOutputDefinition,
    FloatOutputDefinition,
)
from django_analyses.models.output.types import FileOutput, FloatOutput
