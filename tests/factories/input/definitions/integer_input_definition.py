from factory import Faker
from factory.django import DjangoModelFactory


class IntegerInputDefinitionFactory(DjangoModelFactory):
    key = Faker("pystr", min_chars=3, max_chars=50)
    required = Faker("pybool")
    description = Faker("sentence")
    min_value = Faker("pyint", min_value=-20, max_value=-10)
    max_value = Faker("pyint", min_value=20, max_value=40)
    default = Faker("pyint", min_value=-10, max_value=20)

    class Meta:
        model = "django_analyses.IntegerInputDefinition"
