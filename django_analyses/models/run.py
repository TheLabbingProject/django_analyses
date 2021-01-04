"""
Definition of the :class:`Run` model.

"""
import datetime

from django.conf import settings
from django.contrib.auth import get_user_model
from django.db import models
from django.utils import timezone
from django_analyses.models.managers.run import RunManager
from django_analyses.utils.choice_enum import ChoiceEnum
from django_extensions.db.models import TimeStampedModel
from model_utils.managers import InheritanceQuerySet
from pathlib import Path
from typing import Any


class RunStatus(ChoiceEnum):
    STARTED = "Started"
    SUCCESS = "Success"
    FAILURE = "Failure"


class Run(TimeStampedModel):
    """
    :class:`~django.db.models.Model` representing a single analysis version's
    run in the database.

    """

    #: The :class:`~django_analyses.models.analysis_version.AnalysisVersion`
    #: that was run.
    analysis_version = models.ForeignKey(
        "django_analyses.AnalysisVersion", on_delete=models.PROTECT
    )

    #: The user who created this run.
    user = models.ForeignKey(
        get_user_model(), blank=True, null=True, on_delete=models.SET_NULL,
    )

    #: The :class:`~django_celery_results.models.task_result.TaskResult`
    #: instance associated with this run.
    task_result = models.OneToOneField(
        "django_celery_results.TaskResult",
        blank=True,
        null=True,
        on_delete=models.CASCADE,
    )

    #: The status of this run.
    status = models.CharField(
        max_length=7, choices=RunStatus.choices(), blank=True, null=True,
    )

    #: Run start time.
    start_time = models.DateTimeField(blank=True, null=True)

    #: Run end time.
    end_time = models.DateTimeField(blank=True, null=True)

    #: Traceback saved in case of run failure.
    traceback = models.TextField(blank=True, null=True)

    objects = RunManager()

    class Meta:
        ordering = ("-created",)

    def __str__(self) -> str:
        """
        Returns the string representation of the
        :class:`~django_analyses.models.run.Run` instance.

        Returns
        -------
        str
            String representation of this instance
        """

        return f"#{self.id} {self.analysis_version} run from {self.created}"

    def get_input_set(self) -> InheritanceQuerySet:
        """
        Returns the :class:`~django_analyses.models.input.input.Input`
        subclasses' instances created for this execution of the
        :attr:`~django_analyses.models.run.Run.analysis_version`.

        Returns
        -------
        :class:`~model_utils.managers.InheritanceQuerySet`
            This run's inputs
        """

        return self.base_input_set.select_subclasses()

    def get_output_set(self) -> InheritanceQuerySet:
        """
        Returns the :class:`~django_analyses.models.output.output.Output`
        subclasses' instances created on this execution of the
        :attr:`~django_analyses.models.run.Run.analysis_version`.

        Returns
        -------
        :class:`~model_utils.managers.InheritanceQuerySet`
            This run's outputs
        """

        return self.base_output_set.select_subclasses()

    def get_output(self, key: str) -> Any:
        """
        Returns a particular output created in this run according to its
        definition's
        :attr:`~django_analyses.models.output.definitions.output_definition.key`
        field.

        Parameters
        ----------
        key : str
            The desired :class:`~django_analyses.models.output.output.Output`'s
            associated definition keyword

        Returns
        -------
        Any
            Output value
        """

        match = [
            output
            for output in self.output_set.all()
            if output.definition.key == key
        ]
        if match:
            return match[0].value

    def get_input_configuration(self) -> dict:
        """
        Returns the full (including defaults) input configuration of this run.

        Returns
        -------
        dict
            Full input configuration
        """

        defaults = self.input_defaults.copy()
        defaults.update(self.raw_input_configuration)
        return defaults

    def get_output_configuration(self) -> dict:
        """
        Returns the output configuration of this run.

        Returns
        -------
        dict
            Output configuration
        """

        return {output.key: output.value for output in self.output_set}

    def fix_input_value(self, inpt) -> Any:
        """
        Reverts changes that may have been made to a given input in order to
        return the "raw" input configuration of this run (i.e. the input as it
        was passed by the user).

        Parameters
        ----------
        inpt : :class:`~django_analyses.models.input.input.Input`
            An input of this run

        Returns
        -------
        Any
            The "raw" input value
        """

        if getattr(inpt.definition, "is_output_path", False):
            return Path(inpt.value).name
        elif isinstance(inpt._meta.get_field("value"), models.ForeignKey):
            return inpt.value.id
        return inpt.value

    def get_raw_input_configuration(self) -> dict:
        """
        Returns the "raw" configuration of this run. As some inputs may have
        been transformed, this method is used to reverse these changes in case
        this run's parameters are compared in the future to new input
        parameters.

        Returns
        -------
        dict
            Raw input configuration as provided by the user
        """

        return {
            inpt.key: self.fix_input_value(inpt)
            for inpt in self.input_set
            if not (
                getattr(inpt.definition, "is_output_directory", False)
                or getattr(inpt.definition, "dynamic_default", False)
            )
        }

    def get_results_json(self) -> dict:
        """
        Returns a JSON serializable dictionary of the results.

        Returns
        -------
        dict
            JSON serializable output dictionary
        """

        return {
            output.definition.key: output.json_value
            for output in self.output_set.all()
        }

    @property
    def path(self) -> Path:
        """
        Retruns the default :class:`~pathlib.Path` for any artifacts created
        by this run.

        Returns
        -------
        :class:`pathlib.Path`
            Run artifacts directory under
            `MEDIA_ROOT
            <https://docs.djangoproject.com/en/3.0/ref/settings/#media-root>`_.
        """

        path = Path(settings.ANALYSIS_BASE_PATH) / str(self.id)
        return path if path.is_dir() else None

    @property
    def input_defaults(self) -> dict:
        """
        Returns the default configuration parameters according to this
        instance's
        :class:`~django_analyses.models.input.input_specification.InputSpecification`\'s
        :attr:`~django_analyses.models.input.input_specification.InputSpecification.default_configuration`
        property.

        Returns
        -------
        dict
            This analysis version's default input configuration
        """

        return self.analysis_version.input_specification.default_configuration

    @property
    def input_configuration(self) -> dict:
        """
        Returns a dictionary with the full input configuration of this run.

        Returns
        -------
        dict
            Full input configuration

        See Also
        --------
        * :meth:`get_input_configuration`
        """

        return self.get_input_configuration()

    @property
    def output_configuration(self) -> dict:
        """
        Returns a dictionary of the output configuration of this run.

        Returns
        -------
        dict
            Output configuration

        See Also
        --------
        * :meth:`get_output_configuration`
        """

        return self.get_output_configuration()

    @property
    def input_set(self) -> models.QuerySet:
        """
        Returns the :class:`~django_analyses.models.input.input.Input`
        subclasses' instances created for this run.

        Returns
        -------
        :class:`~django.db.models.query.QuerySet`
            This run's inputs

        See Also
        --------
        * :meth:`get_input_set`
        """

        return self.get_input_set()

    @property
    def output_set(self) -> models.QuerySet:
        """
        Returns the :class:`~django_analyses.models.output.output.Output`
        subclasses' instances created by this run.

        Returns
        -------
        :class:`~django.db.models.query.QuerySet`
            This run's outputs

        See Also
        --------
        * :meth:`get_output_set`
        """

        return self.get_output_set()

    @property
    def raw_input_configuration(self) -> dict:
        """
        Returns a dictionary of this run's raw input configuration.

        Returns
        -------
        dict
            This run's raw input configuration

        See Also
        --------
        * :meth:`get_raw_input_configuration`
        """

        return self.get_raw_input_configuration()

    @property
    def duration(self) -> datetime.timedelta:
        """
        Returns the time delta between this instance's :attr:`end_time` and
        :attr:`start_time`. If :attr:`end_time` isn't set yet returns time
        since :attr:`start_time`.

        Returns
        -------
        datetime.timedelta
            Run duration
        """

        if self.start_time and self.end_time:
            return self.end_time - self.start_time
        elif self.start_time:
            return timezone.now() - self.start_time
