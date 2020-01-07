from factory import Faker
from factory.django import DjangoModelFactory


class FloatInputDefinitionFactory(DjangoModelFactory):
    key = Faker("pystr", min_chars=3, max_chars=50)
    required = Faker("pybool")
    description = Faker("sentence")
    min_value = Faker("pyfloat", min_value=-20, max_value=-10)
    max_value = Faker("pyfloat", min_value=20, max_value=40)
    default = Faker("pyfloat", min_value=-10, max_value=20)

    class Meta:
        model = "django_analyses.FloatInputDefinition"
