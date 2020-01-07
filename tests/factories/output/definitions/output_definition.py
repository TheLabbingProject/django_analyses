from factory import Faker
from factory.django import DjangoModelFactory


class OutputDefinitionFactory(DjangoModelFactory):
    key = Faker("pystr", min_chars=3, max_chars=50)
    description = Faker("sentence")

    class Meta:
        model = "django_analyses.OutputDefinition"
