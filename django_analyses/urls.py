from django.urls import include, path
from rest_framework import routers

from django_analyses import views

app_name = "django_analyses"
router = routers.DefaultRouter()
router.register(r"analysis", views.AnalysisViewSet)
router.register(r"analysis_version", views.AnalysisVersionViewSet)
router.register(r"category", views.CategoryViewSet)
router.register(r"input_specification", views.InputSpecificationViewSet)
router.register(r"output_specification", views.OutputSpecificationViewSet)
router.register(r"run", views.RunViewSet)
router.register(r"node", views.NodeViewSet)
router.register(r"pipe", views.PipeViewSet)
router.register(r"pipeline", views.PipelineViewSet)

# In viewsets of base models basename must be provided because of the
# `get_queryset` method override. Since the `queryset` attribute is not
# provided the basename cannot be infered.
router.register(r"input", views.InputViewSet, basename="input")
router.register(
    r"input_definition",
    views.InputDefinitionViewSet,
    basename="inputdefinition",
)
router.register(r"output", views.OutputViewSet, basename="output")
router.register(
    r"output_definition",
    views.OutputDefinitionViewSet,
    basename="outputdefinition",
)


urlpatterns = [
    path("analyses/", include(router.urls)),
    path(
        "analyses/output/html_repr/<int:output_id>/",
        views.OutputViewSet.as_view({"get": "html_repr"}),
        name="output_html_repr",
    ),
    path(
        "analyses/output/html_repr/<int:output_id>/<int:index>/",
        views.OutputViewSet.as_view({"get": "html_repr"}),
        name="output_html_repr",
    ),
    path(
        "analyses/input/html_repr/<int:input_id>/",
        views.InputViewSet.as_view({"get": "html_repr"}),
        name="input_html_repr",
    ),
    path(
        "analyses/input/html_repr/<int:input_id>/<int:index>/",
        views.InputViewSet.as_view({"get": "html_repr"}),
        name="input_html_repr",
    ),
    path(
        "analyses/run/<int:run_id>/to_zip/",
        views.RunViewSet.as_view({"get": "to_zip"}),
        name="run_to_zip",
    ),
    path(
        "analyses/output/<int:output_id>/download/",
        views.OutputViewSet.as_view({"get": "download"}),
        name="file_output_download",
    ),
    path(
        "analyses/input/<int:input_id>/download/",
        views.OutputViewSet.as_view({"get": "download"}),
        name="file_input_download",
    ),
]
