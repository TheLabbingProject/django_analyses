from django.db.models import QuerySet
from django_analysis.analysis.definitions_manager import DefinitionsManager
from django_analysis.models.analysis_version import AnalysisVersion
from django_analysis.models.run import Run


class RunManager:
    def __init__(self):
        self.definitions_manager = DefinitionsManager()

    def get_input_definitions(self, run: Run, **kwargs) -> QuerySet:
        raw_definitions = run.analysis_version.input_specification.input_definitions
        return raw_definitions.filter(key__in=kwargs).select_subclasses()

    def create_input_instances(self, run: Run, **kwargs) -> list:
        input_definitions = self.get_input_definitions(run, **kwargs)
        inputs = []
        for key, value in kwargs.items():
            input_definition = input_definitions.get(key=key)
            input_instance = input_definition.INPUT_CLASS.objects.create(
                value=value, definition=input_definition, run=run
            )
            inputs.append(input_instance)
        return inputs

    def get_existing_run(self, analysis_version: AnalysisVersion, **kwargs) -> Run:
        runs = Run.objects.filter(analysis_version=analysis_version)
        matching = [run for run in runs if run.input_configuration == kwargs]
        return matching[0] if matching else None

    def initialize_analysis(self, analysis_version: AnalysisVersion, **kwargs) -> Run:
        run = Run.objects.create(analysis_version=analysis_version)
        self.create_input_instances(run, **kwargs)
        analysis_class = self.definitions_manager.get_analysis_class(analysis_version)
        return analysis_class(**kwargs)

