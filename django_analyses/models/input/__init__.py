"""
Definition of all the models required to create an input specification for
some :class:`~django_analyses.models.analysis_version.AnalysisVersion` and
keep track of the inputs associated with some
:class:`~django_analyses.models.run.Run` instance.
"""

from django_analyses.models.input.definitions import (BooleanInputDefinition,
                                                      DirectoryInputDefinition,
                                                      FileInputDefinition,
                                                      FloatInputDefinition,
                                                      IntegerInputDefinition,
                                                      ListInputDefinition,
                                                      StringInputDefinition)
from django_analyses.models.input.input import Input
from django_analyses.models.input.input_specification import InputSpecification
from django_analyses.models.input.types import (BooleanInput, DirectoryInput,
                                                FileInput, FloatInput,
                                                IntegerInput, ListInput,
                                                StringInput)
