from factory import SubFactory
from factory.django import DjangoModelFactory
from factory.faker import Faker


class StringInputFactory(DjangoModelFactory):
    run = SubFactory("tests.factories.run.RunFactory")
    definition = SubFactory(
        "tests.factories.input.definitions.string_input_definition.StringInputDefinitionFactory",
        min_length=5,
        max_length=300,
    )
    value = Faker("pystr", min_chars=5, max_chars=40)

    class Meta:
        model = "django_analyses.StringInput"

