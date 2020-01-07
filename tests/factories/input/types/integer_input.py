from factory import SubFactory
from factory.django import DjangoModelFactory
from factory.faker import Faker


class IntegerInputFactory(DjangoModelFactory):
    run = SubFactory("tests.factories.run.RunFactory")
    definition = SubFactory(
        "tests.factories.input.definitions.integer_input_definition.IntegerInputDefinitionFactory"
    )
    value = Faker("pyint", min_value=-100, max_value=100)

    class Meta:
        model = "django_analyses.IntegerInput"
