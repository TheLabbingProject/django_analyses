from factory import Faker
from factory.django import DjangoModelFactory


class FileInputDefinitionFactory(DjangoModelFactory):
    key = Faker("word")
    required = Faker("pybool")
    description = Faker("sentence")

    class Meta:
        model = "django_analyses.FileInputDefinition"
