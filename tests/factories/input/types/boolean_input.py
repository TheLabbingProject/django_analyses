from factory import SubFactory
from factory.django import DjangoModelFactory
from factory.faker import Faker


class BooleanInputFactory(DjangoModelFactory):
    run = SubFactory("tests.factories.run.RunFactory")
    definition = SubFactory(
        "tests.factories.input.definitions.boolean_input_definition.BooleanInputDefinitionFactory"
    )
    value = Faker("pybool")

    class Meta:
        model = "django_analyses.BooleanInput"
