from django.contrib.auth import get_user_model
from django.db import models
from django_analyses.models.analysis_version import AnalysisVersion
from django_analyses.utils.input_manager import InputManager
from django_analyses.utils.output_manager import OutputManager


User = get_user_model()


class RunManager(models.Manager):
    def get_existing(self, analysis_version: AnalysisVersion, **kwargs):
        runs = self.filter(analysis_version=analysis_version)
        configuration = analysis_version.update_input_with_defaults(**kwargs)
        matching = [run for run in runs if run.input_configuration == configuration]
        return matching[0] if matching else None

    def create_and_execute(
        self, analysis_version: AnalysisVersion, user: User = None, **kwargs
    ):
        run = self.create(analysis_version=analysis_version, user=user)
        input_manager = InputManager(run=run, configuration=kwargs)
        inputs = input_manager.fix_input()
        results = analysis_version.run(**inputs)
        output_manager = OutputManager(run=run, results=results)
        output_manager.create_output_instances()
        return run

    def get_or_execute(
        self, analysis_version: AnalysisVersion, user: User = None, **kwargs
    ):
        existing = self.get_existing(analysis_version, **kwargs)
        return existing or self.create_and_execute(analysis_version, user, **kwargs)
