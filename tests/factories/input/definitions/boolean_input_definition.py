from factory import Faker
from factory.django import DjangoModelFactory


class BooleanInputDefinitionFactory(DjangoModelFactory):
    default = Faker("pybool")

    class Meta:
        model = "django_analyses.BooleanInputDefinition"
