"""
Definition of the :class:`Node` class.
"""
from typing import Any, Dict, List, Tuple, Union

from django.contrib.auth import get_user_model
from django.db import models
from django_analyses.models.pipeline.messages import BAD_INPUTS_TYPE
from django_analyses.models.run import Run
from django_extensions.db.models import TimeStampedModel

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
    configuration = models.JSONField(default=dict)

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

    def get_full_configuration(self, inputs: dict = None) -> dict:
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

        inputs = {} if inputs is None else inputs
        defaults = (
            self.analysis_version.input_specification.default_configuration
        )
        node_configuration = defaults.copy()
        node_configuration.update(self.get_configuration())
        node_configuration.update(inputs)
        return node_configuration

    def run(
        self,
        inputs: Union[
            Dict[str, Any], List[Dict[str, Any]], Tuple[Dict[str, Any]]
        ],
        user: User = None,
        return_created: bool = False,
    ) -> Union[Run, List[Run], Tuple[Run, bool], List[Tuple[Run, bool]]]:
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
        return_created : bool
            Whether to also return a boolean indicating if the run already
            existed in the database or created, defaults to False

        Returns
        -------
        Union[Run, List[Run], Tuple[Run, bool], List[Tuple[Run, bool]]]
            The created or retreived run instance/s
        """

        if isinstance(inputs, dict):
            full_configuration = self.get_full_configuration(inputs)
            return Run.objects.get_or_execute(
                self.analysis_version,
                user=user,
                return_created=return_created,
                **full_configuration,
            )
        elif isinstance(inputs, (list, tuple)):
            return [
                self.run(inputs=iteration_inputs)
                for iteration_inputs in inputs
            ]
        else:
            message = BAD_INPUTS_TYPE.format(input_type=type(inputs))
            raise TypeError(message)

    def get_required_nodes(
        self, pipeline=None, run_index: int = None
    ) -> models.QuerySet:
        """
        Returns a queryset of
        :class:`~django_analyses.models.pipeline.node.Node` instances that are
        a previous step in some
        :class:`~django_analyses.models.pipeline.pipeline.Pipeline` instance
        (i.e. there is a pipe in which the retuned nodes are the source and
        this node is the destination).

        Parameters
        ----------
        pipeline : :class:`~django_analyses.models.pipeline.pipeline.Pipeline`
            A pipeline instance to filter the pipe set with, optional
        run_index : int
            If this node is executed more than once in a given pipeline, filter
            by the index of the node's run, optional

        Returns
        -------
        models.QuerySet
            Required nodes
        """

        pipes = self.pipe_destination_set
        if pipeline:
            pipes = pipes.filter(pipeline=pipeline)
        if isinstance(run_index, int):
            pipes = pipes.filter(destination_run_index=run_index)
        return pipes.values("source", "source_run_index")

    def get_requiring_nodes(
        self, pipeline=None, run_index: int = None
    ) -> models.QuerySet:
        """
        Returns a queryset of
        :class:`~django_analyses.models.pipeline.node.Node` instances that are
        the next step in some
        :class:`~django_analyses.models.pipeline.pipeline.Pipeline` instance
        (i.e. there is a pipe in which the retuned nodes are the destination
        and this node is the source).

        Parameters
        ----------
        pipeline : :class:`~django_analyses.models.pipeline.pipeline.Pipeline`
            A pipeline instance to filter the pipe set with, optional
        run_index : int
            If this node is executed more than once in a given pipeline, filter
            by the index of the node's run, optional

        Returns
        -------
        models.QuerySet
            Requiring nodes
        """

        pipes = self.pipe_source_set
        if pipeline:
            pipes = pipes.filter(pipeline=pipeline)
        if isinstance(run_index, int):
            pipes = pipes.filter(source_run_index=run_index)
        return self.pipe_source_set.values(
            "destination", "destination_run_index"
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

        full_configuration = self.get_full_configuration()
        return Run.objects.filter_by_configuration(
            self.analysis_version, **full_configuration
        )

    def is_entry_node(self, pipeline) -> bool:
        """
        Determines whether this node is an entry point of the specified
        pipeline by checking if the first run of this node has any dependencies
        (i.e. has any pipes leading to it).


        Parameters
        ----------
        pipeline : :class:`~django_analyses.models.pipeline.pipeline.Pipeline`
            The pipeline to check

        Returns
        -------
        bool
            Whether this node is an entry point of the given pipeline or not
        """

        return not self.get_required_nodes(pipeline=pipeline, run_index=0)

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
