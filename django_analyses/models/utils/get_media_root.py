from django.conf import settings


def get_media_root() -> str:
    return settings.MEDIA_ROOT
