from django_analysis.utils import ChoiceEnum


class ListElementTypes(ChoiceEnum):
    STR = "String"
    INT = "Integer"
    FLT = "Float"
    BLN = "Boolean"
