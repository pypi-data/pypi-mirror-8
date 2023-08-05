.. AUTO-GENERATED FILE -- DO NOT EDIT!

workflows.rsfmri.fsl.resting
============================


.. module:: nipype.workflows.rsfmri.fsl.resting


.. _nipype.workflows.rsfmri.fsl.resting.create_realign_flow:

:func:`create_realign_flow`
---------------------------

`Link to code <http://github.com/nipy/nipype/tree/e63e055194d62d2bdc4665688261c03a42fd0025/nipype/workflows/rsfmri/fsl/resting.py#L51>`__



Realign a time series to the middle volume using spline interpolation

Uses MCFLIRT to realign the time series and ApplyWarp to apply the rigid
body transformations using spline interpolation (unknown order).

Example
~~~~~~~

>>> wf = create_realign_flow()
>>> wf.inputs.inputspec.func = 'f3.nii'
>>> wf.run() # doctest: +SKIP


Graph
~~~~~

.. graphviz::

	digraph realign{

	  label="realign";

	  realign_inputspec[label="inputspec (utility)"];

	  realign_realigner[label="realigner (fsl)"];

	  realign_splitter[label="splitter (fsl)"];

	  realign_warper[label="warper (fsl)"];

	  realign_joiner[label="joiner (fsl)"];

	  realign_outputspec[label="outputspec (utility)"];

	  realign_inputspec -> realign_realigner;

	  realign_inputspec -> realign_realigner;

	  realign_realigner -> realign_splitter;

	  realign_realigner -> realign_warper;

	  realign_realigner -> realign_warper;

	  realign_splitter -> realign_warper;

	  realign_warper -> realign_joiner;

	  realign_joiner -> realign_outputspec;

	}


.. _nipype.workflows.rsfmri.fsl.resting.create_resting_preproc:

:func:`create_resting_preproc`
------------------------------

`Link to code <http://github.com/nipy/nipype/tree/e63e055194d62d2bdc4665688261c03a42fd0025/nipype/workflows/rsfmri/fsl/resting.py#L92>`__



Create a "resting" time series preprocessing workflow

The noise removal is based on Behzadi et al. (2007)

Parameters
~~~~~~~~~~

name : name of workflow (default: restpreproc)

Inputs::

    inputspec.func : functional run (filename or list of filenames)

Outputs::

    outputspec.noise_mask_file : voxels used for PCA to derive noise components
    outputspec.filtered_file : bandpass filtered and noise-reduced time series

Example
~~~~~~~

>>> TR = 3.0
>>> wf = create_resting_preproc()
>>> wf.inputs.inputspec.func = 'f3.nii'
>>> wf.inputs.inputspec.num_noise_components = 6
>>> wf.inputs.inputspec.highpass_sigma = 100/(2*TR)
>>> wf.inputs.inputspec.lowpass_sigma = 12.5/(2*TR)
>>> wf.run() # doctest: +SKIP


Graph
~~~~~

.. graphviz::

	digraph restpreproc{

	  label="restpreproc";

	  restpreproc_inputspec[label="inputspec (utility)"];

	  restpreproc_slicetimer[label="slicetimer (fsl)"];

	  restpreproc_tsnr[label="tsnr (misc)"];

	  restpreproc_getthreshold[label="getthreshold (fsl)"];

	  restpreproc_threshold[label="threshold (fsl)"];

	  restpreproc_compcorr[label="compcorr (utility)"];

	  restpreproc_remove_noise[label="remove_noise (fsl)"];

	  restpreproc_bandpass_filter[label="bandpass_filter (fsl)"];

	  restpreproc_outputspec[label="outputspec (utility)"];

	  restpreproc_inputspec -> restpreproc_slicetimer;

	  restpreproc_inputspec -> restpreproc_compcorr;

	  restpreproc_inputspec -> restpreproc_bandpass_filter;

	  restpreproc_inputspec -> restpreproc_bandpass_filter;

	  subgraph cluster_restpreproc_realign {

	      label="realign";

	    restpreproc_realign_inputspec[label="inputspec (utility)"];

	    restpreproc_realign_realigner[label="realigner (fsl)"];

	    restpreproc_realign_splitter[label="splitter (fsl)"];

	    restpreproc_realign_warper[label="warper (fsl)"];

	    restpreproc_realign_joiner[label="joiner (fsl)"];

	    restpreproc_realign_outputspec[label="outputspec (utility)"];

	    restpreproc_realign_inputspec -> restpreproc_realign_realigner;

	    restpreproc_realign_inputspec -> restpreproc_realign_realigner;

	    restpreproc_realign_realigner -> restpreproc_realign_splitter;

	    restpreproc_realign_realigner -> restpreproc_realign_warper;

	    restpreproc_realign_realigner -> restpreproc_realign_warper;

	    restpreproc_realign_splitter -> restpreproc_realign_warper;

	    restpreproc_realign_warper -> restpreproc_realign_joiner;

	    restpreproc_realign_joiner -> restpreproc_realign_outputspec;

	  }

	  restpreproc_tsnr -> restpreproc_remove_noise;

	  restpreproc_tsnr -> restpreproc_threshold;

	  restpreproc_tsnr -> restpreproc_getthreshold;

	  restpreproc_getthreshold -> restpreproc_threshold;

	  restpreproc_threshold -> restpreproc_compcorr;

	  restpreproc_threshold -> restpreproc_outputspec;

	  restpreproc_compcorr -> restpreproc_remove_noise;

	  restpreproc_remove_noise -> restpreproc_bandpass_filter;

	  restpreproc_bandpass_filter -> restpreproc_outputspec;

	  restpreproc_slicetimer -> restpreproc_realign_inputspec;

	  restpreproc_realign_outputspec -> restpreproc_tsnr;

	  restpreproc_realign_outputspec -> restpreproc_compcorr;

	}


.. _nipype.workflows.rsfmri.fsl.resting.extract_noise_components:

:func:`extract_noise_components`
--------------------------------

`Link to code <http://github.com/nipy/nipype/tree/e63e055194d62d2bdc4665688261c03a42fd0025/nipype/workflows/rsfmri/fsl/resting.py#L9>`__



Derive components most reflective of physiological noise


.. _nipype.workflows.rsfmri.fsl.resting.select_volume:

:func:`select_volume`
---------------------

`Link to code <http://github.com/nipy/nipype/tree/e63e055194d62d2bdc4665688261c03a42fd0025/nipype/workflows/rsfmri/fsl/resting.py#L38>`__



Return the middle index of a file

