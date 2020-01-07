from factory import Faker
from factory.django import DjangoModelFactory


class InputDefinitionFactory(DjangoModelFactory):
    key = Faker("pystr", min_chars=3, max_chars=50)
    required = Faker("pybool")
    description = Faker("sentence")
    is_configuration = Faker("pybool")

    class Meta:
        model = "django_analyses.InputDefinition"
