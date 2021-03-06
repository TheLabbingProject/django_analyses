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

from django.contrib import admin
from django.urls import reverse
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
from django.utils.safestring import mark_safe
from typing import Union


class AnalysisVersionInline(admin.TabularInline):
    model = AnalysisVersion


@admin.register(Analysis)
class AnalysisAdmin(admin.ModelAdmin):
    list_display = ("title", "description", "created", "modified")
    inlines = [AnalysisVersionInline]


class InputInline(admin.TabularInline):
    model = Input
    readonly_fields = ("key", "value")
    extra = 0

    def get_queryset(self, request):
        return super().get_queryset(request).select_subclasses()


class OutputInline(admin.TabularInline):
    model = Output
    readonly_fields = ("key", "value")
    extra = 0

    def get_queryset(self, request):
        return super().get_queryset(request).select_subclasses()


@admin.register(AnalysisVersion)
class AnalysisVersionAdmin(admin.ModelAdmin):
    fieldsets = (
        (None, {"fields": ("analysis", "title", "description")}),
        (
            "Advanced Options",
            {
                "classes": ("collapse",),
                "fields": ("run_method_key", "nested_results_attribute",),
            },
        ),
    )

    def name(self, instance) -> str:
        return str(instance)


@admin.register(Run)
class RunAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "analysis_version",
        "user",
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
        "user",
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

    def duration(self, instance: Run) -> datetime.timedelta:
        return instance.duration

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
    list_display = ("run_id", "key", "value", "analysis_version")
    list_filter = ("run__analysis_version",)
    list_display_links = None
    search_fields = ("run__id",)

    def get_queryset(self, request):
        return (
            super(InputAdmin, self).get_queryset(request).select_subclasses()
        )

    def analysis_version(self, instance) -> str:
        return str(instance.run.analysis_version)

    def run_id(self, instance) -> str:
        return instance.run.id


@admin.register(Output)
class OutputAdmin(admin.ModelAdmin):
    list_display = ("run_id", "key", "value", "analysis_version")
    list_filter = (
        "run__analysis_version",
        "run__id",
    )
    list_display_links = None

    def get_queryset(self, request):
        return (
            super(OutputAdmin, self).get_queryset(request).select_subclasses()
        )

    def run_id(self, instance) -> str:
        return instance.run.id

    def analysis_version(self, instance) -> str:
        return str(instance.run.analysis_version)


@admin.register(InputDefinition)
class InputDefinitionAdmin(admin.ModelAdmin):
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

    def get_queryset(self, request):
        return (
            super(InputDefinitionAdmin, self)
            .get_queryset(request)
            .select_subclasses()
        )

    def choices(self, instance) -> list:
        return instance.choices if hasattr(instance, "choices") else []

    def min_value(self, instance):
        return instance.min_value if hasattr(instance, "min_value") else None

    def max_value(self, instance):
        return instance.max_value if hasattr(instance, "max_value") else None


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
    model = InputDefinition.specification_set.through
    verbose_name_plural = "Input Definitions"


@admin.register(InputSpecification)
class InputSpecificationAdmin(admin.ModelAdmin):
    fields = ("analysis",)
    list_display = ("id", "analysis")
    list_filter = ("analysis",)
    inlines = [InputDefinitionsInline]


@admin.register(OutputSpecification)
class OutputSpecificationAdmin(admin.ModelAdmin):
    fields = ("analysis",)
    list_display = ("id", "analysis")
    list_filter = ("analysis",)
