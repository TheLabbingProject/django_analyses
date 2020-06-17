"""
Definition of an :class:`~django_analyses.filters.input.input.InputFilter`
for the :class:`~django_analyses.models.input.input.Input` model.
"""

from django_analyses.models.input.input import Input
from django_filters import rest_framework as filters


class InputFilter(filters.FilterSet):
    """
    Provides useful filtering options for the
    :class:`~django_analyses.models.input.input.Input`
    model.

    """

    class Meta:
        model = Input
        fields = ("run",)
