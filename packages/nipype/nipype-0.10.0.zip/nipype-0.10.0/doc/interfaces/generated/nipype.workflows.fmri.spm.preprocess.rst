.. AUTO-GENERATED FILE -- DO NOT EDIT!

workflows.fmri.spm.preprocess
=============================


.. module:: nipype.workflows.fmri.spm.preprocess


.. _nipype.workflows.fmri.spm.preprocess.create_DARTEL_template:

:func:`create_DARTEL_template`
------------------------------

`Link to code <http://github.com/nipy/nipype/tree/e63e055194d62d2bdc4665688261c03a42fd0025/nipype/workflows/fmri/spm/preprocess.py#L224>`__



Create a vbm workflow that generates DARTEL-based template


Example
~~~~~~~

>>> preproc = create_DARTEL_template()
>>> preproc.inputs.inputspec.structural_files = [os.path.abspath('s1.nii'), os.path.abspath('s3.nii')]
>>> preproc.inputs.inputspec.template_prefix = 'Template'
>>> preproc.run() # doctest: +SKIP

Inputs::

     inputspec.structural_files : structural data to be used to create templates
     inputspec.template_prefix : prefix for dartel template

Outputs::

     outputspec.template_file : DARTEL template
     outputspec.flow_fields : warps from input struct files to the template


Graph
~~~~~

.. graphviz::

	digraph dartel_template{

	  label="dartel_template";

	  dartel_template_inputspec[label="inputspec (utility)"];

	  dartel_template_segment[label="segment (spm)"];

	  dartel_template_dartel[label="dartel (spm)"];

	  dartel_template_outputspec[label="outputspec (utility)"];

	  dartel_template_inputspec -> dartel_template_dartel;

	  dartel_template_inputspec -> dartel_template_segment;

	  dartel_template_segment -> dartel_template_dartel;

	  dartel_template_dartel -> dartel_template_outputspec;

	  dartel_template_dartel -> dartel_template_outputspec;

	}


.. _nipype.workflows.fmri.spm.preprocess.create_spm_preproc:

:func:`create_spm_preproc`
--------------------------

`Link to code <http://github.com/nipy/nipype/tree/e63e055194d62d2bdc4665688261c03a42fd0025/nipype/workflows/fmri/spm/preprocess.py#L15>`__



Create an spm preprocessing workflow with freesurfer registration and
artifact detection.

The workflow realigns and smooths and registers the functional images with
the subject's freesurfer space.

Example
~~~~~~~

>>> preproc = create_spm_preproc()
>>> preproc.base_dir = '.'
>>> preproc.inputs.inputspec.fwhm = 6
>>> preproc.inputs.inputspec.subject_id = 's1'
>>> preproc.inputs.inputspec.subjects_dir = '.'
>>> preproc.inputs.inputspec.functionals = ['f3.nii', 'f5.nii']
>>> preproc.inputs.inputspec.norm_threshold = 1
>>> preproc.inputs.inputspec.zintensity_threshold = 3

Inputs::

     inputspec.functionals : functional runs use 4d nifti
     inputspec.subject_id : freesurfer subject id
     inputspec.subjects_dir : freesurfer subjects dir
     inputspec.fwhm : smoothing fwhm
     inputspec.norm_threshold : norm threshold for outliers
     inputspec.zintensity_threshold : intensity threshold in z-score

Outputs::

     outputspec.realignment_parameters : realignment parameter files
     outputspec.smoothed_files : smoothed functional files
     outputspec.outlier_files : list of outliers
     outputspec.outlier_stats : statistics of outliers
     outputspec.outlier_plots : images of outliers
     outputspec.mask_file : binary mask file in reference image space
     outputspec.reg_file : registration file that maps reference image to
                             freesurfer space
     outputspec.reg_cost : cost of registration (useful for detecting misalignment)


Graph
~~~~~

.. graphviz::

	digraph preproc{

	  label="preproc";

	  preproc_inputspec[label="inputspec (utility)"];

	  preproc_realign[label="realign (spm)"];

	  preproc_smooth[label="smooth (spm)"];

	  preproc_artdetect[label="artdetect (rapidart)"];

	  preproc_outputspec[label="outputspec (utility)"];

	  preproc_inputspec -> preproc_realign;

	  preproc_inputspec -> preproc_artdetect;

	  preproc_inputspec -> preproc_artdetect;

	  preproc_inputspec -> preproc_smooth;

	  preproc_realign -> preproc_outputspec;

	  preproc_realign -> preproc_smooth;

	  preproc_realign -> preproc_artdetect;

	  preproc_realign -> preproc_artdetect;

	  subgraph cluster_preproc_getmask {

	      label="getmask";

	    preproc_getmask_inputspec[label="inputspec (utility)"];

	    preproc_getmask_register[label="register (freesurfer)"];

	    preproc_getmask_fssource[label="fssource (io)"];

	    preproc_getmask_threshold[label="threshold (freesurfer)"];

	    preproc_getmask_transform[label="transform (freesurfer)"];

	    preproc_getmask_threshold2[label="threshold2 (freesurfer)"];

	    preproc_getmask_outputspec[label="outputspec (utility)"];

	    preproc_getmask_inputspec -> preproc_getmask_register;

	    preproc_getmask_inputspec -> preproc_getmask_register;

	    preproc_getmask_inputspec -> preproc_getmask_register;

	    preproc_getmask_inputspec -> preproc_getmask_register;

	    preproc_getmask_inputspec -> preproc_getmask_fssource;

	    preproc_getmask_inputspec -> preproc_getmask_fssource;

	    preproc_getmask_inputspec -> preproc_getmask_transform;

	    preproc_getmask_inputspec -> preproc_getmask_transform;

	    preproc_getmask_register -> preproc_getmask_transform;

	    preproc_getmask_register -> preproc_getmask_outputspec;

	    preproc_getmask_register -> preproc_getmask_outputspec;

	    preproc_getmask_fssource -> preproc_getmask_threshold;

	    preproc_getmask_threshold -> preproc_getmask_transform;

	    preproc_getmask_transform -> preproc_getmask_threshold2;

	    preproc_getmask_threshold2 -> preproc_getmask_outputspec;

	  }

	  preproc_smooth -> preproc_outputspec;

	  preproc_artdetect -> preproc_outputspec;

	  preproc_artdetect -> preproc_outputspec;

	  preproc_artdetect -> preproc_outputspec;

	  preproc_inputspec -> preproc_getmask_inputspec;

	  preproc_inputspec -> preproc_getmask_inputspec;

	  preproc_realign -> preproc_getmask_inputspec;

	  preproc_getmask_outputspec -> preproc_artdetect;

	  preproc_getmask_outputspec -> preproc_outputspec;

	  preproc_getmask_outputspec -> preproc_outputspec;

	  preproc_getmask_outputspec -> preproc_outputspec;

	}


.. _nipype.workflows.fmri.spm.preprocess.create_vbm_preproc:

:func:`create_vbm_preproc`
--------------------------

`Link to code <http://github.com/nipy/nipype/tree/e63e055194d62d2bdc4665688261c03a42fd0025/nipype/workflows/fmri/spm/preprocess.py#L131>`__



Create a vbm workflow that generates DARTEL-based warps to MNI space

Based on: http://www.fil.ion.ucl.ac.uk/~john/misc/VBMclass10.pdf

Example
~~~~~~~

>>> preproc = create_vbm_preproc()
>>> preproc.inputs.inputspec.fwhm = 8
>>> preproc.inputs.inputspec.structural_files = [os.path.abspath('s1.nii'), os.path.abspath('s3.nii')]
>>> preproc.inputs.inputspec.template_prefix = 'Template'
>>> preproc.run() # doctest: +SKIP

Inputs::

     inputspec.structural_files : structural data to be used to create templates
     inputspec.fwhm: single of triplet for smoothing when normalizing to MNI space
     inputspec.template_prefix : prefix for dartel template

Outputs::

     outputspec.normalized_files : normalized gray matter files
     outputspec.template_file : DARTEL template
     outputspec.icv : intracranial volume (cc - assuming dimensions in mm)


Graph
~~~~~

.. graphviz::

	digraph vbmpreproc{

	  label="vbmpreproc";

	  vbmpreproc_inputspec[label="inputspec (utility)"];

	  vbmpreproc_norm2mni[label="norm2mni (spm)"];

	  vbmpreproc_calc_icv[label="calc_icv (utility)"];

	  vbmpreproc_outputspec[label="outputspec (utility)"];

	  vbmpreproc_inputspec -> vbmpreproc_norm2mni;

	  subgraph cluster_vbmpreproc_dartel_template {

	      label="dartel_template";

	    vbmpreproc_dartel_template_inputspec[label="inputspec (utility)"];

	    vbmpreproc_dartel_template_segment[label="segment (spm)"];

	    vbmpreproc_dartel_template_dartel[label="dartel (spm)"];

	    vbmpreproc_dartel_template_outputspec[label="outputspec (utility)"];

	    vbmpreproc_dartel_template_inputspec -> vbmpreproc_dartel_template_segment;

	    vbmpreproc_dartel_template_inputspec -> vbmpreproc_dartel_template_dartel;

	    vbmpreproc_dartel_template_segment -> vbmpreproc_dartel_template_dartel;

	    vbmpreproc_dartel_template_dartel -> vbmpreproc_dartel_template_outputspec;

	    vbmpreproc_dartel_template_dartel -> vbmpreproc_dartel_template_outputspec;

	  }

	  vbmpreproc_norm2mni -> vbmpreproc_outputspec;

	  vbmpreproc_calc_icv -> vbmpreproc_outputspec;

	  vbmpreproc_inputspec -> vbmpreproc_dartel_template_inputspec;

	  vbmpreproc_inputspec -> vbmpreproc_dartel_template_inputspec;

	  vbmpreproc_dartel_template_outputspec -> vbmpreproc_norm2mni;

	  vbmpreproc_dartel_template_outputspec -> vbmpreproc_norm2mni;

	  vbmpreproc_dartel_template_segment -> vbmpreproc_norm2mni;

	  vbmpreproc_dartel_template_segment -> vbmpreproc_calc_icv;

	  vbmpreproc_dartel_template_outputspec -> vbmpreproc_outputspec;

	}

