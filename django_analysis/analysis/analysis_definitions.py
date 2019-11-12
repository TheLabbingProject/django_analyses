from django_analysis.analysis.specifications.fsl.bet import (
    BET_INPUT_SPECIFICATION,
    BET_OUTPUT_SPECIFICATION,
)
from nipype.interfaces.fsl import BET

analysis_definitions = {
    "BET": {
        "6.0.0": {
            "class": BET,
            "input_specification": BET_INPUT_SPECIFICATION,
            "output_specification": BET_OUTPUT_SPECIFICATION,
        }
    }
}
