import factory

from factory.django import DjangoModelFactory
from tests.factories.analysis import AnalysisFactory
from tests.factories.input.definitions.boolean_input_definition import (
    BooleanInputDefinitionFactory,
)
from tests.factories.input.definitions.file_input_definition import (
    FileInputDefinitionFactory,
)
from tests.factories.input.definitions.float_input_definition import (
    FloatInputDefinitionFactory,
)
from tests.factories.input.definitions.integer_input_definition import (
    IntegerInputDefinitionFactory,
)
from tests.factories.input.definitions.list_input_definition import (
    ListInputDefinitionFactory,
)
from tests.factories.input.definitions.string_input_definition import (
    StringInputDefinitionFactory,
)


class InputSpecificationFactory(DjangoModelFactory):
    analysis = factory.SubFactory(AnalysisFactory)

    class Meta:
        model = "django_analyses.InputSpecification"

    @factory.post_generation
    def base_input_definitions(self, create, extracted, **kwargs):
        if create:
            if extracted:
                # A list of base_input_definitions was passed in, use it
                for base_input_definition in extracted:
                    self.base_input_definitions.add(base_input_definition)
            else:
                self.base_input_definitions.add(BooleanInputDefinitionFactory())
                self.base_input_definitions.add(FileInputDefinitionFactory())
                self.base_input_definitions.add(FloatInputDefinitionFactory())
                self.base_input_definitions.add(IntegerInputDefinitionFactory())
                self.base_input_definitions.add(ListInputDefinitionFactory())
                self.base_input_definitions.add(StringInputDefinitionFactory())

            # Validate that at least one definition is required
            if not self.base_input_definitions.filter(required=True):
                definition = self.base_input_definitions.first()
                definition.required = True
                definition.save()
