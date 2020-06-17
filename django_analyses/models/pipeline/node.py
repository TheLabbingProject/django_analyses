"""
Definition of the :class:`~django_analyses.models.pipeline.node.Node` class.
"""

from django.contrib.auth import get_user_model
from django.contrib.postgres.fields import JSONField
from django.db import models
from django_analyses.models.run import Run
from django_extensions.db.models import TimeStampedModel
from typing import Any

User = get_user_model()


class Node(TimeStampedModel):
    """
    A :class:`~django.db.models.Model` representing a single pipeline node in
    the database. A node is simply a reference to some distinct configuration
    of a particular analysis version. Nodes are the building blocks of a
    :class:`~django_analyses.models.pipeline.pipeline.Pipeline`, and
    :class:`~django_analyses.models.pipeline.pipe.Pipe` instances are used to
    attach them to one another.
    """

    #: The analysis version this node holds a configuration for.
    analysis_version = models.ForeignKey(
        "django_analyses.AnalysisVersion", on_delete=models.PROTECT
    )

    #: The configuration of the analysis version ran when executing this node.
    configuration = JSONField(default=dict)

    class Meta:
        ordering = ("-created",)
        unique_together = "analysis_version", "configuration"

    def __str__(self) -> str:
        """
        Returns the string representation of this instance.

        Returns
        -------
        str
            This instance's string representation
        """

        version = self.analysis_version
        config = self.configuration
        return f"\nNode #{self.id}\n{version}\nConfiguration: [{config}]\n"

    def save(self, *args, **kwargs):
        """
        Overrides the model's :meth:`~django.db.models.Model.save` method to
        provide custom validation.

        Hint
        ----
        For more information, see Django's documentation on `overriding model
        methods`_.

        .. _overriding model methods:
           https://docs.djangoproject.com/en/3.0/topics/db/models/#overriding-model-methods
        """

        self.validate()
        super().save(*args, **kwargs)

    def get_configuration(self) -> dict:
        """
        Undo any changes made to the node's configuration for serialization
        before passing them on to the interface.

        Returns
        -------
        dict
            Node's analysis version configuration
        """

        configuration = {}
        for key, value in self.configuration.items():
            definition = self.analysis_version.input_definitions.get(key=key)
            value_field = definition.input_class._meta.get_field("value")
            is_foreign_key = isinstance(value_field, models.ForeignKey)
            if is_foreign_key:
                configuration[key] = value_field.related_model.objects.get(
                    id=value
                )
            else:
                configuration[key] = value
        return configuration

    def validate(self) -> None:
        """
        Validates that the assigned configuration matches the chosen analysis
        version's input specification.
        """

        if self.configuration:
            self.analysis_version.input_specification.validate_keys(
                **self.configuration
            )

    def get_full_configuration(self, inputs: dict) -> dict:
        """
        Returns a "full" input configuration, combining any provided inputs
        with this node's
        :attr:`~django_analyses.models.pipeline.node.Node.configuration` and
        any default values configured in this analysis version's input
        specification.

        Parameters
        ----------
        inputs : dict
            User provided inputs for the execution of the node

        Returns
        -------
        dict
            Full configuration to pass to the interface
        """

        defaults = (
            self.analysis_version.input_specification.default_configuration
        )
        node_configuration = defaults.copy()
        node_configuration.update(self.get_configuration())
        node_configuration.update(inputs)
        return node_configuration

    def run(self, inputs: dict, user: User = None) -> Run:
        """
        Run this node (the interface associated with this node's
        :attr:`~django_analyses.models.pipeline.node.Node.analysis_version`)
        with the given inputs.

        Parameters
        ----------
        inputs : dict
            Any user-provided inputs to pass to the interface
        user : User, optional
            The user creating this run, by default None

        Returns
        -------
        Run
            The run instance holding the information of this run.
        """

        full_configuration = self.get_full_configuration(inputs)
        return Run.objects.get_or_execute(
            self.analysis_version, user=user, **full_configuration
        )

    def get_required_nodes(self) -> models.QuerySet:
        """
        Returns a queryset of
        :class:`~django_analyses.models.pipeline.node.Node` instances that are
        a previous step in some
        :class:`~django_analyses.models.pipeline.pipeline.Pipeline` instance
        (i.e. there is a pipe in which the retuned nodes are the source and
        this node is the destination).

        Returns
        -------
        models.QuerySet
            Required nodes
        """

        node_ids = self.pipe_destination_set.values_list("source", flat=True)
        return Node.objects.filter(id__in=list(node_ids))

    def get_requiring_nodes(self) -> models.QuerySet:
        """
        Returns a queryset of
        :class:`~django_analyses.models.pipeline.node.Node` instances that are
        the next step in some
        :class:`~django_analyses.models.pipeline.pipeline.Pipeline` instance
        (i.e. there is a pipe in which the retuned nodes are the destination
        and this node is the source).

        Returns
        -------
        models.QuerySet
            Requiring nodes
        """

        node_ids = self.pipe_source_set.values_list("destination", flat=True)
        return Node.objects.filter(id__in=list(node_ids))

    def check_configuration_sameness(self, key: str, value: Any) -> bool:
        """
        Checks whether the provided configuration *key* and *value* match this
        node's
        :attr:`~django_analyses.models.pipeline.node.Node.configuration`.
        Takes into account default values and returns *True* for any
        non-configuration inputs (run inputs).

        Parameters
        ----------
        key : str
            The key of the configuration value in question
        value : Any
            Configuration value to compare

        Returns
        -------
        bool
            Whether this node's
            :attr:`~django_analyses.models.pipeline.node.Node.configuration`
            is equal to provided configuration or not
        """

        is_same = value == self.configuration.get(key)
        input_definition = self.analysis_version.input_definitions.get(key=key)
        is_default = (
            value == input_definition.default
            and self.configuration.get(key) is None
        )
        not_configuration = input_definition.is_configuration is False
        return is_same or is_default or not_configuration

    def check_run_configuration_sameness(self, run: Run) -> bool:
        """
        Checks whether the given *run*'s configuration is equivalent to this
        node's
        :attr:`~django_analyses.models.pipeline.node.Node.configuration` value.

        Parameters
        ----------
        run : Run
            Some run of this node's analysis version

        Returns
        -------
        bool
            Whether the given run's configuration is equivalent to this node's
            :attr:`~django_analyses.models.pipeline.node.Node.configuration`
            value

        See Also
        --------
        * :meth:`check_configuration_sameness`
        """

        return all(
            [
                self.check_configuration_sameness(key, value)
                for key, value in run.input_configuration.items()
            ]
        )

    def get_run_set(self) -> models.QuerySet:
        """
        Returns all the existing :class:`~django_analyses.models.run.Run`
        instances that match this node's
        :attr:`~django_analyses.models.pipeline.node.Node.configuration` value.

        Returns
        -------
        models.QuerySet
            Existing node runs
        """

        all_runs = Run.objects.filter(analysis_version=self.analysis_version)
        runs = [
            run
            for run in all_runs
            if self.check_run_configuration_sameness(run)
        ]
        run_ids = [run.id for run in runs]
        return Run.objects.filter(id__in=run_ids)

    @property
    def required_nodes(self) -> models.QuerySet:
        """
        Returns the queryset of required nodes returned by calling
        :meth:`get_required_nodes`, or *None* if it is empty.

        Returns
        -------
        models.QuerySet
            Required nodes

        See Also
        --------
        * :meth:`get_required_nodes`
        """

        return self.get_required_nodes() or None

    @property
    def requiring_nodes(self) -> models.QuerySet:
        """
        Returns the queryset of requiring nodes returned by calling
        :meth:`get_requiring_nodes`, or *None* if it is empty.

        Returns
        -------
        models.QuerySet
            Requiring nodes

        See Also
        --------
        * :meth:`get_requiring_nodes`
        """

        return self.get_requiring_nodes() or None

    @property
    def run_set(self) -> models.QuerySet:
        """
        Returns the queryset of existing runs matching this node's
        :attr:`~django_analyses.models.pipeline.node.Node.configuration` value.

        Returns
        -------
        models.QuerySet
            Required nodes

        See Also
        --------
        * :meth:`get_run_set`
        """

        return self.get_run_set()
