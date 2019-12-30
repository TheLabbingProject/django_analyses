import factory

from tests.factories.analysis import AnalysisFactory
from factory.django import DjangoModelFactory


class InputSpecificationFactory(DjangoModelFactory):
    analysis = factory.SubFactory(AnalysisFactory)

    class Meta:
        model = "django_analyses.InputSpecification"

    @factory.post_generation
    def base_input_definition(self, create, extracted, **kwargs):
        if not create:
            # Simple build, do nothing.
            return

        if extracted:
            # A list of base_input_definitions was passed in, use it
            for base_input_definition in extracted:
                self.base_input_definitions.add(base_input_definition)

