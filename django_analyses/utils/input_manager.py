"""
Definition of the :class:`InputManager` class.
"""

from typing import Any, List, Set, Tuple

from django_analyses.models.input.definitions.directory_input_definition import \
    DirectoryInputDefinition  # noqa: E501
from django_analyses.models.input.definitions.input_definition import \
    InputDefinition
from django_analyses.models.input.definitions.string_input_definition import \
    StringInputDefinition
from django_analyses.models.input.input import Input

BAD_KEY = "Invalid input definition key: {key}"


class InputManager:
    """
    Creates :class:`~django_analyses.models.input.input.Input` subclass
    instances according to the provided
    :class:`~django_analyses.models.run.Run`'s associated
    :class:`~django_analyses.models.input.input_specification.InputSpecification`.
    """

    def __init__(self, run, configuration: dict):
        """
        Initializes an new instance of this class.

        Parameters
        ----------
        run : :class:`~django_analyses.models.run.Run`
            The run for which :class:`Input` subclass instances should be
            created
        configuration : dict
            User provided input configuration dictionary
        """

        self.run = run
        self.raw_configuration = configuration
        self.input_definitions = self.run.analysis_version.input_definitions

    def input_definition_is_a_missing_output_path(
        self, input_definition: InputDefinition
    ) -> bool:
        """
        Checks whether the provided input definition represents an output path,
        and whether it is missing in the provided configuration.

        Parameters
        ----------
        input_definition : InputDefinition
            Input definition in question

        Returns
        -------
        bool
            Whether the provided input definition represents an output path and
            is missing in the complete input configuration
        """

        return (
            isinstance(input_definition, StringInputDefinition)
            and input_definition.is_output_path
            and input_definition.key not in self.raw_configuration
            and input_definition.required
        )

    def input_definition_is_a_missing_output_directory(
        self, input_definition: InputDefinition
    ) -> bool:
        """
        Checks whether the provided input definition represents an output
        directory, and whether it is missing in the provided configuration.

        Parameters
        ----------
        input_definition : InputDefinition
            Input definition in question

        Returns
        -------
        bool
            Whether the provided input definition represents an output
            directory and is missing in the complete input configuration
        """

        return (
            isinstance(input_definition, DirectoryInputDefinition)
            and input_definition.is_output_directory
            and input_definition.key not in self.raw_configuration
        )

    def get_missing_output_path_definitions(
        self,
    ) -> List[StringInputDefinition]:
        """
        Returns missing output path definitions.

        Returns
        -------
        List[StringInputDefinition]
            List of missing output path configurations that should be generated
        """

        return [
            input_definition
            for input_definition in self.input_definitions
            if self.input_definition_is_a_missing_output_path(input_definition)
        ]

    def get_missing_output_directory_definition(
        self,
    ) -> List[DirectoryInputDefinition]:
        """
        Returns missing output directory definition. There should only be one
        at the most, however, it is returned as a list so it can easily be
        appended to other missing inputs.

        Returns
        -------
        List[StringInputDefinition]
            List of missing output directory configurations that should be
            generated
        """

        return [
            input_definition
            for input_definition in self.input_definitions
            if self.input_definition_is_a_missing_output_directory(
                input_definition
            )
        ]

    def get_missing_dynamic_default_definitions(
        self,
    ) -> List[StringInputDefinition]:
        """
        Returns a list of missing string inputs with a
        :attr:`~django_analyses.models.input.definitions.string_input_definition.StringInputDefinition.dynamic_default`
        value.

        Returns
        -------
        List[StringInputDefinition]
            List of missing dynamic_default instances
        """

        return [
            input_definition
            for input_definition in self.input_definitions
            if getattr(input_definition, "dynamic_default", False)
            and input_definition.key not in self.raw_configuration
        ]

    def get_missing_input_definitions(self) -> Set[InputDefinition]:
        """
        Returns the
        :class:`~django_analyses.models.input.definitions.input_definition.InputDefinition`
        subclass instances missing in the configuration for the given run.

        Returns
        -------
        Set[InputDefinition]
            Input definitions missing in the provided configuration
        """

        return set(
            self.get_missing_output_path_definitions()
            + self.get_missing_output_directory_definition()
            + self.get_missing_dynamic_default_definitions()
        )

    def get_or_create_missing_inputs(self) -> List[Input]:
        """
        Returns a list of :class:`~django_analysese.models.input.input.Input`
        subclass instances required to complete the provided run's input
        configuration.

        Returns
        -------
        List[Input]
            Missing input instances
        """

        return [
            input_definition.get_or_create_input_instance(run=self.run)[0]
            for input_definition in self.missing_input_definitions
        ]

    def get_or_create_input_instance_from_raw(
        self, key: str, value: Any
    ) -> Tuple[Input, bool]:
        """
        Get or create the appropriate
        :class:`~django_analysese.models.input.input.Input` instance from
        some user-provided dictionary item configuration.

        Parameters
        ----------
        key : str
            Input definition key
        value : Any
            Input value

        Returns
        -------
        Tuple[Input, bool]
            Matching Input instance and whether is has been created or not

        Raises
        ------
        InputDefinition.DoesNotExist
            Invalid input definition key within the input dictionary
        """

        try:
            input_definition = self.input_definitions.get(key=key)
        except InputDefinition.DoesNotExist:
            message = BAD_KEY.format(key=key)
            raise InputDefinition.DoesNotExist(message)
        else:
            return input_definition.get_or_create_input_instance(
                value=value, run=self.run
            )

    def convert_raw_configuration_to_input_instances(self) -> List[Input]:
        """
        Coverts a user-provided input configuration dictionary to
        :class:`~django_analyses.models.input.input.Input` subclass instances.

        Returns
        -------
        List[Input]
            Created inputs
        """

        return [
            self.get_or_create_input_instance_from_raw(key, value)[0]
            for key, value in self.raw_configuration.items()
        ]

    def get_all_input_instances(self) -> List[Input]:
        """
        Returns all
        :class:`~django_analyses.models.input.input.Input` subclass instances
        for the provided run.

        Returns
        -------
        List[Input]
            Input instances
        """

        return self.raw_input_instances + self.missing_inputs

    def get_required_paths(self) -> List[Input]:
        """
        Returns all input instances that require some parent directory to
        exist.

        Returns
        -------
        List[Input]
            Input instances
        """

        return [
            input_instance.required_path
            for input_instance in self.all_input_instances
            if getattr(input_instance, "required_path", None)
        ]

    def create_required_paths(self) -> None:
        """
        Creates all the directories required for generated files.
        """

        for required_path in self.required_paths:
            required_path.mkdir(parents=True, exist_ok=True)

    def get_full_configuration(self) -> dict:
        """
        Returns the complete input configuration dictionary to be passed to the
        appropriate analysis interface.

        Returns
        -------
        dict
            Full input configuration
        """

        return {
            input_instance.key: input_instance.argument_value
            for input_instance in self.all_input_instances
        }

    def create_input_instances(self) -> dict:
        """
        Creates all the required
        :class:`~django_analyses.models.input.input.Input` subclass instances
        for the provided run, including the creation of the destination
        directories of generated files.

        Returns
        -------
        dict
            Full input configuration
        """

        self.create_required_paths()
        return self.get_full_configuration()

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
