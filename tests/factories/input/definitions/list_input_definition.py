from factory import Faker
from factory.django import DjangoModelFactory


class ListInputDefinitionFactory(DjangoModelFactory):
    key = Faker("pystr", min_chars=3, max_chars=50)
    required = Faker("pybool")
    description = Faker("sentence")
    min_length = Faker("pyint", min_value=2, max_value=4)
    max_length = Faker("pyint", min_value=7, max_value=10)

    class Meta:
        model = "django_analyses.ListInputDefinition"
