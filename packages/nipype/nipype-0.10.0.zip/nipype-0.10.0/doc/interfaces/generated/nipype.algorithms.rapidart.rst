.. AUTO-GENERATED FILE -- DO NOT EDIT!

algorithms.rapidart
===================


.. _nipype.algorithms.rapidart.ArtifactDetect:


.. index:: ArtifactDetect

ArtifactDetect
--------------

`Link to code <http://github.com/nipy/nipype/tree/e63e055194d62d2bdc4665688261c03a42fd0025/nipype/algorithms/rapidart.py#L245>`__

Detects outliers in a functional imaging series

Uses intensity and motion parameters to infer outliers. If `use_norm` is
True, it computes the movement of the center of each face a cuboid centered
around the head and returns the maximal movement across the centers.


Examples
~~~~~~~~

>>> ad = ArtifactDetect()
>>> ad.inputs.realigned_files = 'functional.nii'
>>> ad.inputs.realignment_parameters = 'functional.par'
>>> ad.inputs.parameter_source = 'FSL'
>>> ad.inputs.norm_threshold = 1
>>> ad.inputs.use_differences = [True, False]
>>> ad.inputs.zintensity_threshold = 3
>>> ad.run() # doctest: +SKIP

Inputs::

        [Mandatory]
        mask_type: ('spm_global' or 'file' or 'thresh')
                Type of mask that should be used to mask the functional data.
                *spm_global* uses an spm_global like calculation to determine the
                brain mask. *file* specifies a brain mask file (should be an image
                file consisting of 0s and 1s). *thresh* specifies a threshold to
                use. By default all voxelsare used, unless one of these mask types
                are defined.
        norm_threshold: (a float)
                Threshold to use to detect motion-related outliers when composite
                motion is being used
                mutually_exclusive: rotation_threshold, translation_threshold
        parameter_source: ('SPM' or 'FSL' or 'AFNI' or 'NiPy' or 'FSFAST')
                Source of movement parameters
        realigned_files: (an existing file name)
                Names of realigned functional data files
        realignment_parameters: (an existing file name)
                Names of realignment parameterscorresponding to the functional data
                files
        rotation_threshold: (a float)
                Threshold (in radians) to use to detect rotation-related outliers
                mutually_exclusive: norm_threshold
        translation_threshold: (a float)
                Threshold (in mm) to use to detect translation-related outliers
                mutually_exclusive: norm_threshold
        zintensity_threshold: (a float)
                Intensity Z-threshold use to detection images that deviate from the
                mean

        [Optional]
        bound_by_brainmask: (a boolean, nipype default value: False)
                use the brain mask to determine bounding boxfor composite norm
                (worksfor SPM and Nipy - currentlyinaccurate for FSL, AFNI
        global_threshold: (a float, nipype default value: 8.0)
                use this threshold when mask type equal's spm_global
        ignore_exception: (a boolean, nipype default value: False)
                Print an error message instead of throwing an exception in case the
                interface fails to run
        intersect_mask: (a boolean)
                Intersect the masks when computed from spm_global.
        mask_file: (an existing file name)
                Mask file to be used if mask_type is 'file'.
        mask_threshold: (a float)
                Mask threshold to be used if mask_type is 'thresh'.
        plot_type: ('png' or 'svg' or 'eps' or 'pdf', nipype default value:
                 png)
                file type of the outlier plot
        save_plot: (a boolean, nipype default value: True)
                save plots containing outliers
        use_differences: (a list of items which are an implementor of, or can
                 be adapted to implement, bool or None, nipype default value: [True,
                 False])
                Use differences between successive motion (first element)and
                intensity paramter (second element) estimates in orderto determine
                outliers. (default is [True, False])
        use_norm: (a boolean, nipype default value: True)
                Uses a composite of the motion parameters in order to determine
                outliers.
                requires: norm_threshold

Outputs::

        displacement_files: (a file name)
                One image file for each functional run containing the
                voxeldisplacement timeseries
        intensity_files: (an existing file name)
                One file for each functional run containing the global intensity
                values determined from the brainmask
        mask_files: (a file name)
                One image file for each functional run containing the maskused for
                global signal calculation
        norm_files: (a file name)
                One file for each functional run containing the composite norm
        outlier_files: (an existing file name)
                One file for each functional run containing a list of 0-based
                indices corresponding to outlier volumes
        plot_files: (a file name)
                One image file for each functional run containing the detected
                outliers
        statistic_files: (an existing file name)
                One file for each functional run containing information about the
                different types of artifacts and if design info is provided then
                details of stimulus correlated motion and a listing or artifacts by
                event type.

.. _nipype.algorithms.rapidart.StimulusCorrelation:


.. index:: StimulusCorrelation

StimulusCorrelation
-------------------

`Link to code <http://github.com/nipy/nipype/tree/e63e055194d62d2bdc4665688261c03a42fd0025/nipype/algorithms/rapidart.py#L561>`__

Determines if stimuli are correlated with motion or intensity
parameters.

Currently this class supports an SPM generated design matrix and requires
intensity parameters. This implies that one must run
:ref:`ArtifactDetect <nipype.algorithms.rapidart.ArtifactDetect>`
and :ref:`Level1Design <nipype.interfaces.spm.model.Level1Design>` prior to running this or
provide an SPM.mat file and intensity parameters through some other means.

Examples
~~~~~~~~

>>> sc = StimulusCorrelation()
>>> sc.inputs.realignment_parameters = 'functional.par'
>>> sc.inputs.intensity_values = 'functional.rms'
>>> sc.inputs.spm_mat_file = 'SPM.mat'
>>> sc.inputs.concatenated_design = False
>>> sc.run() # doctest: +SKIP

Inputs::

        [Mandatory]
        concatenated_design: (a boolean)
                state if the design matrix contains concatenated sessions
        intensity_values: (an existing file name)
                Name of file containing intensity values
        realignment_parameters: (an existing file name)
                Names of realignment parameters corresponding to the functional data
                files
        spm_mat_file: (an existing file name)
                SPM mat file (use pre-estimate SPM.mat file)

        [Optional]
        ignore_exception: (a boolean, nipype default value: False)
                Print an error message instead of throwing an exception in case the
                interface fails to run

Outputs::

        stimcorr_files: (an existing file name)
                List of files containing correlation values
