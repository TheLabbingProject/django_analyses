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
                "description": "Simple addition of two floating point numbers.",  # noqa: E501
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
        "description": "Returns the value of base in the power of exponent.",
        "versions": [
            {
                "title": "1.0",
                "description": "Simple power calculation for two floating point numbers.",  # noqa: E501
                "input": {
                    "base": {
                        "type": FloatInputDefinition,
                        "description": "The base for power calculation.",
                        "required": True,
                        "is_configuration": False,
                    },
                    "exponent": {
                        "type": FloatInputDefinition,
                        "description": "The exponent in which the base is raised.",  # noqa: E501
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
                        "description": "Input array. If axis is None, x must be 1-D or 2-D.",  # noqa: E501
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


ADDITION_NODE = {
    "analysis_version": "addition",
    "configuration": {},
}
SQUARE_NODE = {
    "analysis_version": "power",
    "configuration": {"exponent": 2},
}
NORM_NODE = {
    "analysis_version": "norm",
    "configuration": {},
}
PIPELINES = [
    {
        "title": "Test Pipeline 0",
        "description": "Tests a pipeline with two identical nodes.",
        "pipes": [
            {
                "source": ADDITION_NODE,
                "source_run_index": 0,
                "source_port": "result",
                "destination": ADDITION_NODE,
                "destination_run_index": 1,
                "destination_port": "x",
            }
        ],
    },
    {
        "title": "Test Pipeline 1",
        "description": "Interleaved pipeline with identical nodes.",
        "pipes": [
            {
                "source": ADDITION_NODE,
                "source_run_index": 0,
                "source_port": "result",
                "destination": SQUARE_NODE,
                "destination_run_index": 1,
                "destination_port": "base",
            },
            {
                "source": ADDITION_NODE,
                "source_run_index": 1,
                "source_port": "result",
                "destination": ADDITION_NODE,
                "destination_run_index": 2,
                "destination_port": "y",
            },
            {
                "source": SQUARE_NODE,
                "source_run_index": 1,
                "source_port": "result",
                "destination": ADDITION_NODE,
                "destination_run_index": 2,
                "destination_port": "x",
            },
            {
                "source": SQUARE_NODE,
                "source_run_index": 0,
                "source_port": "result",
                "destination": NORM_NODE,
                "destination_run_index": 0,
                "destination_port": "x",
                "index": 1,
            },
            {
                "source": ADDITION_NODE,
                "source_run_index": 2,
                "source_port": "result",
                "destination": NORM_NODE,
                "destination_run_index": 0,
                "destination_port": "x",
                "index": 0,
            },
        ],
    },
]
