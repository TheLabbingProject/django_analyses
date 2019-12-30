from factory import Faker
from factory.django import DjangoModelFactory


class FloatInputDefinitionFactory(DjangoModelFactory):
    key = Faker("word")
    required = Faker("pybool")
    description = Faker("sentence")
    min_value = Faker("pyfloat", min_value=-20, max_value=-10)
    max_value = Faker("pyfloat", min_value=20, max_value=40)
    default = Faker("pyfloat", min_value=-10, max_value=20)

    class Meta:
        model = "django_analyses.FloatInputDefinition"
