from django_analysis.models.input.definitions import (
    BooleanInputDefinition,
    FileInputDefinition,
    FloatInputDefinition,
    IntegerInputDefinition,
    StringInputDefinition,
)

BET_INPUT_SPECIFICATION = {
    "in_file": {
        "type": FileInputDefinition,
        "required": True,
        "description": "A NIfTI format file to skullstrip.",
    },
    "out_file": {
        "type": StringInputDefinition,
        "required": True,
        "description": "Desired output file path.",
    },
    "outline": {
        "type": BooleanInputDefinition,
        "description": "Whether to create a surface outline image.",
    },
    "mask": {
        "type": BooleanInputDefinition,
        "description": "Whether to create a binary mask image.",
    },
    "skull": {
        "type": BooleanInputDefinition,
        "description": "Whether to create a skull image.",
    },
    "no_output": {
        "type": BooleanInputDefinition,
        "description": "Suppress output creation altogether.",
    },
    "frac": {
        "type": FloatInputDefinition,
        "default": 0.5,
        "description": "Fractional intensity threshold.",
        "min_value": 0,
        "max_value": 1,
    },
    "vertical_gradient": {
        "type": FloatInputDefinition,
        "default": 0,
        "description": "Verical gradient in fractional intensity threshold.",
        "min_value": -1,
        "max_value": 1,
    },
    "radius": {
        "type": IntegerInputDefinition,
        "description": "Head radius.",
        "min_value": 0,
    },
}
