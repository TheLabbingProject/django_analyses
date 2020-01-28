from factory import SubFactory
from factory.django import DjangoModelFactory


class RunFactory(DjangoModelFactory):
    analysis_version = SubFactory(
        "tests.factories.analysis_version.AnalysisVersionFactory"
    )
    user = SubFactory("tests.factories.user.UserFactory")

    class Meta:
        model = "django_analyses.Run"
