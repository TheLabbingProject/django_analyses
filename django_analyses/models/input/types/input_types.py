from pylabber.utils import ChoiceEnum


class InputTypes(ChoiceEnum):
    STR = "String"
    BLN = "Boolean"
    FIL = "File"
    DIR = "Directory"
    INT = "Integer"
    FLT = "Float"
    LST = "List"
