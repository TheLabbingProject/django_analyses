from factory import Faker
from factory.django import DjangoModelFactory


class AnalysisFactory(DjangoModelFactory):
    title = Faker("sentence", nb_words=3, variable_nb_words=True)
    description = Faker("paragraph", nb_sentences=3, variable_nb_sentences=True)

    class Meta:
        model = "django_analyses.Analysis"
