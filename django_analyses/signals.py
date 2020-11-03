"""
Signal receivers.

References
----------
* Signals_

.. _Signals:
   https://docs.djangoproject.com/en/3.0/ref/signals/
"""

import json
import shutil

from django.db.models import Model
from django.db.models.signals import pre_delete
from django.dispatch import receiver
from django_analyses.models.run import Run
from django_celery_results.models import TaskResult


@receiver(pre_delete, sender=Run)
def run_pre_delete_receiver(
    sender: Model, instance: Run, using, **kwargs
) -> None:
    """
    Remove a Run instance's directory when deleted.

    Parameters
    ----------
    sender : Model
        The :class:`~django_analyses.models.run.Run` model
    instance : Run
        The Run instance
    using : Any
        pre_delete signal argument
    """

    if instance.path:
        shutil.rmtree(instance.path)


# Managing the association of Run instances with TaskResults

STARMAP = "celery.starmap"


def handle_node_execution_end(task_result: TaskResult, created: bool) -> None:
    run_ids = json.loads(task_result.result)
    if task_result.status == "SUCCESS" and run_ids:
        if isinstance(run_ids, int):
            associate_run_with_task(run_ids, task_result)
        else:
            for run_id in run_ids:
                associate_run_with_task(run_id, task_result)


def associate_run_with_task(run_id: int, task_result: TaskResult) -> None:
    run = Run.objects.get(id=run_id)
    if run.task_result != task_result:
        run.task_result = task_result
        run.save()


POST_TASK_RESULT_HANDLERS = {
    "django_analyses.node-execution": handle_node_execution_end
}


# @receiver(post_save, sender=TaskResult)
# def task_result_post_save_receiver(
#     sender: Model, instance: TaskResult, created: bool, **kwargs
# ) -> None:
#     handler = POST_TASK_RESULT_HANDLERS.get(instance.task_name)
#     if handler:
#         handler(instance, created)


# TODO: Fix for STARMAP tasks (group/chunk) so that the handler will iterate
# the results. This is currently difficult because task_kwargs returns as a
# string and it's hard to infer the task's name and therefore to match a
# handler.
