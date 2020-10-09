"""
Signal receivers.

References
----------
* Signals_

.. _Signals:
   https://docs.djangoproject.com/en/3.0/ref/signals/
"""

import shutil

from django.db.models import Model
from django.db.models.signals import pre_delete, post_save
from django.dispatch import receiver
from django_analyses.models.run import Run
from django_celery_results.models import TaskResult


@receiver(pre_delete, sender=Run)
def run_pre_delete_receiver(
    sender: Model, instance: Run, using, **kwargs
) -> None:
    if instance.path:
        shutil.rmtree(instance.path)


@receiver(post_save, sender=TaskResult)
def task_result_post_save_receiver(
    sender: Model, instance: TaskResult, created: bool, **kwargs
) -> None:
    if instance.name == "django_analyses.node-execution":
        run_id = instance.result
        if created and run_id:
            run = Run.objects.get(id=run_id)
            run.task_result = instance
            run.save()
