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
        Returns the :obj:`str` representation of the instance.

        Returns
        -------
        :obj:`str`
            This instances string representation
        """

        return self.title

    def get_node_set(self) -> QuerySet:
        """
        Returns all :class:`~django_analyses.models.pipeline.node.Node` instances
        used in this pipeline.

        Returns
        -------
        :class:`~django.db.models.query.QuerySet`
            Pipeline nodes
        """

        source_node_ids = list(self.pipe_set.values_list("source", flat=True))
        destination_node_ids = list(self.pipe_set.values_list("destination", flat=True))
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
        :obj:`list`
            List of :class:`~django_analyses.models.pipeline.node.Node`
            instances
        """

        return [node for node in self.node_set if node.required_nodes is None]

    @property
    def node_set(self) -> QuerySet:
        """
        See :meth:`~django_analyses.models.pipeline.pipeline.Pipeline.get_node_set`.

        Returns
        -------
        :class:`django.db.query.QuerySet`
            Pipeline nodes
        """

        return self.get_node_set()

    @property
    def entry_nodes(self) -> list:
        """
        See :meth:`~django_analyses.models.pipeline.pipeline.Pipeline.get_entry_nodes`.

        Returns
        -------
        :class:`django.db.query.QuerySet`
            Entry nodes
        """

        return self.get_entry_nodes()
