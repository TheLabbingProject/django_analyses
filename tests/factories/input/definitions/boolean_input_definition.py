from factory import Faker
from factory.django import DjangoModelFactory


class BooleanInputDefinitionFactory(DjangoModelFactory):
    key = Faker("word")
    required = Faker("pybool")
    description = Faker("sentence")
    default = Faker("pybool")

    class Meta:
        model = "django_analyses.BooleanInputDefinition"
