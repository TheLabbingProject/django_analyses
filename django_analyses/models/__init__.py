"""
Creates :class:`~django.db.models.Model` and :class:`~django.db.models.Manager`
subclasses to represent and manage all the different parts of an analysis
pipeline.

"""

from django_analyses.models.analysis import Analysis
from django_analyses.models.analysis_version import AnalysisVersion
from django_analyses.models.run import Run
from django_analyses.models.input.input import Input
from django_analyses.models.input.definitions import (
    BooleanInputDefinition,
    DirectoryInputDefinition,
    FileInputDefinition,
    FloatInputDefinition,
    IntegerInputDefinition,
    ListInputDefinition,
    StringInputDefinition,
)
from django_analyses.models.input.types import (
    BooleanInput,
    DirectoryInput,
    FileInput,
    FloatInput,
    IntegerInput,
    ListInput,
    StringInput,
)
from django_analyses.models.input.input_specification import InputSpecification
from django_analyses.models.output.output_specification import (
    OutputSpecification,
)
from django_analyses.models.output.output import Output
from django_analyses.models.output.definitions import (
    FileOutputDefinition,
    FloatOutputDefinition,
)
from django_analyses.models.output.types import FileOutput, FloatOutput
from django_analyses.models.pipeline import Node, Pipe, Pipeline
