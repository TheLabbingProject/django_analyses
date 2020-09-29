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
from django.db.models.signals import pre_delete
from django.dispatch import receiver
from django_analyses.models.run import Run


@receiver(pre_delete, sender=Run)
def run_pre_delete_receiver(
    sender: Model, instance: Run, using, **kwargs
) -> None:
    if instance.path:
        shutil.rmtree(instance.path)
