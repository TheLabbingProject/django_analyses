from django.conf import settings
from django_analyses.models.input.types.directory_input import DirectoryInput
from rest_framework import serializers


class DirectoryInputSerializer(serializers.ModelSerializer):
    value = serializers.FilePathField(
        settings.MEDIA_ROOT, allow_folders=True, allow_files=False,
    )

    class Meta:
        model = DirectoryInput
        fields = "id", "key", "value", "run", "definition"
