"""
Definition of the :class:`~django_analyses.models.run.Run` model's manager.
"""

from django.contrib.auth import get_user_model
from django.db import models
from django_analyses.models.analysis_version import AnalysisVersion
from django_analyses.utils.input_manager import InputManager
from django_analyses.utils.output_manager import OutputManager


User = get_user_model()


class RunManager(models.Manager):
    """
    Manager for the :class:`~django_analyses.models.run.Run` model. Handles the
    creation and retrieval of runs when
    :class:`~django_analyses.models.pipeline.node.Node` are executed.
    """

    def get_existing(self, analysis_version: AnalysisVersion, **kwargs):
        """
        Returns an existing run instance for the specified analysis version
        if one with the specified configuration exists, or *None*.

        Parameters
        ----------
        analysis_version : AnalysisVersion
            The desired AnalysisVersion instance for which a run is queried

        Returns
        -------
        Run
            Existing run instance or *None*
        """

        runs = self.filter(analysis_version=analysis_version)

        # ForeignKey fields are serialized to the database as the primary keys
        # of the associated instances, so in order to compare configurations
        # with model instances, we convert the value to primary key.
        for key, value in kwargs.items():
            if isinstance(value, models.Model):
                kwargs[key] = value.id

        # Update with the analysis version's input specification deafults in
        # order to compare the full configuration.
        configuration = analysis_version.update_input_with_defaults(**kwargs)

        # Find a matching run instance (only one should exist) and return it
        # or None.
        matching = [
            run for run in runs if run.input_configuration == configuration
        ]
        return matching[0] if matching else None

    def create_and_execute(
        self, analysis_version: AnalysisVersion, user: User = None, **kwargs
    ):
        """
        Execute *analysis_version* with the provided configuration (keyword
        arguments) and return the created run.

        Parameters
        ----------
        analysis_version : AnalysisVersion
            AnalysisVersion to execute
        user : User, optional
            User who executed the run, by default None

        Returns
        -------
        Run
            Resulting run instance
        """

        run = self.create(analysis_version=analysis_version, user=user)
        input_manager = InputManager(run=run, configuration=kwargs)
        inputs = input_manager.fix_input()
        try:
            results = analysis_version.run(**inputs)
        except KeyboardInterrupt:
            run.delete()
            return
        output_manager = OutputManager(run=run, results=results)
        output_manager.create_output_instances()
        return run

    def get_or_execute(
        self, analysis_version: AnalysisVersion, user: User = None, **kwargs
    ):
        """
        Get or execute a run of *analysis_version* with the provided keyword
        arguments.

        Parameters
        ----------
        analysis_version : AnalysisVersion
            AnalysisVersion to retrieve or execute
        user : User, optional
            User who executed the run, by default None, by default None

        Returns
        -------
        Run
            New or existings run instance
        """

        existing = self.get_existing(analysis_version, **kwargs)
        return existing or self.create_and_execute(
            analysis_version, user, **kwargs
        )
