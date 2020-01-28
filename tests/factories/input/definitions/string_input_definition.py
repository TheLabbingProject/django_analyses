from factory import Faker
from factory.django import DjangoModelFactory


class StringInputDefinitionFactory(DjangoModelFactory):
    key = Faker("pystr", min_chars=3, max_chars=50)
    required = Faker("pybool")
    description = Faker("sentence")
    min_length = Faker("pyint", min_value=0, max_value=10)
    max_length = Faker("pyint", min_value=20, max_value=500)
    default = Faker("pystr", min_chars=10, max_chars=20)

    class Meta:
        model = "django_analyses.StringInputDefinition"
