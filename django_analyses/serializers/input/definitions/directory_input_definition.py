from django.conf import settings
from django_analyses.models.input.definitions import DirectoryInputDefinition
from rest_framework import serializers


class DirectoryInputDefinitionSerializer(serializers.ModelSerializer):
    default = serializers.FilePathField(settings.MEDIA_ROOT, required=False)

    class Meta:
        model = DirectoryInputDefinition
        fields = "__all__"
