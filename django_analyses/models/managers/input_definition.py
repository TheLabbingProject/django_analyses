from copy import deepcopy
from model_utils.managers import InheritanceManager


class InputDefinitionManager(InheritanceManager):
    def from_dict(self, key: str, definition: dict):
        definition_model = definition.pop("type")
        try:
            return definition_model.objects.get(key=key, **definition)
        # This try-except clause with the MultipleObjectsRetuned added
        # prevents raising an exception in case of a definition that is a
        # subset of two other definitions.
        except (self.model.DoesNotExist, self.model.MultipleObjectsReturned):
            return definition_model.objects.create(key=key, **definition)

    def from_specification_dict(self, specification: dict) -> list:
        return [
            self.from_dict(key, definition)
            for key, definition in deepcopy(specification).items()
        ]
