from django.urls import include, path
from django_analysis import views
from rest_framework import routers

app_name = "django_analysis"
router = routers.DefaultRouter()
router.register(r"analysis", views.AnalysisViewSet)
router.register(r"analysis_version", views.AnalysisVersionViewSet)
router.register(r"input_specification", views.InputSpecificationViewSet)
router.register(r"output_specification", views.OutputSpecificationViewSet)
router.register(r"run", views.RunViewSet)

urlpatterns = [path("analysis/", include(router.urls))]

