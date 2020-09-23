"""
Definition of the :class:`~django_analyses.models.pipeline.pipe.Pipe` class.
"""

from django.db import models
from django_analyses.models.input.definitions.input_definition import (
    InputDefinition,
)
from django_analyses.models.managers.pipe import PipeManager
from django_analyses.models.output.definitions.output_definition import (
    OutputDefinition,
)


class Pipe(models.Model):
    """
    A :class:`~django.db.models.Model` representing a directed association
    between one :class:`~django_analyses.models.pipeline.node.Node`\'s output
    and another :class:`~django_analyses.models.pipeline.node.Node`\'s input
    within the context of a particular
    :class:`~django_analyses.models.pipeline.pipeline.Pipeline`.
    """

    #: The :class:`~django_analyses.models.pipeline.pipeline.Pipeline`
    #: instance to which this pipe belongs.
    pipeline = models.ForeignKey(
        "django_analyses.Pipeline", on_delete=models.CASCADE
    )

    #: The *source* :class:`~django_analyses.models.pipeline.node.Node`, i.e. a
    #: node that will provide some input for the destination node.
    source = models.ForeignKey(
        "django_analyses.Node",
        on_delete=models.PROTECT,
        related_name="pipe_source_set",
    )

    base_source_port = models.ForeignKey(
        "django_analyses.OutputDefinition", on_delete=models.PROTECT
    )
    """
    An output definition of the *source* node that will provide some input of
    the *destination* node.

    Note
    ----
    This field holds the reference to the base
    :class:`~django_analyses.models.output.definitions.output_definition.OutputDefinition`
    instance.

    See Also
    --------
    * :attr:`source_port`

    .. # noqa: E501
    """

    #: The *destination* :class:`~django_analyses.models.pipeline.node.Node`,
    #: i.e. a node that will be provided an input from the *source* node.
    destination = models.ForeignKey(
        "django_analyses.Node",
        on_delete=models.PROTECT,
        related_name="pipe_destination_set",
    )

    base_destination_port = models.ForeignKey(
        "django_analyses.InputDefinition", on_delete=models.PROTECT
    )
    """
    An input definition of the *destination* node that will be provided some
    input by the *source* node.

    Note
    ----
    This field holds the reference to the base
    :class:`~django_analyses.models.input.definitions.input_definition.InputDefinition`
    instance.

    See Also
    --------
    * :attr:`destination_port`

    .. # noqa: E501
    """

    #: The *index* field is used to listify arguments in transit between nodes.
    #: An integer indicates expected input's index in the destination
    #: ListInput, and *None* indicates the index doesn't matter.
    index = models.PositiveIntegerField(default=None, blank=True, null=True)

    group = models.PositiveIntegerField(default=0)

    objects = PipeManager()

    # A template to generate the string representation of pipe isntances.
    _STRING_TEMPLATE = (
        "{source} [{source_key}] --> [{destination_key}] {destination}"
    )

    def __str__(self) -> str:
        """
        Returns the string representation of this instance.

        Returns
        -------
        str
            This instance's string representation
        """

        source = self.source.analysis_version.analysis
        source_key = self.base_source_port.key
        destination = self.destination.analysis_version.analysis
        destination_key = self.base_destination_port.key
        return self._STRING_TEMPLATE.format(
            source=source,
            source_key=source_key,
            destination=destination,
            destination_key=destination_key,
        )

    @property
    def source_port(self) -> OutputDefinition:
        """
        Returns the
        :class:`~django_analyses.models.output.definitions.output_definition.OutputDefinition`
        subclass of the assigned :attr:`base_source_port`.

        .. # noqa: E501

        Returns
        -------
        OutputDefinition
            The *source* output definition
        """

        return OutputDefinition.objects.select_subclasses().get(
            id=self.base_source_port.id
        )

    @property
    def destination_port(self) -> InputDefinition:
        """
        Returns the
        :class:`~django_analyses.models.input.definitions.input_definition.InputDefinition`
        subclass of the assigned :attr:`base_destination_port`.

        .. # noqa: E501

        Returns
        -------
        InputDefinition
            The *destination* input definition
        """

        return InputDefinition.objects.select_subclasses().get(
            id=self.base_destination_port.id
        )
