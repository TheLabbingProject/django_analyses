"""
Registers various :mod:`~django.contrib.admin` models to generate the app's
admin site interface.

References
----------
* `The Django admin site`_

.. _The Django admin site:
   https://docs.djangoproject.com/en/3.0/ref/contrib/admin/
"""
import datetime
import json
from typing import Any, Union

from django.contrib import admin
from django.db.models import JSONField
from django.forms import widgets
from django.urls import reverse
from django.utils.safestring import mark_safe
from django_admin_inline_paginator.admin import TabularInlinePaginated
from nonrelated_inlines.admin import NonrelatedStackedInline

from django_analyses.models.analysis import Analysis
from django_analyses.models.analysis_version import AnalysisVersion
from django_analyses.models.input.definitions.input_definition import (
    InputDefinition,
)
from django_analyses.models.input.input import Input
from django_analyses.models.input.input_specification import InputSpecification
from django_analyses.models.output.definitions.output_definition import (
    OutputDefinition,
)
from django_analyses.models.output.output import Output
from django_analyses.models.output.output_specification import (
    OutputSpecification,
)
from django_analyses.models.output.types.output_types import OutputTypes
from django_analyses.models.pipeline.node import Node
from django_analyses.models.pipeline.pipe import Pipe
from django_analyses.models.pipeline.pipeline import Pipeline
from django_analyses.models.run import Run
from django_analyses.utils.html import Html

DOWNLOAD_BUTTON = '<span><a href={url} type="button" class="button" id="run-{run_id}-download-button">{text}</a></span>'  # noqa: E501


def custom_titled_filter(title: str):
    """
    Copied from SO:
    https://stackoverflow.com/a/21223908/4416932
    """

    class Wrapper(admin.FieldListFilter):
        def __new__(cls, *args, **kwargs):
            instance = admin.FieldListFilter.create(*args, **kwargs)
            instance.title = title
            return instance

    return Wrapper


class PrettyJSONWidget(widgets.Textarea):
    def format_value(self, value):
        try:
            value = json.dumps(json.loads(value), indent=2, sort_keys=True)
            # these lines will try to adjust size of TextArea to fit to content
            row_lengths = [len(r) for r in value.split("\n")]
            self.attrs["rows"] = min(max(len(row_lengths) + 2, 10), 30)
            self.attrs["cols"] = min(max(max(row_lengths) + 2, 40), 120)
            return value
        except Exception:
            return super().format_value(value)


class AnalysisVersionInline(admin.TabularInline):
    model = AnalysisVersion
    fields = (
        "id_link",
        "title",
        "description",
        "input_specification_link",
        "output_specification_link",
        "run_count",
    )
    readonly_fields = (
        "id_link",
        "title",
        "description",
        "input_specification_link",
        "output_specification_link",
        "run_count",
    )
    extra = 0
    can_delete = False

    class Media:
        css = {"all": ("django_analyses/css/hide_admin_original.css",)}

    def has_add_permission(self, request, obj):
        return False

    def id_link(self, instance: AnalysisVersion) -> str:
        model_name = instance.__class__.__name__
        pk = instance.id
        return Html.admin_link(model_name, pk)

    def input_specification_link(self, instance: AnalysisVersion) -> str:
        model_name = instance.input_specification.__class__.__name__
        pk = instance.input_specification.id
        return Html.admin_link(model_name, pk)

    def output_specification_link(self, instance: AnalysisVersion) -> str:
        model_name = instance.output_specification.__class__.__name__
        pk = instance.output_specification.id
        return Html.admin_link(model_name, pk)

    def run_count(self, instance: AnalysisVersion) -> int:
        return Run.objects.filter(analysis_version=instance).count()

    id_link.short_description = "ID"
    input_specification_link.short_description = "Input Specification"
    output_specification_link.short_description = "Output Specification"


class NodeInline(admin.TabularInline):
    model = Node
    fields = (
        "id_link",
        "configuration",
    )
    readonly_fields = (
        "id_link",
        "configuration",
    )
    extra = 0
    can_delete = False

    class Media:
        css = {"all": ("django_analyses/css/hide_admin_original.css",)}

    def has_add_permission(self, request, obj):
        return False

    def id_link(self, instance: Node) -> str:
        model_name = instance.__class__.__name__
        pk = instance.id
        return Html.admin_link(model_name, pk)

    id_link.short_description = "ID"


class AnalysisVersionInputSpecInline(admin.TabularInline):
    model = AnalysisVersion
    fields = (
        "version_link",
        "description",
        "output_specification_link",
    )
    readonly_fields = (
        "version_link",
        "description",
        "output_specification_link",
    )
    extra = 0
    can_delete = False

    class Media:
        css = {"all": ("django_analyses/css/hide_admin_original.css",)}

    def version_link(self, instance: AnalysisVersion) -> str:
        pk = instance.id
        text = instance.title
        return Html.admin_link("AnalysisVersion", pk, text)

    version_link.short_description = "Title"

    def output_specification_link(self, instance: AnalysisVersion) -> str:
        model_name = instance.output_specification.__class__.__name__
        pk = instance.output_specification.id
        return Html.admin_link(model_name, pk)

    output_specification_link.short_description = "Output Specification"

    def has_add_permission(self, request, obj):
        return False


class AnalysisVersionOutputSpecInline(admin.TabularInline):
    model = AnalysisVersion
    fields = (
        "version_link",
        "description",
        "input_specification_link",
    )
    readonly_fields = (
        "version_link",
        "description",
        "input_specification_link",
    )
    extra = 0
    can_delete = False

    class Media:
        css = {"all": ("django_analyses/css/hide_admin_original.css",)}

    def version_link(self, instance: AnalysisVersion) -> str:
        pk = instance.id
        text = instance.title
        return Html.admin_link("AnalysisVersion", pk, text)

    version_link.short_description = "Title"

    def input_specification_link(self, instance: AnalysisVersion) -> str:
        model_name = instance.input_specification.__class__.__name__
        pk = instance.input_specification.id
        return Html.admin_link(model_name, pk)

    input_specification_link.short_description = "Input Specification"

    def has_add_permission(self, request, obj):
        return False


@admin.register(Analysis)
class AnalysisAdmin(admin.ModelAdmin):
    fields = "title", "description", "category", "created", "modified"
    list_display = (
        "title",
        "description",
        "run_count",
    )
    readonly_fields = "run_count", "created", "modified"
    inlines = [AnalysisVersionInline]

    def run_count(self, instance: Analysis) -> int:
        return Run.objects.filter(analysis_version__analysis=instance).count()


class NodeRunInline(TabularInlinePaginated, NonrelatedStackedInline):
    model = Run
    fields = (
        "run_link",
        "start_time",
        "end_time",
        "duration",
        "_status",
        "download",
    )
    readonly_fields = (
        "run_link",
        "start_time",
        "end_time",
        "duration",
        "_status",
        "download",
    )
    can_delete = False
    extra = 0
    per_page = 20
    _form_queryset = None

    class Media:
        css = {"all": ("django_mri/css/hide_admin_original.css",)}

    def has_add_permission(self, request, instance: Run):
        return False

    def get_form_queryset(self, instance: Run):
        if self._form_queryset is None:
            self._form_queryset = instance.run_set.all()
        return self._form_queryset

    def run_link(self, instance: Run) -> str:
        model_name = instance.__class__.__name__
        pk = instance.id
        return Html.admin_link(model_name, pk)

    def _status(self, instance: Run) -> bool:
        if instance.status == "SUCCESS":
            return True
        elif instance.status == "FAILURE":
            return False

    def download(self, instance: Run) -> str:
        if instance.status == "SUCCESS" and instance.path.exists():
            url = reverse("analyses:run_to_zip", args=(instance.id,))
            button = DOWNLOAD_BUTTON.format(
                url=url, run_id=instance.id, text="ZIP"
            )
            return mark_safe(button)

    run_link.short_description = "Run"
    _status.boolean = True


@admin.register(Node)
class NodeAdmin(admin.ModelAdmin):
    fields = "analysis_version_link", "configuration"
    readonly_fields = ("analysis_version_link",)
    list_display = (
        "id",
        "analysis_version_link",
        "configuration",
    )
    list_filter = ("analysis_version__analysis",)
    search_fields = (
        "id",
        "analysis_version__analysis__title",
        "analysis_version__title",
        "configuration__has_key",
    )
    formfield_overrides = {JSONField: {"widget": PrettyJSONWidget}}
    inlines = (NodeRunInline,)

    def analysis_version_link(self, instance: Node) -> str:
        model_name = instance.analysis_version.__class__.__name__
        pk = instance.analysis_version.id
        text = str(instance.analysis_version)
        return Html.admin_link(model_name, pk, text)

    analysis_version_link.short_description = "Analysis Version"


@admin.register(Pipe)
class PipeAdmin(admin.ModelAdmin):
    fieldsets = (
        (
            None,
            {
                "fields": [
                    "pipeline",
                    "source_analysis_version",
                    "source_port_key",
                    "source_node",
                    "source_configuration",
                    "destination_analysis_version",
                    "destination_port_key",
                    "destination_node",
                    "destination_configuration",
                ]
            },
        ),
        (
            "Configuration",
            {
                "fields": [
                    "index",
                    "source_run_index",
                    "destination_run_index",
                ]
            },
        ),
    )
    readonly_fields = (
        "id_link",
        "pipeline_link",
        "source_analysis_version",
        "source_port_key",
        "source_node",
        "source_configuration",
        "destination_analysis_version",
        "destination_port_key",
        "destination_node",
        "destination_configuration",
    )
    list_filter = (
        "pipeline",
        (
            "source__analysis_version__analysis",
            custom_titled_filter("source analysis"),
        ),
        (
            "destination__analysis_version__analysis",
            custom_titled_filter("destination analysis"),
        ),
    )
    list_display = (
        "id_link",
        "pipeline_link",
        "source_analysis_version",
        "source_node",
        "source_port_key",
        "destination_analysis_version",
        "destination_node",
        "destination_port_key",
    )
    search_fields = (
        "id",
        "pipeline__title",
        "source__analysis_version__analysis__title",
        "source__analysis_version__title",
        "destination__analysis_version__analysis__title",
        "destination__analysis_version__title",
    )
    formfield_overrides = {JSONField: {"widget": PrettyJSONWidget}}

    def id_link(self, instance: Pipe) -> str:
        return Html.admin_link("Pipe", instance.id)

    def pipeline_link(self, instance: Pipe) -> str:
        model_name = instance.pipeline.__class__.__name__
        pk = instance.pipeline.id
        text = instance.pipeline.title
        return Html.admin_link(model_name, pk, text)

    def source_node(self, instance: Pipe) -> str:
        model_name = instance.source.__class__.__name__
        pk = instance.source.id
        return Html.admin_link(model_name, pk)

    def source_configuration(self, instance: Pipe) -> str:
        return instance.source.configuration

    def destination_node(self, instance: Pipe) -> str:
        model_name = instance.destination.__class__.__name__
        pk = instance.destination.id
        return Html.admin_link(model_name, pk)

    def destination_configuration(self, instance: Pipe) -> str:
        return instance.destination.configuration

    def source_analysis_version(self, instance: Pipe) -> str:
        version = instance.source.analysis_version
        model_name = version.__class__.__name__
        pk = version.id
        text = str(version)
        return Html.admin_link(model_name, pk, text)

    def source_port_key(self, instance: Pipe) -> str:
        definition = instance.source_port
        pk = definition.id
        text = definition.key
        return Html.admin_link("OutputDefinition", pk, text)

    def destination_analysis_version(self, instance: Pipe) -> str:
        version = instance.destination.analysis_version
        model_name = version.__class__.__name__
        pk = version.id
        text = str(version)
        return Html.admin_link(model_name, pk, text)

    def destination_port_key(self, instance: Pipe) -> str:
        definition = instance.destination_port
        pk = definition.id
        text = definition.key
        return Html.admin_link("InputDefinition", pk, text)

    id_link.short_description = "ID"
    pipeline_link.short_description = "Pipeline"
    source_port_key.short_description = "Port"
    destination_port_key.short_description = "Port"


class PipeInLine(admin.TabularInline):
    model = Pipe
    fields = (
        "id_link",
        "source_analysis_version",
        "source_node",
        "source_port_key",
        "destination_analysis_version",
        "destination_port_key",
        "destination_node",
    )
    readonly_fields = (
        "id_link",
        "source_analysis_version",
        "source_node",
        "source_port_key",
        "destination_analysis_version",
        "destination_port_key",
        "destination_node",
    )
    extra = 0
    can_delete = False

    class Media:
        css = {"all": ("django_analyses/css/hide_admin_original.css",)}

    def has_add_permission(self, request, obj):
        return False

    def id_link(self, instance: Input) -> str:
        return Html.admin_link("Pipe", instance.id)

    def source_node(self, instance: Pipe) -> str:
        model_name = instance.source.__class__.__name__
        pk = instance.source.id
        return Html.admin_link(model_name, pk)

    def destination_node(self, instance: Pipe) -> str:
        model_name = instance.destination.__class__.__name__
        pk = instance.destination.id
        return Html.admin_link(model_name, pk)

    def source_analysis_version(self, instance: Pipe) -> str:
        version = instance.source.analysis_version
        model_name = version.__class__.__name__
        pk = version.id
        text = str(version)
        return Html.admin_link(model_name, pk, text)

    def source_port_key(self, instance: Pipe) -> str:
        definition = instance.source_port
        pk = definition.id
        text = definition.key
        return Html.admin_link("OutputDefinition", pk, text)

    def destination_analysis_version(self, instance: Pipe) -> str:
        version = instance.destination.analysis_version
        model_name = version.__class__.__name__
        pk = version.id
        text = str(version)
        return Html.admin_link(model_name, pk, text)

    def destination_port_key(self, instance: Pipe) -> str:
        definition = instance.destination_port
        pk = definition.id
        text = definition.key
        return Html.admin_link("InputDefinition", pk, text)

    id_link.short_description = "ID"
    source_analysis_version.short_description = "Source"
    source_port_key.short_description = "Port"
    destination_analysis_version.short_description = "Destination"
    destination_port_key.short_description = "Port"

    id_link.short_description = "ID"


@admin.register(Pipeline)
class PipelineAdmin(admin.ModelAdmin):
    fields = "title", "description", "created", "modified"
    readonly_fields = "created", "modified", "node_count", "pipe_count"
    list_display = (
        "id",
        "title",
        "description",
        "node_count",
        "pipe_count",
    )
    search_fields = (
        "id",
        "title",
        "description",
    )
    inlines = (PipeInLine,)

    def node_count(self, instance: Pipeline) -> int:
        return instance.node_set.count()

    def pipe_count(self, instance: Pipeline) -> int:
        return instance.pipe_set.count()

    node_count.short_description = "# Nodes"
    pipe_count.short_description = "# Pipes"


class InputInline(admin.TabularInline):
    model = Input
    readonly_fields = "id_link", "definition_link", "input_type", "value"
    extra = 0
    can_delete = False

    def get_queryset(self, request):
        return super().get_queryset(request).select_subclasses()

    def has_add_permission(self, request, obj):
        return False

    def definition_link(self, instance: Input) -> str:
        pk = instance.definition.id
        text = instance.definition.key
        return Html.admin_link("InputDefinition", pk, text)

    def id_link(self, instance: Input) -> str:
        return Html.admin_link("Input", instance.id)

    def input_type(self, instance: Input) -> str:
        return instance.definition.get_type().value

    definition_link.short_description = "Key"
    id_link.short_description = "ID"
    input_type.short_description = "Type"


class OutputInline(admin.TabularInline):
    model = Output
    readonly_fields = (
        "id_link",
        "definition_link",
        "output_type",
        "value",
        "download",
    )
    extra = 0
    can_delete = False

    def get_queryset(self, request):
        return super().get_queryset(request).select_subclasses()

    def has_add_permission(self, request, obj):
        return False

    def id_link(self, instance: Output) -> str:
        return Html.admin_link("Output", instance.id)

    def definition_link(self, instance: Output) -> str:
        pk = instance.definition.id
        text = instance.definition.key
        return Html.admin_link("OutputDefinition", pk, text)

    def output_type(self, instance: Output) -> str:
        return instance.definition.get_type().value

    def download(self, instance: Output) -> str:
        instance = Output.objects.get_subclass(id=instance.id)
        is_file = instance.get_type() == OutputTypes.FIL
        is_file_list = (
            instance.get_type() == OutputTypes.LST
            and instance.definition.element_type == "FIL"
        )
        if is_file or is_file_list:
            url = reverse("analyses:file_output_download", args=(instance.id,))
            button = DOWNLOAD_BUTTON.format(
                url=url, run_id=instance.id, text="Download"
            )
            return mark_safe(button)
        return ""

    definition_link.short_description = "Definition"
    id_link.short_description = "ID"
    output_type.short_description = "Type"


@admin.register(AnalysisVersion)
class AnalysisVersionAdmin(admin.ModelAdmin):
    fieldsets = (
        (
            None,
            {
                "fields": (
                    "analysis",
                    "title",
                    "description",
                    "input_specification_link",
                    "output_specification_link",
                )
            },
        ),
        (
            "Advanced Options",
            {
                "fields": (
                    "max_parallel",
                    "run_method_key",
                    "nested_results_attribute",
                    "fixed_run_method_kwargs",
                ),
            },
        ),
    )
    readonly_fields = (
        "analysis",
        "id_link",
        "input_specification_link",
        "output_specification_link",
        "run_count",
    )
    list_display = (
        "id_link",
        "analysis_link",
        "title",
        "description",
        "input_specification_link",
        "output_specification_link",
        "run_count",
        "created",
        "modified",
    )
    inlines = (NodeInline,)

    def name(self, instance) -> str:
        return str(instance)

    def analysis_link(self, instance: InputSpecification) -> str:
        model_name = instance.analysis.__class__.__name__
        pk = instance.analysis.id
        text = instance.analysis.title
        return Html.admin_link(model_name, pk, text)

    def input_specification_link(self, instance: AnalysisVersion) -> str:
        model_name = instance.input_specification.__class__.__name__
        pk = instance.input_specification.id
        return Html.admin_link(model_name, pk)

    def output_specification_link(self, instance: AnalysisVersion) -> str:
        model_name = instance.output_specification.__class__.__name__
        pk = instance.output_specification.id
        return Html.admin_link(model_name, pk)

    def id_link(self, instance: AnalysisVersion) -> str:
        model_name = instance.__class__.__name__
        pk = instance.id
        return Html.admin_link(model_name, pk)

    def run_count(self, instance: AnalysisVersion) -> int:
        return Run.objects.filter(analysis_version=instance).count()

    analysis_link.short_description = "Analysis"
    input_specification_link.short_description = "Input Specification"
    output_specification_link.short_description = "Output Specification"
    id_link.short_description = "ID"


@admin.register(Run)
class RunAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "analysis_version_link",
        "user_link",
        "start_time",
        "end_time",
        "duration",
        "_status",
        "download",
    )
    inlines = (InputInline, OutputInline)
    fieldsets = (
        (None, {"fields": ("analysis_version_link", "user", "node")}),
        (
            "Execution",
            {
                "fields": (
                    "start_time",
                    "end_time",
                    ("status", "duration"),
                    "traceback",
                    "path",
                    "download",
                ),
            },
        ),
    )
    readonly_fields = (
        "analysis_version",
        "analysis_version_link",
        "user_link",
        "node",
        "start_time",
        "end_time",
        "duration",
        "status",
        "path",
        "download",
    )
    list_filter = (
        "status",
        "start_time",
        "analysis_version__analysis",
        "user",
    )
    search_fields = (
        "id",
        "analysis_version__title",
        "analysis_version__analysis__title",
    )

    class Media:
        css = {"all": ("django_analyses/css/hide_admin_original.css",)}
        # js = ("django_analyses/js/",)

    def download(self, instance: Run) -> str:
        if instance.status == "SUCCESS" and instance.path.exists():
            url = reverse("analyses:run_to_zip", args=(instance.id,))
            button = DOWNLOAD_BUTTON.format(
                url=url, run_id=instance.id, text="ZIP"
            )
            return mark_safe(button)

    def duration(self, instance: Run) -> datetime.timedelta:
        return instance.duration

    def analysis_version_link(self, instance: Run) -> str:
        model_name = instance.analysis_version.__class__.__name__
        pk = instance.analysis_version.id
        text = str(instance.analysis_version)
        return Html.admin_link(model_name, pk, text)

    def node(self, instance: Run) -> str:
        nodes = Node.objects.filter(analysis_version=instance.analysis_version)
        links = []
        for node in nodes:
            if node.check_run_configuration_sameness(instance):
                model_name = node.__class__.__name__
                pk = node.id
                links.append(Html.admin_link(model_name, pk))
        if links:
            return mark_safe(", ".join(links))

    def user_link(self, instance: Run) -> str:
        if instance.user:
            model_name = instance.user.__class__.__name__
            pk = instance.user.id
            text = instance.user.username
            return Html.admin_link(model_name, pk, text)

    def _status(self, instance: Run) -> Union[str, bool]:
        if instance.status == "SUCCESS":
            return True
        elif instance.status == "FAILURE":
            return False
        else:
            return None

    _status.boolean = True
    analysis_version_link.short_description = "Analysis Version"
    user_link.short_description = "User"


@admin.register(Input)
class InputAdmin(admin.ModelAdmin):
    fields = (
        "analysis_version_link",
        "definition_link",
        "run_link",
        "input_type",
        "_value",
    )
    list_display = (
        "analysis_version_link",
        "run_link",
        "definition_link",
        "input_type",
        "value",
    )
    list_filter = ("run__analysis_version",)
    list_display_links = None
    search_fields = ("run__id",)
    readonly_fields = (
        "analysis_version_link",
        "definition_link",
        "run_link",
        "input_type",
        "_value",
    )

    def get_queryset(self, request):
        return super().get_queryset(request).select_subclasses()

    def analysis_version(self, instance) -> str:
        return str(instance.run.analysis_version)

    def run_link(self, instance: Input) -> str:
        model_name = instance.run.__class__.__name__
        pk = instance.run.id
        return Html.admin_link(model_name, pk)

    def analysis_version_link(self, instance: Input) -> str:
        analysis_version = instance.run.analysis_version
        model_name = analysis_version.__class__.__name__
        pk = analysis_version.id
        text = str(analysis_version)
        return Html.admin_link(model_name, pk, text)

    def definition_link(self, instance: Input) -> str:
        pk = instance.definition.id
        text = instance.definition.key
        return Html.admin_link("InputDefinition", pk, text)

    def input_type(self, instance: Input) -> str:
        return instance.definition.get_type().value

    def _value(self, instance: Input) -> Any:
        instance = Input.objects.get_subclass(id=instance.id)
        return instance.value

    run_link.short_description = "Run"
    analysis_version_link.short_description = "Analysis Version"
    definition_link.short_description = "Definition"
    input_type.short_description = "Type"
    _value.short_description = "Value"


@admin.register(Output)
class OutputAdmin(admin.ModelAdmin):
    fields = (
        "analysis_version_link",
        "run_link",
        "definition_link",
        "output_type",
        "_value",
        "download",
    )
    list_display = (
        "analysis_version_link",
        "run_link",
        "definition_link",
        "output_type",
        "value",
        "download",
    )
    list_filter = ("run__analysis_version",)
    list_display_links = None
    search_fields = ("run__id",)
    readonly_fields = (
        "analysis_version_link",
        "definition_link",
        "run_link",
        "output_type",
        "_value",
        "download",
    )

    class Media:
        js = ("//cdnjs.cloudflare.com/ajax/libs/jquery/3.3.1/jquery.min.js",)

    def change_view(self, *args, **kwargs):
        instance = Output.objects.get_subclass(id=kwargs["object_id"])
        kwargs["extra_context"] = kwargs.get("extra_context", {})
        kwargs["extra_context"]["output_type"] = instance.get_type().value
        return super().change_view(*args, **kwargs)

    def get_queryset(self, request):
        return super().get_queryset(request).select_subclasses()

    def analysis_version(self, instance: Output) -> str:
        return str(instance.run.analysis_version)

    def download(self, instance: Output) -> str:
        instance = Output.objects.get_subclass(id=instance.id)
        if instance.get_type() == OutputTypes.FIL:
            url = reverse("analyses:file_output_download", args=(instance.id,))
            button = DOWNLOAD_BUTTON.format(
                url=url, run_id=instance.id, text="Download"
            )
            return mark_safe(button)

    def run_link(self, instance: Output) -> str:
        model_name = instance.run.__class__.__name__
        pk = instance.run.id
        return Html.admin_link(model_name, pk)

    def analysis_version_link(self, instance: Output) -> str:
        analysis_version = instance.run.analysis_version
        model_name = analysis_version.__class__.__name__
        pk = analysis_version.id
        text = str(analysis_version)
        return Html.admin_link(model_name, pk, text)

    def definition_link(self, instance: Output) -> str:
        pk = instance.definition.id
        text = instance.definition.key
        return Html.admin_link("OutputDefinition", pk, text)

    def output_type(self, instance: Output) -> str:
        return instance.definition.get_type().value

    def _value(self, instance: Output) -> Any:
        instance = Output.objects.get_subclass(id=instance.id)
        return instance.value

    run_link.short_description = "Run"
    analysis_version_link.short_description = "Analysis Version"
    definition_link.short_description = "Definition"
    output_type.short_description = "Type"
    _value.short_description = "Value"


@admin.register(InputDefinition)
class InputDefinitionAdmin(admin.ModelAdmin):
    fieldsets = (
        (
            None,
            {
                "fields": [
                    "key",
                    "description",
                    "required",
                    "default",
                    "min_value",
                    "max_value",
                    "choices",
                ]
            },
        ),
        (
            "Advanced Integration",
            {
                "classes": ("collapse",),
                "fields": [
                    "is_configuration",
                    "run_method_input",
                    "db_value_preprocessing",
                    "value_attribute",
                ],
            },
        ),
    )
    list_display = (
        "key",
        "description",
        "min_value",
        "max_value",
        "default",
        "choices",
        "required",
        "is_configuration",
    )
    list_filter = (
        "specification_set__analysis__title",
        "specification_set__id",
    )
    readonly_fields = (
        "default",
        "choices",
        "min_value",
        "max_value",
    )

    class Media:
        css = {"all": ("django_analyses/css/hide_admin_original.css",)}

    def get_queryset(self, request):
        return (
            super(InputDefinitionAdmin, self)
            .get_queryset(request)
            .select_subclasses()
        )

    def choices(self, instance) -> list:
        return getattr(instance, "choices", "")

    def min_value(self, instance):
        return getattr(instance, "min_value", "")

    def max_value(self, instance):
        return getattr(instance, "max_value", "")


@admin.register(OutputDefinition)
class OutputDefinitionAdmin(admin.ModelAdmin):
    list_display = ("key", "description", "analysis")
    list_filter = (
        "specification_set__analysis__title",
        "specification_set__id",
    )

    def analysis(self, instance):
        return instance.specification_set.first().analysis


class InputDefinitionsInline(admin.TabularInline):
    fields = (
        "id_link",
        "key",
        "input_type",
        "description",
        "required",
        "default",
    )
    readonly_fields = (
        "id_link",
        "key",
        "input_type",
        "description",
        "required",
        "default",
    )
    model = InputDefinition.specification_set.through
    verbose_name_plural = "Input Definitions"
    extra = 0
    can_delete = False

    def has_add_permission(self, request, obj):
        return False

    def id_link(self, instance: InputDefinition) -> str:
        model_name = instance.inputdefinition.__class__.__name__
        pk = instance.inputdefinition.id
        return Html.admin_link(model_name, pk)

    def input_type(self, instance: InputDefinition) -> str:
        pk = instance.inputdefinition.id
        subinstance = InputDefinition.objects.get_subclass(id=pk)
        model_name = subinstance.__class__.__name__
        return model_name.replace("InputDefinition", "")

    def key(self, instance: InputDefinition) -> str:
        return instance.inputdefinition.key

    def description(self, instance: InputDefinition) -> str:
        return instance.inputdefinition.description

    def required(self, instance: InputDefinition) -> bool:
        return instance.inputdefinition.required

    def default(self, instance: InputDefinition) -> str:
        default = instance.inputdefinition.default
        return "" if default is None else default

    id_link.short_description = "ID"
    input_type.short_description = "Type"
    required.boolean = True


@admin.register(InputSpecification)
class InputSpecificationAdmin(admin.ModelAdmin):
    fields = ("analysis",)
    list_display = (
        "id",
        "analysis_link",
        "analysis_versions",
        "input_definitions_count",
    )
    list_filter = ("analysis",)
    readonly_fields = (
        "analysis",
        "analysis_link",
        "analysis_versions",
        "input_definitions_count",
    )
    inlines = [AnalysisVersionInputSpecInline, InputDefinitionsInline]

    class Media:
        css = {"all": ("django_analyses/css/hide_admin_original.css",)}

    def analysis_link(self, instance: InputSpecification) -> str:
        model_name = instance.analysis.__class__.__name__
        pk = instance.analysis.id
        text = instance.analysis.title
        return Html.admin_link(model_name, pk, text)

    analysis_link.short_description = "Analysis"

    def analysis_versions(self, instance: InputSpecification) -> str:
        links = []
        for analysis_version in instance.analysis_version_set.all():
            model_name = analysis_version.__class__.__name__
            pk = analysis_version.id
            text = analysis_version.title
            link = Html.admin_link(model_name, pk, text)
            links.append(link)
        return mark_safe(", ".join(links))

    analysis_versions.short_description = "Analysis Versions"

    def input_definitions_count(self, instance: InputSpecification) -> int:
        return instance.input_definitions.count()

    input_definitions_count.short_description = "# of Input Definitions"


class OutputDefinitionsInline(admin.TabularInline):
    fields = (
        "id_link",
        "key",
        "output_type",
        "description",
    )
    readonly_fields = (
        "id_link",
        "key",
        "output_type",
        "description",
    )
    model = OutputDefinition.specification_set.through
    verbose_name_plural = "Output Definitions"
    extra = 0
    can_delete = False

    def has_add_permission(self, request, obj):
        return False

    def id_link(self, instance: OutputDefinition) -> str:
        model_name = instance.outputdefinition.__class__.__name__
        pk = instance.outputdefinition.id
        return Html.admin_link(model_name, pk)

    def output_type(self, instance: OutputDefinition) -> str:
        pk = instance.outputdefinition.id
        subinstance = OutputDefinition.objects.get_subclass(id=pk)
        model_name = subinstance.__class__.__name__
        return model_name.replace("OutputDefinition", "")

    def key(self, instance: OutputDefinition) -> str:
        return instance.outputdefinition.key

    def description(self, instance: OutputDefinition) -> str:
        return instance.outputdefinition.description

    id_link.short_description = "ID"
    output_type.short_description = "Type"


@admin.register(OutputSpecification)
class OutputSpecificationAdmin(admin.ModelAdmin):
    fields = ("analysis",)
    list_display = (
        "id",
        "analysis_link",
        "analysis_versions",
        "output_definitions_count",
    )
    list_filter = ("analysis",)
    readonly_fields = (
        "analysis",
        "analysis_link",
        "analysis_versions",
        "output_definitions_count",
    )
    inlines = [AnalysisVersionOutputSpecInline, OutputDefinitionsInline]

    class Media:
        css = {"all": ("django_analyses/css/hide_admin_original.css",)}

    def analysis_link(self, instance: OutputSpecification) -> str:
        model_name = instance.analysis.__class__.__name__
        pk = instance.analysis.id
        text = instance.analysis.title
        return Html.admin_link(model_name, pk, text)

    analysis_link.short_description = "Analysis"

    def analysis_versions(self, instance: OutputSpecification) -> str:
        links = []
        for analysis_version in instance.analysis_version_set.all():
            model_name = analysis_version.__class__.__name__
            pk = analysis_version.id
            text = analysis_version.title
            link = Html.admin_link(model_name, pk, text)
            links.append(link)
        return mark_safe(", ".join(links))

    analysis_versions.short_description = "Analysis Versions"

    def output_definitions_count(self, instance: OutputSpecification) -> int:
        return instance.output_definitions.count()

    output_definitions_count.short_description = "# of Output Definitions"
