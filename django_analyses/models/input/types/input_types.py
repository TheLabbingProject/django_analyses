from django_analyses.utils.choice_enum import ChoiceEnum


class InputTypes(ChoiceEnum):
    STR = "String"
    BLN = "Boolean"
    FIL = "File"
    DIR = "Directory"
    INT = "Integer"
    FLT = "Float"
    LST = "List"
