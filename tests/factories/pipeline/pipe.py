from factory import SubFactory
from factory.django import DjangoModelFactory


class PipeFactory(DjangoModelFactory):
    pipeline = SubFactory("tests.factories.pipeline.pipeline.PipelineFactory")
    source = SubFactory("tests.factories.pipeline.node.NodeFactory")
    base_source_port = SubFactory(
        "tests.factories.output.definitions.output_definition.OutputDefinitionFactory"
    )
    destination = SubFactory("tests.factories.pipeline.node.NodeFactory")
    base_destination_port = SubFactory(
        "tests.factories.input.definitions.input_definition.InputDefinitionFactory"
    )

    class Meta:
        model = "django_analyses.Pipe"
