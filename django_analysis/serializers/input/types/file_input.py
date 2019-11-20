from django.conf import settings
from django_analysis.models.input.types.file_input import FileInput
from rest_framework import serializers


class FileInputSerializer(serializers.ModelSerializer):
    value = serializers.FilePathField(settings.MEDIA_ROOT)

    class Meta:
        model = FileInput
        fields = "id", "key", "value", "run", "definition"
