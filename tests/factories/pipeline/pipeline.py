from factory import Faker
from factory.django import DjangoModelFactory


class PipelineFactory(DjangoModelFactory):
    title = Faker("pystr", min_chars=3, max_chars=18)
    description = Faker("paragraph", nb_sentences=3, variable_nb_sentences=True)
    created = Faker("date_between", start_date="-30d", end_date="-15d")
    modified = Faker("date_between", start_date="-14d", end_date="today")

    class Meta:
        model = "django_analyses.Pipeline"
