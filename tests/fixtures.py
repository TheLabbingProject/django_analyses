from django_analyses.models.input.definitions.float_input_definition import (
    FloatInputDefinition,
)
from django_analyses.models.input.definitions.list_input_definition import (
    ListInputDefinition,
)
from django_analyses.models.input.definitions.string_input_definition import (
    StringInputDefinition,
)
from django_analyses.models.output.definitions.float_output_definition import (
    FloatOutputDefinition,
)

ANALYSES = [
    {
        "title": "addition",
        "description": "Returns the sum of two numbers.",
        "versions": [
            {
                "title": "1.0",
                "description": "Simple addition of two floating point numbers.",
                "run_method_key": "calculate",
                "input": {
                    "x": {
                        "type": FloatInputDefinition,
                        "description": "One number for addition execution.",
                        "required": True,
                        "is_configuration": False,
                    },
                    "y": {
                        "type": FloatInputDefinition,
                        "description": "Second number for addition execution.",
                        "required": True,
                        "is_configuration": False,
                    },
                },
                "output": {
                    "result": {
                        "type": FloatOutputDefinition,
                        "description": "Result for x + y",
                    }
                },
            }
        ],
    },
    {
        "title": "power",
        "description": "Returns the value of x in the power of y.",
        "versions": [
            {
                "title": "1.0",
                "description": "Simple power calculation for two floating point numbers.",
                "input": {
                    "base": {
                        "type": FloatInputDefinition,
                        "description": "The base for power calculation.",
                        "required": True,
                        "is_configuration": False,
                    },
                    "exponent": {
                        "type": FloatInputDefinition,
                        "description": "The exponent in which the base is raised.",
                        "required": True,
                        "is_configuration": False,
                    },
                },
                "output": {
                    "result": {
                        "type": FloatOutputDefinition,
                        "description": "Result for x in the power of y (x**y)",
                    }
                },
            }
        ],
    },
    {
        "title": "norm",
        "description": "Calculate vector norm.",
        "versions": [
            {
                "title": "NumPy:1.18",
                "description": "Matrix or vector norm.",
                "run_method_key": "normalize",
                "input": {
                    "x": {
                        "type": ListInputDefinition,
                        "element_type": "FLT",
                        "description": "Input array. If axis is None, x must be 1-D or 2-D.",
                        "required": True,
                        "is_configuration": False,
                    },
                    "order": {
                        "type": StringInputDefinition,
                        "description": "Order of the norm.",
                        "default": None,
                        "required": False,
                        "is_configuration": True,
                    },
                },
                "output": {
                    "norm": {
                        "type": FloatOutputDefinition,
                        "description": "The norm of the vector x.",
                    }
                },
            }
        ],
    },
]
