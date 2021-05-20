from django_analyses.utils.choice_enum import ChoiceEnum


class OutputTypes(ChoiceEnum):
    FIL = "File"
    FLT = "Float"
    LST = "List"
