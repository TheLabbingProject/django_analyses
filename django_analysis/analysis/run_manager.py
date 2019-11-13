from django.db.models import QuerySet
from django_analysis.analysis.definitions_manager import DefinitionsManager
from django_analysis.models.analysis_version import AnalysisVersion
from django_analysis.models.run import Run


class RunManager:
    def __init__(self):
        self.definitions_manager = DefinitionsManager()

    def create_input_instances(self, run: Run, **kwargs) -> list:
        input_definitions = run.analysis_version.get_input_definitions_for_kwargs(
            **kwargs
        )
        inputs = []
        for key, value in kwargs.items():
            input_definition = input_definitions.get(key=key)
            input_instance = input_definition.INPUT_CLASS.objects.create(
                value=value, definition=input_definition, run=run
            )
            inputs.append(input_instance)
        return inputs

    def create_output_instances(self, run: Run, **results) -> list:
        output_definitions = run.analysis_version.get_output_definitions_for_results(
            **results
        )
        outputs = []
        for key, value in results.items():
            output_definition = output_definitions.get(key=key)
            output_instance = output_definition.OUTPUT_CLASS.objects.create(
                value=value, definition=output_definition, run=run
            )
            outputs.append(output_instance)
        return outputs

    def get_complete_configuration(
        self, analysis_version: AnalysisVersion, **kwargs
    ) -> dict:
        configuration = (
            analysis_version.input_specification.get_default_input_configurations()
        )
        configuration.update(kwargs)
        return configuration

    def get_existing_run(self, analysis_version: AnalysisVersion, **kwargs) -> Run:
        runs = Run.objects.filter(analysis_version=analysis_version)
        configuration = self.get_complete_configuration(analysis_version, **kwargs)
        matching = [run for run in runs if run.input_configuration == configuration]
        return matching[0] if matching else None

    def create_run(self, analysis_version: AnalysisVersion, **kwargs) -> Run:
        run = Run.objects.create(analysis_version=analysis_version)
        self.create_input_instances(run, **kwargs)
        results = self.definitions_manager.run_analysis(analysis_version, **kwargs)
        self.create_output_instances(run, **results)
        return run

    def run(self, analysis_version: AnalysisVersion, **kwargs) -> Run:
        existing_run = self.get_existing_run(analysis_version, **kwargs)
        return existing_run or self.create_run(analysis_version, **kwargs)
