from django_analyses.models.input.definitions.directory_input_definition import (
    DirectoryInputDefinition,
)
from django_analyses.models.input.definitions.input_definition import InputDefinition
from django_analyses.models.input.definitions.string_input_definition import (
    StringInputDefinition,
)


class InputManager:
    def __init__(self, run, configuration: dict):
        self.run = run
        self.raw_configuration = configuration
        self.input_definitions = self.run.analysis_version.input_definitions

    def input_definition_is_a_missing_output_path(
        self, input_definition: InputDefinition
    ) -> bool:
        return (
            isinstance(input_definition, StringInputDefinition)
            and input_definition.is_output_path
            and input_definition.key not in self.raw_configuration
        )

    def input_definition_is_a_missing_output_directory(
        self, input_definition: InputDefinition
    ) -> bool:
        return (
            isinstance(input_definition, DirectoryInputDefinition)
            and input_definition.is_output_directory
            and input_definition.key not in self.raw_configuration
        )

    def get_missing_output_path_definitions(self) -> list:
        return [
            input_definition
            for input_definition in self.input_definitions
            if self.input_definition_is_a_missing_output_path(input_definition)
        ]

    def get_missing_output_directory_definition(self) -> DirectoryInputDefinition:
        return [
            input_definition
            for input_definition in self.input_definitions
            if self.input_definition_is_a_missing_output_directory(input_definition)
        ]

    def get_missing_dynamic_default_definitions(self) -> list:
        return [
            input_definition
            for input_definition in self.input_definitions
            if getattr(input_definition, "dynamic_default", False)
            and input_definition.key not in self.raw_configuration
        ]

    def get_missing_input_definitions(self) -> list:
        return (
            self.get_missing_output_path_definitions()
            + self.get_missing_output_directory_definition()
            + self.get_missing_dynamic_default_definitions()
        )

    def get_or_create_missing_inputs(self) -> list:
        return [
            input_definition.get_or_create_input_instance(run=self.run)[0]
            for input_definition in self.missing_input_definitions
        ]

    def get_or_create_input_instance_from_raw(self, key: str, value) -> tuple:
        input_definition = self.input_definitions.get(key=key)
        return input_definition.get_or_create_input_instance(value=value, run=self.run)

    def convert_raw_configuration_to_input_instances(self) -> list:
        return [
            self.get_or_create_input_instance_from_raw(key, value)[0]
            for key, value in self.raw_configuration.items()
        ]

    def get_all_input_instances(self) -> list:
        return self.raw_input_instances + self.missing_inputs

    def get_required_paths(self) -> list:
        return [
            input_instance.required_path
            for input_instance in self.all_input_instances
            if getattr(input_instance, "required_path", None)
        ]

    def create_required_paths(self) -> None:
        for required_path in self.required_paths:
            required_path.mkdir(parents=True, exist_ok=True)

    def get_full_configuration(self) -> dict:
        return {
            input_instance.key: input_instance.argument_value
            for input_instance in self.all_input_instances
        }

    def fix_input(self) -> dict:
        self.create_required_paths()
        return self.full_configuration

    @property
    def missing_input_definitions(self) -> list:
        return self.get_missing_input_definitions()

    @property
    def missing_inputs(self) -> list:
        return self.get_or_create_missing_inputs()

    @property
    def raw_input_instances(self) -> list:
        return self.convert_raw_configuration_to_input_instances()

    @property
    def all_input_instances(self) -> list:
        return self.get_all_input_instances()

    @property
    def required_paths(self) -> list:
        return self.get_required_paths()

    @property
    def full_configuration(self) -> dict:
        return self.get_full_configuration()
