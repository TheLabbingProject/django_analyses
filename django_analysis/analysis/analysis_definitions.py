from django_analysis.analysis.specifications.fsl.bet import (
    BET_INPUT_SPECIFICATION,
    BET_OUTPUT_SPECIFICATION,
)
from nipype.interfaces.fsl import BET

analysis_definitions = {
    "BET": {
        "6.0.0": {
            "class": BET,
            "input": BET_INPUT_SPECIFICATION,
            "output": BET_OUTPUT_SPECIFICATION,
            "nested_results": "outputs.get_traitsfree",
        }
    }
}
