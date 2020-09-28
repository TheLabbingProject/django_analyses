"""
Definition of the
:class:`~django_analyses.models.pipeline.pipeline.Pipeline` class.
"""

from django.db.models import QuerySet
from django_analyses.models.managers.pipeline import PipelineManager
from django_analyses.models.pipeline.node import Node
from django_extensions.db.models import TitleDescriptionModel, TimeStampedModel


class Pipeline(TitleDescriptionModel, TimeStampedModel):
    """
    A pipeline essentially represents a set of
    :class:`~django_analyses.models.pipeline.pipe.Pipe` instances constituting
    a distinct analysis procedure.
    """

    objects = PipelineManager()

    def __str__(self) -> str:
        """
        Returns the string representation of the instance.

        Returns
        -------
        str
            This instance's string representation
        """

        return self.title

    def get_node_set(self) -> QuerySet:
        """
        Returns all :class:`~django_analyses.models.pipeline.node.Node`
        instances used in this pipeline.

        Returns
        -------
        :class:`~django.db.models.query.QuerySet`
            Pipeline nodes
        """

        source_node_ids = list(self.pipe_set.values_list("source", flat=True))
        destination_node_ids = list(
            self.pipe_set.values_list("destination", flat=True)
        )
        node_ids = set(source_node_ids + destination_node_ids)
        return Node.objects.filter(id__in=node_ids)

    def get_entry_nodes(self) -> list:
        """
        Returns the "entry" node/s of this pipeline, i.e. nodes that are a
        :attr:`~django_analyses.models.pipeline.pipe.Pipe.source` of some
        :class:`~django_analyses.models.pipeline.pipe.Pipe` but not a
        :attr:`~django_analyses.models.pipeline.pipe.Pipe.destination` in any.

        Returns
        -------
        list
            List of :class:`~django_analyses.models.pipeline.node.Node`
            instances
        """

        return [
            node for node in self.node_set if node.is_entry_node(pipeline=self)
        ]

    def count_node_runs(self, node: Node) -> int:
        """
        Returns the number of times a particular node is meant to run during
        the execution of this pipeline.

        Parameters
        ----------
        node : Node
            Node to count

        Returns
        -------
        int
            Number of separate runs of *node* within this pipeline
        """

        source_pipes = self.pipe_set.filter(source=node)
        destination_pipes = self.pipe_set.filter(destination=node)
        source_run_indices = list(
            source_pipes.values_list("source_run_index", flat=True)
        )
        destination_run_indices = list(
            destination_pipes.values_list("destination_run_index", flat=True)
        )
        max_index = max(source_run_indices + destination_run_indices)
        return max_index + 1

    @property
    def node_set(self) -> QuerySet:
        """
        Returns all :class:`~django_analyses.models.pipeline.node.Node`
        instances used in this pipeline.

        Returns
        -------
        QuerySet
            Pipeline nodes

        See Also
        --------
        * :meth:`get_node_set`
        """

        return self.get_node_set()

    @property
    def entry_nodes(self) -> list:
        """
        Returns the "entry" node/s of this pipeline.

        Returns
        -------
        list
            Entry nodes

        See Also
        --------
        * :meth:`get_entry_nodes`
        """

        return self.get_entry_nodes()
