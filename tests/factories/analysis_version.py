from factory import SubFactory
from factory.django import DjangoModelFactory


class AnalysisVersionFactory(DjangoModelFactory):
    analysis = SubFactory("tests.factories.analysis.AnalysisFactory")
    input_specification = SubFactory(
        "tests.factories.input.input_specification.InputSpecificationFactory"
    )
    output_specification = SubFactory(
        "tests.factories.output.output_specification.OutputSpecificationFactory"
    )

    class Meta:
        model = "django_analyses.AnalysisVersion"
