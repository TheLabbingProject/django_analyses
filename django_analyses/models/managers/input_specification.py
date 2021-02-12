"""
Definition of the
:class:`~django_analyses.models.managers.input_specification.InputSpecificationManager`
class.
"""

from django.db import models
from django.db.models import Count, QuerySet
from django_analyses.models.input.definitions.input_definition import \
    InputDefinition


class InputSpecificationManager(models.Manager):
    """
    Custom manager for the
    :class:`~django_analyses.models.input.input_specification.InputSpecification`
    model.
    """

    def filter_by_definitions(self, analysis, definitions: list) -> QuerySet:
        """
        Returns a queryset of input specifications that match the provided
        arguments.

        Parameters
        ----------
        analysis : ~django_analyses.models.analysis.Analysis
            The analysis with which the input specification is associated
        definitions : list
            Input definitions contained in the queried specification

        Returns
        -------
        QuerySet
            Matching input specifications
        """

        possibly_same = self.filter(
            analysis=analysis, base_input_definitions__in=definitions
        )
        return possibly_same.annotate(
            base_input_definitions__count=Count("base_input_definitions")
        ).filter(base_input_definitions__count=len(definitions))

    def from_dict(self, analysis, specification: dict) -> tuple:
        """
        Creates a new input specification from a dictionary of input
        definitions.

        Parameters
        ----------
        analysis : ~django_analyses.models.analysis.Analysis
            The analysis with which the input specification will be associated
        specification : dict
            Input specification dictionary

        Returns
        -------
        Tuple[~django_analyses.models.input.input_specification.InputSpecification,
        bool]
            Input specification, created
        """

        input_definitions = InputDefinition.objects.from_specification_dict(
            specification
        )
        existing_specification = self.filter_by_definitions(
            analysis, input_definitions
        )
        if not existing_specification:
            new_specification = self.create(analysis=analysis)
            new_specification.base_input_definitions.set(input_definitions)
            return new_specification, True
        return existing_specification[0], False
