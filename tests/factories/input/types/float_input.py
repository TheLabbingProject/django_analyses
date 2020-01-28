from factory import SubFactory
from factory.django import DjangoModelFactory
from factory.faker import Faker


class FloatInputFactory(DjangoModelFactory):
    run = SubFactory("tests.factories.run.RunFactory")
    definition = SubFactory(
        "tests.factories.input.definitions.float_input_definition.FloatInputDefinitionFactory"
    )
    value = Faker("pyfloat", min_value=-1000, max_value=1000)

    class Meta:
        model = "django_analyses.FloatInput"
