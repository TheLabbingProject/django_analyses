"""
Definition of the
:class:`~django_analyses.models.analysis_version.AnalysisVersion` class.

"""

from django.conf import settings
from django.contrib.postgres.fields import JSONField
from django.db import models
from django_analyses.models.managers.analysis_version import AnalysisVersionManager
from django_extensions.db.models import TitleDescriptionModel, TimeStampedModel


class AnalysisVersion(TitleDescriptionModel, TimeStampedModel):
    """
    :class:`~django.db.models.Model` representing a single analysis version in the
    database.

    Each :class:`~django_analyses.models.analysis_version.AnalysisVersion` instance
    should be assigned an interface through the project's :attr:`ANALYSIS_INTERFACES`
    setting (for more information see
    :ref:`user_guide/analysis_integration/simplified_example:Interface Integration`
    and
    :ref:`user_guide/analysis_integration/integration_customization:Integration Customization`).



    """

    analysis = models.ForeignKey(
        "django_analyses.Analysis",
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        related_name="version_set",
    )
    input_specification = models.ForeignKey(
        "django_analyses.InputSpecification",
        on_delete=models.PROTECT,
        blank=True,
        null=True,
        related_name="analysis_version_set",
    )
    output_specification = models.ForeignKey(
        "django_analyses.OutputSpecification",
        on_delete=models.PROTECT,
        blank=True,
        null=True,
        related_name="analysis_version_set",
    )

    # Integration customization
    run_method_key = models.CharField(max_length=100, default="run")
    fixed_run_method_kwargs = JSONField(default=dict)
    nested_results_attribute = models.CharField(max_length=100, blank=True, null=True)

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
        :obj:`str`
            String representation of this instance
        """

        return f"{self.analysis.title} v{self.title}"

    def get_interface(self) -> object:
        """
        Queries the project's settings to locate the instance's interface.
        For more information see
        :ref:`user_guide/analysis_integration/simplified_example:Interface Integration`.

        Returns
        -------
        :obj:`object`
            Interface class used to run this version of the analysis

        Raises
        ------
        NotImplementedError
            No interface could be found for this analysis
        """

        try:
            return settings.ANALYSIS_INTERFACES[self.analysis.title][self.title]
        except KeyError:
            raise NotImplementedError(f"No interface detected for {self}!")

    def get_interface_initialization_kwargs(self, **kwargs) -> dict:
        """
        Returns the parameters required at the interface's class initialization.

        Returns
        -------
        :obj:`dict`
            Initialization parameters as a keyword arguments :obj:`dict`.
        """

        return {
            key: value
            for key, value in kwargs.items()
            if not self.input_definitions.get(key=key).run_method_input
        }

    def get_run_method_kwargs(self, **kwargs) -> dict:
        """
        Returns the parameters required when calling the interface's :meth:`run` method.

        Returns
        -------
        :obj:`dict`
            :meth:`run` method parameters as a keyword arguments :obj:`dict`.
        """

        return {
            key: value
            for key, value in kwargs.items()
            if self.input_definitions.get(key=key).run_method_input
        }

    def run_interface(self, **kwargs) -> dict:
        """
        Call the interface class's :meth:`run` method with the given keyword arguments.

        Returns
        -------
        :obj:`dict`
            Dictionary of results
        """

        interface = self.get_interface()

        # Initialize the interface class
        init_kwargs = self.get_interface_initialization_kwargs(**kwargs)
        instance = interface(**init_kwargs)

        # Prepare run method kwargs
        run_method_kwargs = {
            **self.fixed_run_method_kwargs,
            **self.get_run_method_kwargs(**kwargs),
        }

        # Run the analysis and return the results dictionary
        run_method = getattr(instance, self.run_method_key)
        return run_method(**run_method_kwargs)

    def extract_results(self, results: object) -> dict:
        """
        Extracts a results dictionary from an arbitrary results :obj:`object` in case the
        :attr:`~django_analyses.models.analysis_version.AnalysisVersion.nested_results_attribute`
        is not :obj:`None`.

        Parameters
        ----------
        results : :obj:`object`
            Arbitrary results object

        Returns
        -------
        :obj:`dict`
            Results dictionary
        """

        for nested_attribute in self.nested_results_parts:
            results = getattr(results, nested_attribute)
        return results if isinstance(results, dict) else results()

    def run(self, **kwargs) -> dict:
        """
        Runs the interface safely by validating the input according to the instance's
        :attr:`~django_analyses.models.analysis_version.AnalysisVersion.input_specification`
        and applying any special integration customizations (for more information see
        :ref:`user_guide/analysis_integration/integration_customization:Integration Customization`).

        Returns
        -------
        :obj:`dict`
            Results dictionary
        """

        self.input_specification.validate_kwargs(**kwargs)
        raw_results = self.run_interface(**kwargs)
        return self.extract_results(raw_results)

    def update_input_with_defaults(self, **kwargs) -> dict:
        """
        Updates a configuration specified as keyword arguments with the instance's
        :attr:`~django_analyses.models.analysis_version.AnalysisVersion.input_specification`
        defaults.

        Returns
        -------
        :obj:`dict`
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
        :obj:`list`
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
        sub-classes as defined in its
        :attr:`~django_analyses.models.analysis_version.AnalysisVersion.input_specification`.


        Returns
        -------
        :class:`~django.db.models.query.QuerySet`
            :class:`~django_analyses.models.input.definitions.input_definition.InputDefinition`
            sub-classes.
        """

        return self.input_specification.input_definitions

    @property
    def output_definitions(self) -> models.QuerySet:
        """
        Returns the associated instance's
        :class:`~django_analyses.models.output.definitions.output_definition.OutputDefinition`
        sub-classes as defined in its
        :attr:`~django_analyses.models.analysis_version.AnalysisVersion.output_specification`.


        Returns
        -------
        :class:`~django.db.models.query.QuerySet`
            :class:`~django_analyses.models.output.definitions.output_definition.OutputDefinition`
            sub-classes.
        """

        return self.output_specification.output_definitions
