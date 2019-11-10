from django_analysis.input_specifications.fsl.bet import BET_INPUT_SPECIFICATION
from nipype.interfaces.fsl import BET

model_to_analysis = {
    "BET": {"6.0.0": {"class": BET, "input_specification": BET_INPUT_SPECIFICATION}}
}
