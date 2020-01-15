from django_analyses.models.input.definitions import (
    BooleanInputDefinition,
    FileInputDefinition,
    FloatInputDefinition,
    IntegerInputDefinition,
    ListInputDefinition,
    StringInputDefinition,
)
from django_analyses.models.output.definitions import (
    FileOutputDefinition,
    FloatOutputDefinition,
)

VERSIONLESS_ANALYSIS = {
    "title": "Test Analysis",
    "description": "A description of a test analysis for testing.",
}

INPUT_SPEC_0 = {
    "boolean_input_0": {
        "type": BooleanInputDefinition,
        "description": "A boolean input.",
        "required": True,
    },
    "file_input_0": {
        "type": FileInputDefinition,
        "description": "A file input.",
        "required": True,
        "is_configuration": False,
    },
    "float_input_0": {
        "type": FloatInputDefinition,
        "description": "A float input.",
        "required": False,
    },
    "integer_input_0": {
        "type": IntegerInputDefinition,
        "description": "An integer input.",
        "required": False,
    },
    "list_input_0": {
        "type": ListInputDefinition,
        "description": "An integer input.",
        "required": True,
    },
    "string_input_0": {
        "type": StringInputDefinition,
        "description": "A string input.",
        "required": False,
    },
}

INPUT_SPEC_1 = {
    "boolean_input_1": {
        "type": BooleanInputDefinition,
        "description": "A boolean input.",
        "required": True,
    },
    "file_input_0": {
        "type": FileInputDefinition,
        "description": "A file input.",
        "required": True,
        "is_configuration": False,
    },
    "float_input_1": {
        "type": FloatInputDefinition,
        "description": "A float input.",
        "required": False,
    },
    "integer_input_0": {
        "type": IntegerInputDefinition,
        "description": "An integer input.",
        "required": False,
    },
    "list_input_1": {
        "type": ListInputDefinition,
        "description": "An integer input.",
        "required": True,
    },
    "string_input_0": {
        "type": StringInputDefinition,
        "description": "A string input.",
        "required": False,
    },
}


INPUT_SPEC_2 = {
    "boolean_input_2": {
        "type": BooleanInputDefinition,
        "description": "A boolean input.",
        "required": True,
    },
    "file_input_2": {
        "type": FileInputDefinition,
        "description": "A file input.",
        "required": True,
        "is_configuration": False,
    },
    "float_input_1": {
        "type": FloatInputDefinition,
        "description": "A float input.",
        "required": False,
    },
    "integer_input_2": {
        "type": IntegerInputDefinition,
        "description": "An integer input.",
        "required": False,
    },
    "list_input_2": {
        "type": ListInputDefinition,
        "description": "An integer input.",
        "required": True,
    },
    "string_input_0": {
        "type": StringInputDefinition,
        "description": "A string input.",
        "required": False,
    },
}

OUTPUT_SPEC_0 = {
    "float_output_0": {"type": FloatOutputDefinition, "description": "A float output."},
    "file_output_0": {"type": FileOutputDefinition, "description": "A file output."},
}

OUTPUT_SPEC_1 = {
    "float_output_0": {"type": FloatOutputDefinition, "description": "A float output."},
    "file_output_1": {"type": FileOutputDefinition, "description": "A file output."},
}

OUTPUT_SPEC_2 = {
    "float_output_2": {"type": FloatOutputDefinition, "description": "A float output."},
    "file_output_2": {"type": FileOutputDefinition, "description": "A file output."},
}

ANALYSIS_0 = {
    "title": "Test Versioned Analysis",
    "description": "A description of a test versioned analysis for testing.",
    "versions": [
        {
            "title": "1.0",
            "description": "The first version.",
            "input": INPUT_SPEC_0,
            "output": OUTPUT_SPEC_0,
        },
        {
            "title": "1.1",
            "description": "The first version with some fixes.",
            "input": INPUT_SPEC_1,
            "output": OUTPUT_SPEC_0,
        },
        {
            "title": "2.0",
            "description": "The second version.",
            "input": INPUT_SPEC_1,
            "output": OUTPUT_SPEC_1,
        },
    ],
}

ANALYSIS_1 = {
    "title": "Another Analysis",
    "description": "Another test analysis for testing.",
    "versions": [
        {
            "title": "1.0",
            "description": "The first version.",
            "input": INPUT_SPEC_2,
            "output": OUTPUT_SPEC_2,
        }
    ],
}
