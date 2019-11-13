from django_analysis.analysis.analysis_definitions import analysis_definitions
from django_analysis.models.analysis import Analysis
from django_analysis.models.analysis_version import AnalysisVersion
from django_analysis.models.input_specification import InputSpecification
from django_analysis.models.output_specification import OutputSpecification


class DefinitionsManager:
    INPUT_SPECIFICATION_KEY = "input"
    OUTPUT_SPECIFICATION_KEY = "output"
    ANALYSIS_CLASS_KEY = "class"
    RUN_METHOD = "run"
    NESTED_RESULTS_KEY = "nested_results"

    def get_analysis_definition(self, analysis: Analysis) -> dict:
        try:
            return analysis_definitions[analysis.title]
        except AttributeError:
            raise ValueError(f"No analysis definition found for {analysis.title}!")

    def get_version_definition(self, analysis_version: AnalysisVersion) -> dict:
        analysis_definition = self.get_analysis_definition(analysis_version.analysis)
        try:
            return analysis_definition[analysis_version.title]
        except AttributeError:
            raise ValueError(
                f"Invalid version '{analysis_version.title}' for analysis '{analysis_version.analysis.title}'"
            )

    def get_run_method_key(self, analysis_version: AnalysisVersion) -> str:
        version_definition = self.get_version_definition(analysis_version)
        return version_definition.get("run_method") or self.RUN_METHOD

    def get_analysis_class(self, analysis_version: AnalysisVersion) -> object:
        version_definition = self.get_version_definition(analysis_version)
        return version_definition[self.ANALYSIS_CLASS_KEY]

    def create_analysis_instance(self, analysis_version: AnalysisVersion, **kwargs):
        analysis_class = self.get_analysis_class(analysis_version)
        return analysis_class(**kwargs)

    def get_nested_results(self, analysis_version: AnalysisVersion, results) -> dict:
        nested_definition = self.get_nested_results_definition(analysis_version)
        for nested_attribute in nested_definition:
            results = getattr(results, nested_attribute)
        return results if isinstance(results, dict) else results()

    def run_analysis(self, analysis_version: AnalysisVersion, **kwargs) -> dict:
        analysis_instance = self.create_analysis_instance(analysis_version, **kwargs)
        run_method_key = self.get_run_method_key(analysis_version)
        run_method = getattr(analysis_instance, run_method_key)
        results = run_method()
        return self.get_nested_results(analysis_version, results)

    def get_input_specification_definition(
        self, analysis_version: AnalysisVersion
    ) -> dict:
        version_definition = self.get_version_definition(analysis_version)
        return version_definition[self.INPUT_SPECIFICATION_KEY]

    def get_output_specification_definition(
        self, analysis_version: AnalysisVersion
    ) -> dict:
        version_definition = self.get_version_definition(analysis_version)
        return version_definition[self.OUTPUT_SPECIFICATION_KEY]

    def update_input_specification_from_definition(
        self, analysis_version: AnalysisVersion
    ) -> None:
        input_specification_definition = self.get_input_specification_definition(
            analysis_version
        )
        input_specification, created = InputSpecification.objects.from_dict(
            analysis_version.analysis, input_specification_definition
        )
        analysis_version.input_specification = input_specification

    def update_output_specification_from_definition(
        self, analysis_version: AnalysisVersion
    ) -> None:
        output_specification_definition = self.get_output_specification_definition(
            analysis_version
        )
        output_specification, created = OutputSpecification.objects.from_dict(
            analysis_version.analysis, output_specification_definition
        )
        analysis_version.output_specification = output_specification

    def update_from_definition(
        self, analysis_version: AnalysisVersion, save: bool = True
    ) -> None:
        self.update_input_specification_from_definition(analysis_version)
        self.update_output_specification_from_definition(analysis_version)
        if save:
            analysis_version.save()

    def get_nested_results_definition(self, analysis_version: AnalysisVersion) -> dict:
        version_definition = self.get_version_definition(analysis_version)
        nested_results_definition = version_definition.get(self.NESTED_RESULTS_KEY)
        return nested_results_definition.split(".") if nested_results_definition else []
