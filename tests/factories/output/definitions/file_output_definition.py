from factory import Faker
from factory.django import DjangoModelFactory


class FileOutputDefinitionFactory(DjangoModelFactory):
    key = Faker("word")
    description = Faker("sentence")

    class Meta:
        model = "django_analyses.FileOutputDefinition"
