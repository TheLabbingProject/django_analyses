import nipype

from django_analysis.analysis.specifications.fsl.bet import (
    BET_INPUT_SPECIFICATION,
    BET_OUTPUT_SPECIFICATION,
)

from nipype.interfaces.fsl import BET

analysis_definitions = [
    {
        "title": "BET",
        "description": "FSL brain extraction (BET).",
        "versions": [
            {
                "title": BET().version,
                "description": f"Default BET version for nipype {nipype.__version__}.",
                "input": BET_INPUT_SPECIFICATION,
                "output": BET_OUTPUT_SPECIFICATION,
                "nested_results_attribute": "outputs.get_traitsfree",
            }
        ],
    }
]
