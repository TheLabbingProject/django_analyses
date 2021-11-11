"""
Definition of the :class:`RunStatus` :class:`Enum` subclass.
"""
from django_analyses.utils.choice_enum import ChoiceEnum


class RunStatus(ChoiceEnum):
    STARTED = "Started"
    SUCCESS = "Success"
    FAILURE = "Failure"
