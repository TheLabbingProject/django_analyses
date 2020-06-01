Realistic Example
=================

As a realistic pipeline generation usage example we will create a basic brain
MRI preprocessing pipeline using Nipype_\'s interface for FSL_.

The pipeline will receive a NIfTI_ instance from the database as input
and then run:

    1. Brain extraction (BET_)
    2. Reorientation to the MNI152 standard brain template space
       (fslreorient2std_)
    3. Cropping (robustfov_)
    4. Linear registration (FLIRT_)
    5. Nonlinear registration (FNIRT_)

django_mri_ already provides the required analyses, so in order to
create a new pipeline we can simply use a :obj:`dict` defining the pipes
that make up the pipeline.

First, this pipeline assumes the MNI152 standard brain template exists in the
database:

.. code-block:: python
    :caption: basic_fsl_preprocessing.py

    from django_mri.models.nifti import NIfTI


    try:
        MNI = NIfTI.objects.get(path__contains="MNI152_T1_2mm_brain")
    except NIfTI.DoesNotExist:
        raise NIfTI.DoesNotExist("Could not find MNI152_T1_2mm_brain in the database.")


Then, in order to keep things readable, let's define each node's configuration
and create a definition of that node::

    BET_CONFIGURATION = {"robust": True}
    REORIENT_CONFIGURATION = {}
    ROBUSTFOV_CONFIGURATION = {}
    FLIRT_CONFIGURATION = {"reference": MNI.id, "interp": "spline"}
    FNIRT_CONFIGURATION = {"ref_file": MNI.id}

    BET_NODE = {"analysis_version": "BET", "configuration": BET_CONFIGURATION}
    REORIENT_NODE = {
        "analysis_version": "fslreorient2std",
        "configuration": REORIENT_CONFIGURATION,
    }
    ROBUST_FOV_NODE = {
        "analysis_version": "robustfov",
        "configuration": ROBUSTFOV_CONFIGURATION,
    }
    FLIRT_NODE = {
        "analysis_version": "FLIRT",
        "configuration": {"reference": MNI.id, "interp": "spline"},
    }
    FNIRT_NODE = {
        "analysis_version": "FNIRT",
        "configuration": {"ref_file": MNI.id},
    }

Now we can specify the pipes::

    BET_TO_REORIENT = {
        "source": BET_NODE,
        "source_port": "out_file",
        "destination": REORIENT_NODE,
        "destination_port": "in_file",
    }
    REORIENT_TO_FOV = {
        "source": REORIENT_NODE,
        "source_port": "out_file",
        "destination": ROBUST_FOV_NODE,
        "destination_port": "in_file",
    }
    FOV_TO_FLIRT = {
        "source": ROBUST_FOV_NODE,
        "source_port": "out_roi",
        "destination": FLIRT_NODE,
        "destination_port": "in_file",
    }
    FLIRT_TO_FNIRT = {
        "source": FLIRT_NODE,
        "source_port": "out_file",
        "destination": FNIRT_NODE,
        "destination_port": "in_file",
    }

And finally, everything is ready for the pipeline::

    BASIC_FSL_PREPROCESSING = {
        "title": "Basic FSL Preprocessing",
        "description": "Basic MRI preprocessing pipeline using FSL.",
        "pipes": [BET_TO_REORIENT, REORIENT_TO_FOV, FOV_TO_FLIRT, FLIRT_TO_FNIRT],
    }

Add the pipeline to the database::

    >>> from basic_fsl_preprocessing import BASIC_FSL_PREPROCESSING
    >>> from django_analyses.models import Pipeline
    >>> from django_analyses.pipeline_runner import PipelineRunner
    >>> from django_mri.models import Scan

    >>> pipeline = Pipeline.objects.from_dict(BASIC_FSL_PREPROCESSING)
    >>> scan = Scan.objects.filter(description__icontains="MPRAGE").first()
    >>> pipeline_input = {"in_file": scan.nifti}
    >>> pipeline_runner = PipelineRunner(pipeline)
    >>> results = pipeline_runner.run(inputs=pipeline_input)
    >>> results
    {<Node:
    Node #51
    FLIRT v6.0.3:b862cdd5
    Configuration: [{'interp': 'spline', 'reference': 585}]
    >: <Run: #117 FLIRT v6.0.3:b862cdd5 run from 2020-06-01 12:34:51.103207>,
    <Node:
    Node #49
    BET v6.0.3:b862cdd5
    Configuration: [{'robust': True}]
    >: <Run: #114 BET v6.0.3:b862cdd5 run from 2020-06-01 12:34:39.941216>,
    <Node:
    Node #44
    FNIRT v6.0.3:b862cdd5
    Configuration: [{'ref_file': 585}]
    >: <Run: #118 FNIRT v6.0.3:b862cdd5 run from 2020-06-01 12:35:28.673283>,
    <Node:
    Node #43
    robustfov v6.0.3:b862cdd5
    Configuration: [{}]
    >: <Run: #116 robustfov v6.0.3:b862cdd5 run from 2020-06-01 12:34:48.512874>,
    <Node:
    Node #42
    fslreorient2std v6.0.3:b862cdd5
    Configuration: [{}]
    >: <Run: #115 fslreorient2std v6.0.3:b862cdd5 run from 2020-06-01 12:34:46.985302>}

To get our output file we could::

    >>> from django_analyses.models import Run
    >>> from django_mri.models import NIfTI
    >>> run = Run.objects.get(id=118)
    >>> for output in run.output_set.all():
    >>>     print(output.key, output.value)
    fieldcoeff_file NIfTI object (653)
    log_file /media/dir/analysis/118/log.txt
    modulatedref_file NIfTI object (652)
    warped_file NIfTI object (649)
    field_file NIfTI object (650)
    jacobian_file NIfTI object (651)
    >>> path = NIfTI.objects.get(id=649).path
    >>> path
    /media/dir/analysis/118/warped.nii.gz

.. _BET: https://fsl.fmrib.ox.ac.uk/fsl/fslwiki/BET
.. _django_mri: https://github.com/TheLabbingProject/django_mri
.. _fslreorient2std: https://fsl.fmrib.ox.ac.uk/fsl/fslwiki/Orientation%20Explained
.. _FLIRT: https://fsl.fmrib.ox.ac.uk/fsl/fslwiki/FLIRT
.. _FNIRT: https://fsl.fmrib.ox.ac.uk/fsl/fslwiki/FNIRT
.. _FSL: https://fsl.fmrib.ox.ac.uk/fsl/fslwiki
.. _NIfTI: https://nifti.nimh.nih.gov/
.. _Nipype: https://nipype.readthedocs.io/en/latest/
.. _robustfov: https://fsl.fmrib.ox.ac.uk/fsl/fslwiki/InitialProcessing