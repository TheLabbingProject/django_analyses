from django_analysis.models.analysis_version import AnalysisVersion
from django_extensions.db.models import TitleDescriptionModel, TimeStampedModel


class Analysis(TitleDescriptionModel, TimeStampedModel):
    pass

    def __str__(self) -> str:
        return self.title

    def get_latest_version(self) -> AnalysisVersion:
        return self.analysis_version_set.last()
