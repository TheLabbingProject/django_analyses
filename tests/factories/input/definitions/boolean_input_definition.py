from factory import Faker
from factory.django import DjangoModelFactory


class BooleanInputDefinitionFactory(DjangoModelFactory):
    key = Faker("pystr", min_chars=3, max_chars=50)
    required = Faker("pybool")
    description = Faker("sentence")
    default = Faker("pybool")

    class Meta:
        model = "django_analyses.BooleanInputDefinition"
