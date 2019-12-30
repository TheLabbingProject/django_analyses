from factory.django import DjangoModelFactory


class FileInputDefinitionFactory(DjangoModelFactory):
    class Meta:
        model = "django_analyses.FileInputDefinition"
