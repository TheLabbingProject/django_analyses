import factory
from factory.django import DjangoModelFactory
from tests.factories.analysis import AnalysisFactory
from tests.factories.output.definitions.file_output_definition import \
    FileOutputDefinitionFactory


class OutputSpecificationFactory(DjangoModelFactory):
    analysis = factory.SubFactory(AnalysisFactory)

    class Meta:
        model = "django_analyses.OutputSpecification"

    @factory.post_generation
    def base_output_definitions(self, create, extracted, **kwargs):
        if create:
            if extracted:
                # A list of base_output_definitions was passed in, use it
                for base_output_definition in extracted:
                    self.base_output_definitions.add(base_output_definition)
            else:
                self.base_output_definitions.add(FileOutputDefinitionFactory())
                self.base_output_definitions.add(FileOutputDefinitionFactory())
                self.base_output_definitions.add(FileOutputDefinitionFactory())

