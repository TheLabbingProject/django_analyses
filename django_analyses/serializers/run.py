from django.contrib.auth import get_user_model
from django_analyses.models.run import Run
from django_analyses.serializers.analysis_version import (
    AnalysisVersionSerializer,
)
from rest_auth.serializers import UserDetailsSerializer
from rest_framework import serializers


User = get_user_model()


class MiniUserSerializer(UserDetailsSerializer):
    """
    Minified serializer class for the :class:`User` model.
    """

    class Meta(UserDetailsSerializer.Meta):
        fields = (
            "id",
            "username",
            "first_name",
            "last_name",
            "email",
        )


class RunSerializer(serializers.HyperlinkedModelSerializer):
    user = MiniUserSerializer()
    analysis_version = AnalysisVersionSerializer()

    class Meta:
        model = Run
        fields = (
            "id",
            "user",
            "analysis_version",
            "created",
            "modified",
        )
