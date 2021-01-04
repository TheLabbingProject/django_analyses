"""
Definition of the :class:`AnalysisVersion` class.
"""
from django.db import models
from django_analyses.models.managers.analysis_version import (
    AnalysisVersionManager,
)
from django_analyses.models.utils import get_analysis_version_interface
from django_extensions.db.models import TitleDescriptionModel, TimeStampedModel
from typing import Any


class AnalysisVersion(TitleDescriptionModel, TimeStampedModel):
    """
    A :class:`~django.db.models.Model` representing a single analysis version
    in the database.

    Each :class:`~django_analyses.models.analysis_version.AnalysisVersion`
    instance should be assigned an interface through the project's
    :attr:`ANALYSIS_INTERFACES` setting (for more information see
    :ref:`user_guide/analysis_integration/simplified_example:Interface
    Integration` and
    :ref:`user_guide/analysis_integration/integration_customization:Integration
    Customization`).
    """

    analysis = models.ForeignKey(
        "django_analyses.Analysis",
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        related_name="version_set",
    )
    """
    The :class:`~django_analyses.models.analysis.Analysis` instance to which
    this analysis version belongs.
    """

    input_specification = models.ForeignKey(
        "django_analyses.InputSpecification",
        on_delete=models.PROTECT,
        blank=True,
        null=True,
        related_name="analysis_version_set",
    )
    """
    The
    :class:`~django_analyses.models.input.input_specification.InputSpecification`
    instance specifying the
    :class:`~django_analyses.models.input.definitions.input_definition.InputDefinition`
    subclasses associated with this analysis version.
    """

    output_specification = models.ForeignKey(
        "django_analyses.OutputSpecification",
        on_delete=models.PROTECT,
        blank=True,
        null=True,
        related_name="analysis_version_set",
    )
    """
    The
    :class:`~django_analyses.models.output.output_specification.OutputSpecification`
    instance specifying the
    :class:`~django_analyses.models.output.definitions.output_definition.OutputDefinition`
    subclasses associated with this analysis version.
    """

    #############################
    # Integration customization #
    #############################

    run_method_key = models.CharField(max_length=100, default="run")
    """
    Custom *run* method name for the interface.
    Each analysis version is expected to have some class associated with it and
    used as an interface for running the analysis. This field determines the
    name of the method that will be called (default value is *"run"*).
    """

    fixed_run_method_kwargs = models.JSONField(default=dict)
    """
    Any "fixed" keyword arguments that should always be passed to the
    interface's *run* method at execution.
    """

    nested_results_attribute = models.CharField(
        max_length=100, blank=True, null=True
    )
    """
    Analysis interfaces are expected to return a dictionary of the results. In
    case this analysis version's interface returns some object which conatins
    the desired dictionary, this field allows specifying the attribute or
    method that may be used to retrieve it.

    Example
    -------
    Nipype_\'s interfaces generally return some kind of
    :class:`InterfaceResults` object with an :attr:`outputs` attribute that may
    be used to create a dictionary of the results by calling the
    :meth:`get_traitsfree` method.
    In order to integrate smoothly with Nipype's interfaces, we could simply
    specify *nested_results_attribute="outputs.get_traitsfree"* when creating
    the appropriate analysis versions.

    .. _Nipype: https://nipype.readthedocs.io/en/latest/
    """

    #####################
    # Execution Options #
    #####################

    max_parallel = models.PositiveIntegerField(default=4)
    """
    Maximal number of parallel executions that may be run using Celery_. This
    attribute is used in :func:`~django_analyses.tasks.execute_node` to
    chunk an iterable of node inputs in case it is longer than this value.
    For more information see Celery's `Chunks documentation`_.

    .. _Celery:
       https://docs.celeryproject.org/
    .. _Chunks documentation:
       https://docs.celeryproject.org/en/stable/userguide/canvas.html#chunks
    """

    objects = AnalysisVersionManager()

    class Meta:
        unique_together = "analysis", "title"
        ordering = ("-title",)

    def __str__(self) -> str:
        """
        Returns the string representation of the
        :class:`~django_analyses.models.analysis_version.AnalysisVersion`
        instance.

        Returns
        -------
        str
            String representation of this instance
        """

        return f"{self.analysis.title} v{self.title}"

    def get_interface(self) -> object:
        """
        Queries the project's settings to locate the instance's interface.
        For more information see
        :ref:`user_guide/analysis_integration/simplified_example:Interface
        Integration`.

        Returns
        -------
        :obj:`object`
            Interface class used to run this version of the analysis

        Raises
        ------
        NotImplementedError
            No interface could be found for this analysis
        """

        return get_analysis_version_interface(self)

    def get_interface_initialization_kwargs(self, **kwargs) -> dict:
        """
        Returns the parameters required at the interface's class
        initialization.

        Returns
        -------
        dict
            Initialization parameters as a keyword arguments dict
        """

        return {
            key: value
            for key, value in kwargs.items()
            if not self.input_definitions.get(key=key).run_method_input
        }

    def get_run_method_kwargs(self, **kwargs) -> dict:
        """
        Returns the parameters required when calling the interface's
        :meth:`run` method.

        Returns
        -------
        dict
            :meth:`run` method parameters as a keyword arguments dict
        """

        return {
            key: value
            for key, value in kwargs.items()
            if self.input_definitions.get(key=key).run_method_input
        }

    def run_interface(self, **kwargs) -> dict:
        """
        Call the interface class's :meth:`run` method with the given keyword
        arguments.

        Returns
        -------
        dict
            Dictionary of results
        """

        # Initialize the interface class
        init_kwargs = self.get_interface_initialization_kwargs(**kwargs)
        instance = self.interface(**init_kwargs)

        # Prepare run method kwargs
        run_method_kwargs = {
            **self.fixed_run_method_kwargs,
            **self.get_run_method_kwargs(**kwargs),
        }

        # Run the analysis and return the results dictionary
        run_method = getattr(instance, self.run_method_key)
        return run_method(**run_method_kwargs)

    def extract_results(self, results: Any) -> dict:
        """
        Extracts a results dictionary from an arbitrary results object in case
        the :attr:`nested_results_attribute` is not `None`.

        Parameters
        ----------
        results : Any
            Arbitrary results object

        Returns
        -------
        dict
            Results dictionary
        """

        for nested_attribute in self.nested_results_parts:
            results = getattr(results, nested_attribute)
        return results if isinstance(results, dict) else results()

    def run(self, **kwargs) -> dict:
        """
        Runs the interface safely by validating the input according to the
        instance's
        :attr:`~django_analyses.models.analysis_version.AnalysisVersion.input_specification`
        and applying any special integration customizations (for more
        information see
        :ref:`user_guide/analysis_integration/integration_customization:Integration
        Customization`).

        Returns
        -------
        dict
            Results dictionary
        """

        self.input_specification.validate_kwargs(**kwargs)
        raw_results = self.run_interface(**kwargs)
        return self.extract_results(raw_results)

    def update_input_with_defaults(self, **kwargs) -> dict:
        """
        Updates a configuration specified as keyword arguments with the
        instance's
        :attr:`~django_analyses.models.analysis_version.AnalysisVersion.input_specification`
        defaults.

        Returns
        -------
        dict
            Configuration updated with default values
        """

        configuration = self.input_specification.default_configuration.copy()
        configuration.update(kwargs)
        return configuration

    @property
    def nested_results_parts(self) -> list:
        """
        Splits the
        :attr:`~django_analyses.models.analysis_version.AnalysisVersion.nested_results_attribute`
        at *"."* indices in case of a deeply nested attribute.

        Returns
        -------
        list
            Listed parts of nested result dictionary location
        """

        return (
            self.nested_results_attribute.split(".")
            if self.nested_results_attribute
            else []
        )

    @property
    def input_definitions(self) -> models.QuerySet:
        """
        Returns the associated instance's
        :class:`~django_analyses.models.input.definitions.input_definition.InputDefinition`
        subclasses as defined in its
        :attr:`~django_analyses.models.analysis_version.AnalysisVersion.input_specification`.


        Returns
        -------
        :class:`~django.db.models.query.QuerySet`
            :class:`~django_analyses.models.input.definitions.input_definition.InputDefinition`
            subclasses
        """

        return self.input_specification.input_definitions

    @property
    def output_definitions(self) -> models.QuerySet:
        """
        Returns the associated instance's
        :class:`~django_analyses.models.output.definitions.output_definition.OutputDefinition`
        subclasses as defined in its
        :attr:`~django_analyses.models.analysis_version.AnalysisVersion.output_specification`.


        Returns
        -------
        :class:`~django.db.models.query.QuerySet`
            :class:`~django_analyses.models.output.definitions.output_definition.OutputDefinition`
            subclasses
        """

        return self.output_specification.output_definitions

    @property
    def interface(self) -> type:
        """
        Returns the associated interface for this instance.

        Returns
        -------
        type
            Analysis interface class
        """

        return self.get_interface()
