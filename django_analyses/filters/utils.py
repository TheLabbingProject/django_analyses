"""
Utilities for the :mod:`~django_analyses.filters` module.
"""
from django_filters import rest_framework as filters


class NumberInFilter(filters.BaseInFilter, filters.NumberFilter):
    pass


DEFAULT_LOOKUP_CHOICES = (
    ("contains", "Contains (case-sensitive)"),
    ("icontains", "Contains (case-insensitive)"),
    ("exact", "Exact"),
)
