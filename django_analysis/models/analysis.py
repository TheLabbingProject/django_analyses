from django_analysis.models.managers.analysis import AnalysisManager
from django_extensions.db.models import TitleDescriptionModel, TimeStampedModel


class Analysis(TitleDescriptionModel, TimeStampedModel):

    objects = AnalysisManager()

    def __str__(self) -> str:
        return self.title

    def get_latest_version(self):
        return self.analysis_version_set.last()
