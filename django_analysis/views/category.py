from django_analysis.filters.category import CategoryFilter
from django_analysis.models.category import Category
from django_analysis.serializers.category import CategorySerializer
from django_analysis.views.defaults import DefaultsMixin
from django_analysis.views.pagination import StandardResultsSetPagination
from rest_framework import viewsets


class CategoryViewSet(DefaultsMixin, viewsets.ModelViewSet):
    filter_class = CategoryFilter
    pagination_class = StandardResultsSetPagination
    serializer_class = CategorySerializer
    queryset = Category.objects.all()
