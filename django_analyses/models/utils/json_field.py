from django.db.models import JSONField


class DefaultJSONField(JSONField):
    def formfield(self, **kwargs):
        from django_analyses.forms.json_field import DefaultJSONFormField

        return super().formfield(
            **{"form_class": DefaultJSONFormField, **kwargs}
        )
