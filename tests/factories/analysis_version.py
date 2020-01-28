from factory import SubFactory
from factory.django import DjangoModelFactory
from factory.faker import Faker


class AnalysisVersionFactory(DjangoModelFactory):
    title = Faker("ipv4")
    description = Faker("sentence")
    analysis = SubFactory("tests.factories.analysis.AnalysisFactory")
    input_specification = SubFactory(
        "tests.factories.input.input_specification.InputSpecificationFactory"
    )
    output_specification = SubFactory(
        "tests.factories.output.output_specification.OutputSpecificationFactory"
    )

    class Meta:
        model = "django_analyses.AnalysisVersion"
