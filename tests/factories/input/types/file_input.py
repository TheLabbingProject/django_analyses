from factory import SubFactory
from factory.django import DjangoModelFactory
from factory.faker import Faker


class FileInputFactory(DjangoModelFactory):
    run = SubFactory("tests.factories.run.RunFactory")
    definition = SubFactory(
        "tests.factories.input.definitions.file_input_definition.FileInputDefinitionFactory"
    )
    value = Faker("file_path", depth=3)

    class Meta:
        model = "django_analyses.FileInput"
