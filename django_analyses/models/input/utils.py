from django_analyses.utils.choice_enum import ChoiceEnum


class ListElementTypes(ChoiceEnum):
    BLN = "Boolean"
    INT = "Integer"
    FIL = "File"
    FLT = "Float"
    STR = "String"
    TUP = "Tuple"


TYPES_DICT = {
    ListElementTypes.STR: str,
    ListElementTypes.INT: int,
    ListElementTypes.FLT: float,
    ListElementTypes.BLN: bool,
    ListElementTypes.FIL: "file",
    ListElementTypes.TUP: tuple,
}
