Realistic Analysis Integration Example
--------------------------------------

In this example, we will integrate a basic version of
`Nipype <https://github.com/nipy/nipype>`_\'s interface for
`FSL <https://fsl.fmrib.ox.ac.uk/fsl/fslwiki>`_\'s
`SUSAN <https://fsl.fmrib.ox.ac.uk/fsl/fslwiki/SUSAN>`_ noise-reduction
algorithm for MRI images. This example is adapted from
`django_mri <https://github.com/TheLabbingProject/django_mri>`_.

Input and Output Specification
..............................

:class:`~django_analyses.models.managers.input_specification.InputSpecificationManager`
and
:class:`~django_analyses.models.managers.output_specification.OutputSpecificationManager`
provide a :meth:`from_dict` method which can generate specifications based on a
:obj:`dict` with the following structure:

.. code-block:: python

    SPECIFICATION = {
        "definition_key_1": {
            "type": InputDefinitionSubclass,
            "attribute": "value"
        },
        "definition_key_2": {
            "type": InputDefinitionSubclass,
            "attribute": "value2"
        },
    }

If we try to recreate SUSAN's specifications from the
`Nipype's docs <https://nipype.readthedocs.io/en/latest/api/generated/nipype.interfaces.fsl.preprocess.html#susan>`_
according to this structure, it might look something like:

.. code-block:: python
    :caption: susan_specifications.py

    from django_analyses.models.input.definitions import (
        BooleanInputDefinition,
        FileInputDefinition,
        FloatInputDefinition,
        IntegerInputDefinition,
        StringInputDefinition,
    )

    from django_analyses.models.output.definitions import FileOutputDefinition


    SUSAN_INPUT_SPECIFICATION = {
        "brightness_threshold": {
            "type": FloatInputDefinition,
            "required": True,
            "description": "Should be greater than noise level and less than contrast of edges to be preserved.",
        },
        "fwhm": {
            "type": FloatInputDefinition,
            "required": True,
            "description": "FWHM of smoothing, in millimeters.",
        },
        "in_file": {
            "type": FileInputDefinition,
            "required": True,
            "description": "Filename of input time-series.",
        },
        "dimension": {
            "type": IntegerInputDefinition,
            "required": False,
            "default": 3,
            "min_value": 2,
            "max_value": 3,
        },
        "out_file": {
            "type": StringInputDefinition,
            "required": False,
            "description": "Desired output file path.",
            "is_output_path": True,
            "default": "smooth.nii.gz",
        },
        "output_type": {
            "type": StringInputDefinition,
            "required": False,
            "description": "Output file format.",
            "choices": ["NIFTI", "NIFTI_PAIR", "NIFTI_GZ", "NIFTI_PAIR_GZ"],
            "default": "NIFTI_GZ",
        },
        "use_median": {
            "type": BooleanInputDefinition,
            "required": False,
            "default": True,
            "description": "Whether to use a local median filter in the cases where single-point noise is detected.",
        },
        "args": {
            "type": StringInputDefinition,
            "required": False,
            "description": "Additional parameters to pass to the command.",
        },
    }


    SUSAN_OUTPUT_SPECIFICATION = {
        "smoothed_file": {
            "type": FileOutputDefinition,
            "description": "Smoothed output file.",
        }
    }

Analysis Definition
...................

Similarly to the input and output specifications, the
:class:`~django_analyses.models.managers.analysis.AnalysisManager` class exposes a
:meth:`~django_analyses.models.managers.analysis.AnalysisManager.from_list` method
which we could use to easily add analyses to the database.

First we'll create the complete definition in another file.

.. code-block:: python
    :caption: analysis_definitions.py

    from susan_specifications import SUSAN_INPUT_SPECIFICATION, SUSAN_OUTPUT_SPECIFICATION

    analysis_definitions = [
        {
            "title": "SUSAN",
            "description": "Reduces noise in 2/3D images by averaging voxels with similar intensity.",
            "versions": [
                {
                    "title": "1.0.0",
                    "description": "FSL 6.0 version of the SUSAN algorithm.",
                    "input": SUSAN_INPUT_SPECIFICATION,
                    "output": SUSAN_OUTPUT_SPECIFICATION,
                    "nested_results_attribute": "outputs.get_traitsfree",
                }
            ],
        }
    ]

The :attr:`nested_results_attribute` field allows us to integrate smoothly with
`Nipype <https://github.com/nipy/nipype>`_\'s
:class:`~nipype.interfaces.base.specs.BaseTraitedSpec` class by extracting the results
dictionary from the returned object.

All that's left to do is:

.. code-block:: python

    >>> from analysis_definitions import analysis_definitions
    >>> from django_analyses.models import Analysis
    >>> results = Analysis.objects.from_list(analysis_definitions)
    >>> results
    {'SUSAN': {'model': <Analysis: SUSAN>, 'created': True, 'versions': {'1.0.0': {'model': <AnalysisVersion: SUSAN v1.0.0>, 'created': True}}}}

The :meth:`~django_analyses.models.managers.analysis.AnalysisManager.from_list` method
returns a dictionary with references to the specified
:class:`~django_analyses.models.analysis.Analysis` and
:class:`~django_analyses.models.analysis_version.AnalysisVersion` instances and whether
they were created or not.

SUSAN is now an available analysis in our database. Only one thing missing...

Interface Integration
.....................

In order to *django_analyses* to be able to locate the interface used to run this
analysis version, we must add to our project's :code:`ANALYSIS_INTERFACES` setting:

.. code-block:: python
    :caption: settings.py

    from nipype.interfaces.fsl import SUSAN

    ...

    ANALYSIS_INTERFACES = {"SUSAN": {"1.0.0": SUSAN}}


All done!