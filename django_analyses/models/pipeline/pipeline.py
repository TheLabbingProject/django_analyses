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
    :class:`~django_analyses.models.pipeline.pipe.Pipe` instances,
    constituting a distinct analysis procedure.
    """

    objects = PipelineManager()

    def __str__(self):
        return self.title

    def get_node_set(self) -> QuerySet:
        source_node_ids = list(self.pipe_set.values_list("source", flat=True))
        destination_node_ids = list(self.pipe_set.values_list("destination", flat=True))
        node_ids = set(source_node_ids + destination_node_ids)
        return Node.objects.filter(id__in=node_ids)

    def get_entry_nodes(self) -> Node:
        return [node for node in self.node_set if node.required_nodes is None]

    @property
    def node_set(self) -> QuerySet:
        return self.get_node_set()

    @property
    def entry_nodes(self) -> list:
        return self.get_entry_nodes()
