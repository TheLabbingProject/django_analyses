from factory import Faker
from factory.django import DjangoModelFactory


class IntegerInputDefinitionFactory(DjangoModelFactory):
    min_value = Faker("pyint", min_value=-20, max_value=-10)
    max_value = Faker("pyint", min_value=20, max_value=40)
    default = Faker("pyint", min_value=-10, max_value=20)

    class Meta:
        model = "django_analyses.IntegerInputDefinition"
