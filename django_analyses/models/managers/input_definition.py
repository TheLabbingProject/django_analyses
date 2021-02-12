"""
Definition of the
:class:`~django_analyses.models.managers.input_definition.InputDefinitionManager`
class.
"""

from copy import deepcopy

from model_utils.managers import InheritanceManager


class InputDefinitionManager(InheritanceManager):
    """
    Custom manager for the
    :class:`~django_analyses.models.input.definitions.input_definition.InputDefinition`
    model.
    """

    def from_dict(self, key: str, definition: dict):
        """
        Creates an input definition (an instance of any subclass of the
        :class:`~django_analyses.models.input.definitions.input_definition.InputDefinition`
        model) using the provided data. Expects *definition* to include a
        *type* key with the subclass (model) itself.

        Parameters
        ----------
        key : str
            Input definition key
        definition : dict
            Any other fields to populate

        Returns
        -------
        ~django_analyses.models.input.definitions.input_definition.InputDefinition
            Created input definition
        """

        definition_model = definition.pop("type")
        try:
            return definition_model.objects.get(key=key, **definition)
        # This try-except clause with the MultipleObjectsRetuned added
        # prevents raising an exception in case of a definition that is a
        # subset of two other definitions.
        except (self.model.DoesNotExist, self.model.MultipleObjectsReturned):
            return definition_model.objects.create(key=key, **definition)

    def from_specification_dict(self, specification: dict) -> list:
        """
        Creates multiple input definitions using some specification dictionary.

        Parameters
        ----------
        specification : dict
            A dictionary specification of input definitions

        Returns
        -------
        list
            Created input definitions
        """

        return [
            self.from_dict(key, definition)
            for key, definition in deepcopy(specification).items()
        ]
