from factory import SubFactory
from factory.django import DjangoModelFactory
from factory.faker import Faker


class FileOutputFactory(DjangoModelFactory):
    run = SubFactory("tests.factories.run.RunFactory")
    definition = SubFactory(
        "tests.factories.output.definitions.file_output_definition.FileOutputDefinitionFactory"
    )
    value = Faker("file_path", depth=3)

    class Meta:
        model = "django_analyses.FileOutput"
