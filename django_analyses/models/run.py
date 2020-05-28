"""
Definition of the :class:`~django_analyses.models.run.Run` class.

"""

import shutil

from django.conf import settings
from django.contrib.auth import get_user_model
from django.db import models
from django_analyses.models.managers.run import RunManager
from django_extensions.db.models import TimeStampedModel
from pathlib import Path


class Run(TimeStampedModel):
    """
    :class:`~django.db.models.Model` representing a single analysis version's run in the
    database.

    """

    analysis_version = models.ForeignKey(
        "django_analyses.AnalysisVersion", on_delete=models.PROTECT
    )
    user = models.ForeignKey(
        get_user_model(), blank=True, null=True, on_delete=models.SET_NULL,
    )

    objects = RunManager()

    class Meta:
        ordering = ("-created",)

    def __str__(self) -> str:
        """
        Returns the string representation of the :class:`~django_analyses.models.run.Run`
        instance.

        Returns
        -------
        str
            String representation of this instance
        """

        return f"#{self.id} {self.analysis_version} run from {self.created}"

    def delete(self, *args, **kwargs) -> tuple:
        """
        `Overrides <https://docs.djangoproject.com/en/3.0/topics/db/models/#overriding-model-methods>`_
        the :meth:`~django.db.models.Model.delete` method to also remove
        the run's directory from
        `media <https://docs.djangoproject.com/en/3.0/topics/files/>`_.

        Returns
        -------
        :obj:`tuple`
            (number of deleted objects, dictionary of number by type)
        """

        if self.path:
            shutil.rmtree(self.path)
        return super().delete(*args, **kwargs)

    def get_input_set(self) -> models.QuerySet:
        """
        Returns the :class:`~django_analyses.models.input.input.Input` sub-classes'
        instances created for this execution of the
        :attr:`~django_analyses.models.run.Run.analysis_version`.

        Returns
        -------
        :class:`~django.db.models.query.QuerySet`
            This run's inputs
        """

        return self.base_input_set.select_subclasses()

    def get_output_set(self) -> models.QuerySet:
        """
        Returns the :class:`~django_analyses.models.output.output.Output` sub-classes'
        instances created on this execution of the
        :attr:`~django_analyses.models.run.Run.analysis_version`.

        Returns
        -------
        :class:`~django.db.models.query.QuerySet`
            This run's outputs
        """

        return self.base_output_set.select_subclasses()

    def get_input_configuration(self) -> dict:
        """
        Returns the full (including defaults) input configuration of this run.

        Returns
        -------
        :obj:`dict`
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
        :obj:`dict`
            Output configuration
        """

        return {output.key: output.value for output in self.output_set}

    def get_raw_input_configuration(self) -> dict:
        """
        Returns the "raw" configuration of this run. As some inputs may have been
        transformed by the :class:`~django_analyses.utils.input_manager.InputManager`,
        this method is used to reverse these changes in case this run's parameters are
        compared in the future to new input parameters.

        Returns
        -------
        :obj:`dict`
            Raw input configuration as provided by the user
        """

        return {
            inpt.key: inpt.value
            if not getattr(inpt.definition, "is_output_path", False)
            else Path(inpt.value).name
            for inpt in self.input_set
            if not getattr(inpt.definition, "is_output_directory", False)
        }

    @property
    def path(self) -> Path:
        """
        Retruns the default :class:`~pathlib.Path` for any artifacts created by this run.

        Returns
        -------
        :class:`pathlib.Path`
            Run artifacts directory under
            `MEDIA_ROOT <https://docs.djangoproject.com/en/3.0/ref/settings/#media-root>`_.
        """

        path = Path(settings.ANALYSIS_BASE_PATH) / str(self.id)
        return path if path.is_dir() else None

    @property
    def input_defaults(self) -> dict:
        """
        Returns the default configuration parameters according to this instance's
        :class:`~django_analyses.models.input.input_specification.InputSpecification`\'s
        :attr:`~django_analyses.models.input.input_specification.InputSpecification.default_configuration`
        property.

        Returns
        -------
        :obj:`dict`
            This analysis version's default input configuration
        """

        return self.analysis_version.input_specification.default_configuration

    @property
    def input_configuration(self) -> dict:
        """
        Returns a dictionary with the full input configuration of this run.

        Returns
        -------
        :obj:`dict`
            Full input configuration
        """

        return self.get_input_configuration()

    @property
    def output_configuration(self) -> dict:
        """
        Returns a dictionary of the output configuration of this run.

        Returns
        -------
        :obj:`dict`
            Output configuration
        """

        return self.get_output_configuration()

    @property
    def input_set(self) -> models.QuerySet:
        """
        Returns the :class:`~django_analyses.models.input.input.Input` sub-classes'
        instances created for this run.

        Returns
        -------
        :class:`~django.db.models.query.QuerySet`
            This run's inputs
        """

        return self.get_input_set()

    @property
    def output_set(self) -> models.QuerySet:
        """
        Returns the :class:`~django_analyses.models.output.output.Output` sub-classes'
        instances created by this run.

        Returns
        -------
        :class:`~django.db.models.query.QuerySet`
            This run's outputs
        """

        return self.get_output_set()

    @property
    def raw_input_configuration(self) -> dict:
        """
        Returns a dictionary of this run's raw input configuration.
        See :meth:`~django_analyses.models.run.Run.get_raw_input_configuration`.

        Returns
        -------
        :obj:`dict`
            This run's raw input configuration
        """

        return self.get_raw_input_configuration()
