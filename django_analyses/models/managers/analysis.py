"""
Definition of a custom :class:`~django.db.models.Manager` for the
:class:`~django_analyses.models.analysis.Analysis` class.
"""

from typing import Dict, Tuple

from django.db import models
from django_analyses.models.analysis_version import AnalysisVersion


class AnalysisManager(models.Manager):
    """
    Custom :class:`~django.db.models.Manager` for the
    :class:`~django_analyses.models.analysis.Analysis` class.
    """

    def from_dict(self, definition: dict) -> Tuple[models.Model, bool, bool]:
        """
        Gets or creates an :class:`~django_analyses.models.analysis.Analysis`
        instance based on a dictionary definition.

        Parameters
        ----------
        definition : dict
            Analysis definition

        Returns
        -------
        Tuple[models.Model, bool, bool]
            analysis, created, versions_created

        See Also
        --------
        * :ref:`user_guide/analysis_integration/realistic_example:Realistic\
          Analysis Integration Example`
        """

        # Analysis creation
        title = definition["title"]
        description = definition.get("description")
        analysis, created = self.get_or_create(
            title=title, description=description
        )

        # Versions creation
        versions = definition.get("versions", [])
        versions_created = AnalysisVersion.objects.from_list(
            analysis, versions
        )

        return analysis, created, versions_created

    def from_list(self, definitions: list) -> Dict[str, Dict]:
        """
        Gets or creates :class:`~django_analyses.models.analysis.Analysis`
        instances using a list of analysis dictionary definitions.

        Parameters
        ----------
        definition : list
            Analysis definitions

        Returns
        -------
        Dict[str, Dict]
            A dictionary with analysis titles as keys and analysis version
            dictionaries as values.

        See Also
        --------
        * :ref:`user_guide/analysis_integration/realistic_example:Realistic\
          Analysis Integration Example`
        """

        results = {}
        for analysis_definition in definitions:
            analysis, created, versions = self.from_dict(analysis_definition)
            results[analysis.title] = {
                "model": analysis,
                "created": created,
                "versions": versions,
            }
        return results
