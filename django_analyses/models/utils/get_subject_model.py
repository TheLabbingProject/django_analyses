from django.apps import apps
from django.conf import settings
from django.db.models import Model

SUBJECT_MODEL = "research.Subject"


def get_subject_model() -> Model:
    model_identifier = getattr(settings, "SUBJECT_MODEL", SUBJECT_MODEL)
    app_label, model_name = model_identifier.split(".")
    try:
        return apps.get_model(app_label=app_label, model_name=model_name)
    except LookupError:
        pass
