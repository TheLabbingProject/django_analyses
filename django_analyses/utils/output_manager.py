from django.core.exceptions import ObjectDoesNotExist
from django_analyses.models.output.output import Output


class OutputManager:
    def __init__(self, run, results: dict):
        self.run = run
        self.results = results
        self.output_definitions = self.run.analysis_version.output_definitions

    def create_output_instance(self, key: str, value) -> Output:
        try:
            output_definition = self.output_definitions.get(key=key)
        except ObjectDoesNotExist:
            pass
        else:
            return output_definition.create_output_instance(value=value, run=self.run)

    def create_output_instances(self) -> list:
        output_instances = [
            self.create_output_instance(key, value)
            for key, value in self.results.items()
        ]
        return [output for output in output_instances if output is not None]
