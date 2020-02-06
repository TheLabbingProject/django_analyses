from factory import Faker
from factory.django import DjangoModelFactory


class DirectoryInputDefinitionFactory(DjangoModelFactory):
    key = Faker("pystr", min_chars=3, max_chars=50)
    required = Faker("pybool")
    description = Faker("sentence")

    class Meta:
        model = "django_analyses.DirectoryInputDefinition"
