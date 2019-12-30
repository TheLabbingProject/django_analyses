from factory import Faker
from factory.django import DjangoModelFactory


class ListInputDefinitionFactory(DjangoModelFactory):
    min_length = Faker("pyint", min_value=2, max_value=4)
    max_length = Faker("pyint", min_value=7, max_value=10)

    class Meta:
        model = "django_analyses.ListInputDefinition"
