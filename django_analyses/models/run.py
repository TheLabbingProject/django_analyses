"""
Definition of the :class:`Run` model.
"""
import datetime
import inspect
from pathlib import Path
from typing import Any

from django.conf import settings
from django.contrib.auth import get_user_model
from django.db import models
from django.utils import timezone
from django_analyses.models.managers.run import RunManager
from django_analyses.models.utils.run_status import RunStatus
from django_analyses.utils.get_visualizers import get_visualizer
from django_extensions.db.models import TimeStampedModel
from model_utils.managers import InheritanceQuerySet

User = get_user_model()


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
        User, blank=True, null=True, on_delete=models.SET_NULL,
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
        formatted_time = self.created.strftime("%Y-%m-%d %H:%M:%S")
        return f"#{self.id} {self.analysis_version} run from {formatted_time}"

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

    def get_input(self, key: str) -> Any:
        """
        Returns a particular output created in this run according to its
        definition's
        :attr:`~django_analyses.models.input.definitions.input_definition.key`
        field.

        Parameters
        ----------
        key : str
            The desired :class:`~django_analyses.models.input.input.Input`'s
            associated definition keyword

        Returns
        -------
        Any
            Input value
        """
        match = [
            inpt for inpt in self.input_set.all() if inpt.definition.key == key
        ]
        if match:
            return match[0].value

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

    def get_input_configuration(
        self,
        include_non_configuration: bool = True,
        include_defaults: bool = True,
    ) -> dict:
        """
        Returns the  input configuration of this run.

        Parameters
        ----------
        include_non_configuration : bool
            Whether to include inputs for which the associated definition's
            :attr:`~django_analyses.models.input.definitions.input_definitions.InputDefinition.is_configuration`
            attribute is set to False, default is True
        include_defaults : bool
            Whether to include default input configuration values, default is
            True

        Returns
        -------
        dict
            Input configuration
        """
        defaults = self.input_defaults.copy()
        if include_non_configuration and include_defaults:
            return {**defaults, **self.raw_input_configuration}
        elif include_non_configuration and not include_defaults:
            return {
                key: value
                for key, value in self.raw_input_configuration.items()
                if key not in defaults or defaults.get(key) != value
            }
        elif not include_non_configuration and include_defaults:
            full = {**defaults, **self.raw_input_configuration}
            definitions = self.analysis_version.input_definitions
            return {
                key: value
                for key, value in full.items()
                if definitions.get(key=key).is_configuration
            }
        else:
            definitions = self.analysis_version.input_definitions
            return {
                key: value
                for key, value in self.raw_input_configuration.items()
                if (key not in defaults or defaults.get(key) != value)
                and definitions.get(key=key).is_configuration
            }

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

    def check_null_configuration(self) -> bool:
        """
        Checks whether this run's configuration is equivalent to the input
        specification's default settings.

        Returns
        -------
        bool
            Whether this run has only default configuration settings
        """
        return (
            self.get_input_configuration(
                include_defaults=False, include_non_configuration=False
            )
            == {}
        )

    def get_visualizer(self, provider: str = None) -> callable:
        return get_visualizer(
            analysis_version=self.analysis_version, provider=provider
        )

    def visualize(self) -> None:
        visualizer = self.get_visualizer()
        if inspect.isclass(visualizer):
            visualizer = visualizer().visualize(self)
        else:
            visualizer(self)

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
