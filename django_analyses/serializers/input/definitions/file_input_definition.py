from django.conf import settings
from django_analyses.models.input.definitions.file_input_definition import \
    FileInputDefinition
from rest_framework import serializers


class FileInputDefinitionSerializer(serializers.ModelSerializer):
    default = serializers.FilePathField(settings.MEDIA_ROOT, required=False)

    class Meta:
        model = FileInputDefinition
        fields = "__all__"
