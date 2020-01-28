from factory import Faker
from factory.django import DjangoModelFactory


class CategoryFactory(DjangoModelFactory):
    title = Faker("sentence", nb_words=2, variable_nb_words=True)
    description = Faker("paragraph", nb_sentences=4, variable_nb_sentences=True)

    class Meta:
        model = "django_analyses.Category"
