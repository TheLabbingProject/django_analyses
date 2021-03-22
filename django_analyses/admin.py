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
from typing import Union

from django.contrib import admin
from django.urls import reverse
from django.utils.safestring import mark_safe

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
from django_analyses.models.run import Run
from django_analyses.utils.html import Html


class AnalysisVersionInline(admin.TabularInline):
    model = AnalysisVersion
    fields = (
        "version_link",
        "description",
        "input_specification_link",
        "output_specification_link",
        "run_count",
    )
    readonly_fields = (
        "version_link",
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

    def version_link(self, instance: AnalysisVersion) -> str:
        pk = instance.id
        text = instance.title
        return Html.admin_link("AnalysisVersion", pk, text)

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

    input_specification_link.short_description = "Input Specification"
    output_specification_link.short_description = "Output Specification"
    version_link.short_description = "Title"


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
    list_display = "title", "description", "run_count", "created", "modified"
    readonly_fields = ("run_count", "created", "modified")
    inlines = [AnalysisVersionInline]

    def run_count(self, instance: Analysis) -> int:
        return Run.objects.filter(analysis_version__analysis=instance).count()


class InputInline(admin.TabularInline):
    model = Input
    readonly_fields = ("definition_link", "input_type", "value")
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

    def input_type(self, instance: Input) -> str:
        return instance.definition.get_type().value

    definition_link.short_description = "Key"
    input_type.short_description = "Type"


class OutputInline(admin.TabularInline):
    model = Output
    readonly_fields = ("definition_link", "output_type", "value_repr")
    extra = 0
    can_delete = False

    def get_queryset(self, request):
        return super().get_queryset(request).select_subclasses()

    def has_add_permission(self, request, obj):
        return False

    def definition_link(self, instance: Output) -> str:
        pk = instance.definition.id
        text = instance.definition.key
        return Html.admin_link("OutputDefinition", pk, text)

    def output_type(self, instance: Output) -> str:
        return instance.definition.get_type().value

    def value_repr(self, instance: Output) -> str:
        url = reverse("analyses:output_html_repr", args=(instance.id,))
        html = f'<div class="links"><a class="openpop" href={url}>{instance.value}</a></div>'
        return mark_safe(html)

    definition_link.short_description = "Key"
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
                    "max_parallel",
                )
            },
        ),
        (
            "Advanced Options",
            {
                "classes": ("collapse",),
                "fields": (
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
    )
    inlines = (InputInline, OutputInline)
    fieldsets = (
        (None, {"fields": ("analysis_version", "user")}),
        (
            "Execution",
            {
                "fields": (
                    "start_time",
                    "end_time",
                    ("status", "duration"),
                    "traceback",
                    "task_result_",
                ),
            },
        ),
    )
    readonly_fields = (
        "analysis_version",
        "analysis_version_link",
        "user_link",
        "start_time",
        "end_time",
        "duration",
        "status",
        "task_result_",
    )
    list_filter = (
        "status",
        "start_time",
        "analysis_version__analysis",
        "user",
    )

    class Media:
        css = {"all": ("django_analyses/css/hide_admin_original.css",)}
        # js = ("django_analyses/js/",)

    def duration(self, instance: Run) -> datetime.timedelta:
        return instance.duration

    def analysis_version_link(self, instance: Run) -> str:
        model_name = instance.analysis_version.__class__.__name__
        pk = instance.analysis_version.id
        text = str(instance.analysis_version)
        return Html.admin_link(model_name, pk, text)

    analysis_version_link.short_description = "Analysis Version"

    def user_link(self, instance: Run) -> str:
        if instance.user:
            model_name = instance.user.__class__.__name__
            pk = instance.user.id
            text = instance.user.username
            return Html.admin_link(model_name, pk, text)

    user_link.short_description = "User"

    def _status(self, instance: Run) -> Union[str, bool]:
        if instance.status == "SUCCESS":
            return True
        elif instance.status == "FAILURE":
            return False
        else:
            return None

    _status.boolean = True

    def task_result_(self, instance) -> str:
        if instance.task_result:
            url = reverse(
                "admin:django_celery_results_taskresult_change",
                args=(instance.task_result.id,),
            )
            text = instance.task_result.task_id
            html = f'<a href="{url}">{text}</a>'
            return mark_safe(html)


@admin.register(Input)
class InputAdmin(admin.ModelAdmin):
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

    run_link.short_description = "Run"
    analysis_version_link.short_description = "Analysis Version"
    definition_link.short_description = "Definition"
    input_type.short_description = "Type"


@admin.register(Output)
class OutputAdmin(admin.ModelAdmin):
    list_display = (
        "analysis_version_link",
        "run_link",
        "definition_link",
        "output_type",
        "value",
    )
    list_filter = ("run__analysis_version",)
    list_display_links = None
    search_fields = ("run__id",)
    readonly_fields = (
        "analysis_version_link",
        "definition_link",
        "run_link",
        "output_type",
    )

    def get_queryset(self, request):
        return super().get_queryset(request).select_subclasses()

    def analysis_version(self, instance: Output) -> str:
        return str(instance.run.analysis_version)

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

    run_link.short_description = "Run"
    analysis_version_link.short_description = "Analysis Version"
    definition_link.short_description = "Definition"
    output_type.short_description = "Type"


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
