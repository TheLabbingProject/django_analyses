from factory import Faker
from factory.django import DjangoModelFactory


class FloatOutputDefinitionFactory(DjangoModelFactory):
    key = Faker("pyfloat")
    description = Faker("sentence")

    class Meta:
        model = "django_analyses.FloatOutputDefinition"
