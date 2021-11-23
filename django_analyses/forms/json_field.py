from django.contrib.postgres import forms


class DefaultJSONFormField(forms.JSONField):
    empty_values = [None, "", [], ()]
