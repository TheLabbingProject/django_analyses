from factory import Faker
from factory.django import DjangoModelFactory


class AnalysisFactory(DjangoModelFactory):
    title = Faker("pystr", min_chars=3, max_chars=18)
    description = Faker("paragraph", nb_sentences=3, variable_nb_sentences=True)

    class Meta:
        model = "django_analyses.Analysis"
