from factory import SubFactory
from factory.django import DjangoModelFactory
from factory.faker import Faker


class FloatOutputFactory(DjangoModelFactory):
    run = SubFactory("tests.factories.run.RunFactory")
    definition = SubFactory(
        "tests.factories.output.definitions.float_output_definition.FloatOutputDefinitionFactory"
    )
    value = Faker("pyfloat")

    class Meta:
        model = "django_analyses.FloatOutput"
