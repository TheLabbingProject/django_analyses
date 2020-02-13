from django_analyses.utils.choice_enum import ChoiceEnum


class ListElementTypes(ChoiceEnum):
    STR = "String"
    INT = "Integer"
    FLT = "Float"
    BLN = "Boolean"
    FIL = "File"


TYPES_DICT = {
    ListElementTypes.STR: str,
    ListElementTypes.INT: int,
    ListElementTypes.FLT: float,
    ListElementTypes.BLN: bool,
    ListElementTypes.FIL: "file",
}
