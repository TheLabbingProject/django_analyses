from factory import SubFactory
from factory.django import DjangoModelFactory


class AnalysisVersionFactory(DjangoModelFactory):
    analysis = SubFactory("django_analyses.Analysis")

    class Meta:
        model = "django_analyses.AnalysisVersion"
