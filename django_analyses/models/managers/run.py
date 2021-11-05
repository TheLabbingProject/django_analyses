"""
Definition of the :class:`RunManager` class.
"""
from typing import Any, Dict, Iterable, Union

from django.contrib.auth import get_user_model
from django.core.exceptions import ObjectDoesNotExist
from django.db import models
from django.utils import timezone
from django_analyses.models.analysis_version import AnalysisVersion
from django_analyses.models.managers.messages import (
    INVALID_INPUT_DEFINITION_KEY,
)
from django_analyses.utils.input_manager import InputManager
from django_analyses.utils.output_manager import OutputManager

User = get_user_model()


class RunManager(models.Manager):
    """
    Manager for the :class:`~django_analyses.models.run.Run` model. Handles the
    creation and retrieval of runs when
    :class:`~django_analyses.models.pipeline.node.Node` are executed.
    """

    def filter_by_configuration(
        self,
        analysis_version: AnalysisVersion,
        configuration: Union[Dict[str, Any], Iterable[Dict[str, Any]]],
        strict: bool = False,
        ignore_non_config: bool = False,
    ) -> models.QuerySet:
        """
        Returns a queryset of *analysis_version* runs matching the provided
        *configuration*.

        Parameters
        ----------
        analysis_version : AnalysisVersion
            Analysis version runs to query
        configuration : Union[Dict[str, Any], Iterable[Dict[str, Any]]]
            Configuration options to filter by
        strict : bool, optional
            Whether to exclude runs with non-default value configurations not
            included in the provided *configuration*, by default False
        ignore_non_config : bool, optional
            Whether to exclude keys that match definitions for which the
            :attr:`~django_analyses.models.input.definitions.input_definition.InputDefinition.is_configuration`
            attribute is set to False, by default False

        Returns
        -------
        models.QuerySet
            Matching runs
        """
        # Filter by single configuration dictionary.
        if isinstance(configuration, dict):
            if strict:
                configuration = analysis_version.update_input_with_defaults(
                    configuration
                )
            # Determine queried key set.
            key_set = set(configuration.keys())
            if ignore_non_config:
                configuration_keys = (
                    analysis_version.input_specification.configuration_keys
                )
                key_set = key_set.intersection(configuration_keys)
            # Keep track of runs matching each configuration specification.
            potential_runs = {key: [] for key in key_set}
            # In case *strict* is True, keep a reference to the full key set.
            if configuration:
                # Update potential_runs with runs matching each specification
                # in the provided configuration dictionary.
                for key in key_set:
                    value = configuration[key]
                    try:
                        definition = analysis_version.input_definitions.get(
                            key=key
                        )
                    except ObjectDoesNotExist:
                        # If an invalid input definition key was passed, there
                        # can be no matching runs.
                        return self.none()
                    else:
                        matching_input = definition.input_set.filter(
                            value=value
                        )
                        if matching_input.exists():
                            matching_runs = [
                                inpt.run.id for inpt in matching_input
                            ]
                            potential_runs[key] += matching_runs
                        else:
                            # If no matches were found for any given input
                            # value, it means no existing runs can exist for
                            # the entire provided configuration.
                            return self.none()
                # Extract a set of runs satisfying all provided criteria.
                run_ids = set.intersection(*map(set, potential_runs.values()))
            # If the configuration dictionary is empty, the full queryset can
            # be returned automatically.
            else:
                run_ids = (
                    run.id
                    for run in self.all()
                    if run.check_null_configuration()
                )
            return self.filter(id__in=run_ids)
        # Filter by multiple configuration dictionaries.
        elif isinstance(configuration, Iterable):
            run_ids = [
                run.id
                for run in filter(
                    None,
                    [
                        self.filter_by_configuration(specification)
                        for specification in configuration
                    ],
                )
            ]
            return self.filter(id__in=run_ids)

    def get_existing(
        self, analysis_version: AnalysisVersion, configuration: dict
    ):
        """
        Returns an existing run of the provided *analysis_version* with the
        specified *configuration*.

        Parameters
        ----------
        analysis_version : AnalysisVersion
            The desired AnalysisVersion instance for which a run is queried
        configuration : dict
            Full input configuration (excluding default values)

        Returns
        -------
        Run
            Existing run with the specified *analysis_version* and
            *configuration*

        Raises
        ------
        ObjectDoesNotExist
            No matching run exists
        """
        runs = self.filter(analysis_version=analysis_version)

        # ForeignKey fields are serialized to the database as the primary keys
        # of the associated instances, so in order to compare configurations
        # with model instances, we convert the value to primary key.
        for key, value in configuration.items():
            try:
                input_definition = analysis_version.input_definitions.get(
                    key=key
                )
            except ObjectDoesNotExist:
                message = INVALID_INPUT_DEFINITION_KEY.format(
                    analysis_version=analysis_version, key=key
                )
                raise ObjectDoesNotExist(message)
            if input_definition.db_value_preprocessing:
                configuration[key] = input_definition.get_db_value(value)
            elif isinstance(value, models.Model):
                configuration[key] = value.id
        # Update with the analysis version's input specification deafults in
        # order to compare the full configuration.
        configuration = analysis_version.update_input_with_defaults(
            configuration
        )
        # Find a matching run instance (only one should exist) and return it
        # or None.
        matching = [
            run.id for run in runs if run.input_configuration == configuration
        ]
        return self.get(id__in=matching)

    def create_and_execute(
        self,
        analysis_version: AnalysisVersion,
        configuration: dict,
        user: User = None,
    ):
        """
        Execute *analysis_version* with the provided configuration (keyword
        arguments) and return the created run.

        Parameters
        ----------
        analysis_version : AnalysisVersion
            AnalysisVersion to execute
        configuration : dict
            Full input configuration (excluding default values)
        user : User, optional
            User who executed the run, by default None

        Returns
        -------
        Run
            Resulting run instance
        """
        run = self.create(
            analysis_version=analysis_version,
            user=user,
            status="STARTED",
            start_time=timezone.now(),
        )
        update_fields = []
        try:
            input_manager = InputManager(run=run, configuration=configuration)
            inputs = input_manager.create_input_instances()
            results = analysis_version.run(**inputs)
            output_manager = OutputManager(run=run, results=results)
            output_manager.create_output_instances()
        except KeyboardInterrupt:
            run.delete()
            return
        except Exception as e:
            run.status = "FAILURE"
            run.traceback = str(e)
            run.end_time = timezone.now()
            update_fields = ["status", "traceback", "end_time"]
        else:
            run.status = "SUCCESS"
            run.end_time = timezone.now()
            update_fields = ["status", "end_time"]
        run.save(update_fields=update_fields)
        return run

    def get_or_execute(
        self,
        analysis_version: AnalysisVersion,
        configuration: dict,
        user: User = None,
        return_created: bool = False,
    ):
        """
        Get or execute a run of *analysis_version* with the provided keyword
        arguments.

        Parameters
        ----------
        analysis_version : AnalysisVersion
            AnalysisVersion to retrieve or execute
        configuration : dict
            Full input configuration (excluding default values)
        user : User, optional
            User who executed the run, by default None, by default None
        return_created : bool
            Whether to also return a boolean indicating if the run already
            existed in the database or created, defaults to False

        Returns
        -------
        Run
            New or existings run instance
        """

        try:
            existing = self.get_existing(analysis_version, configuration)
        except self.model.DoesNotExist:
            run = self.create_and_execute(
                analysis_version, configuration, user
            )
            return (run, True) if return_created else run
        else:
            return (existing, False) if return_created else existing
