from factory import SubFactory
from factory.django import DjangoModelFactory


class ListInputFactory(DjangoModelFactory):
    run = SubFactory("tests.factories.run.RunFactory")
    definition = SubFactory(
        "tests.factories.input.definitions.list_input_definition.ListInputDefinitionFactory"
    )

    class Meta:
        model = "django_analyses.ListInput"
