from dj_rest_auth.serializers import UserDetailsSerializer
from django.contrib.auth import get_user_model
from rest_framework import serializers

from django_analyses.models.run import Run
from django_analyses.serializers.analysis_version import AnalysisVersionSerializer

User = get_user_model()


class MiniUserSerializer(UserDetailsSerializer):
    """
    Minified serializer class for the :class:`User` model.
    """

    full_name = serializers.SerializerMethodField()

    class Meta(UserDetailsSerializer.Meta):
        fields = (
            "id",
            "username",
            "first_name",
            "last_name",
            "full_name",
            "email",
        )

    def get_full_name(self, instance: User) -> str:
        return instance.profile.get_full_name(include_title=False)


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
            "start_time",
            "end_time",
            "duration",
            "status",
            "traceback",
        )

    def duration(self, instance: Run):
        return self.instance.duration
