"""
:class:`~django_analyses.models.input.definitions.input_definition.InputDefinition`
subclasses are used to create an
:class:`~django_analyses.models.input.input_specification.InputSpecification`
that may be associated with some
:class:`~django_analyses.models.analysis_version.AnalysisVersion`.
Each type of input definition is used describe some kind of input that could be
passed to associated
:class:`~django_analyses.models.analysis_version.AnalysisVersion`.
"""

from .string_input_definition import StringInputDefinition
from .integer_input_definition import IntegerInputDefinition
from .float_input_definition import FloatInputDefinition
from .file_input_definition import FileInputDefinition
from .directory_input_definition import DirectoryInputDefinition
from .boolean_input_definition import BooleanInputDefinition
from .list_input_definition import ListInputDefinition
from .tuple_input_definition import TupleInputDefinition
