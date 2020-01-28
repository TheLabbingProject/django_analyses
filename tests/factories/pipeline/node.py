from factory import Faker, SubFactory
from factory.django import DjangoModelFactory


class NodeFactory(DjangoModelFactory):
    analysis_version = SubFactory(
        "tests.factories.analysis_version.AnalysisVersionFactory"
    )
    created = Faker("date_between", start_date="-30d", end_date="-15d")
    modified = Faker("date_between", start_date="-14d", end_date="today")

    class Meta:
        model = "django_analyses.Node"
