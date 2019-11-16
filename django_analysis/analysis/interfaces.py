from nipype.interfaces.fsl import BET, FLIRT

interfaces = {"BET": {BET().version: BET}, "FLIRT": {FLIRT().version: FLIRT}}
