.. AUTO-GENERATED FILE -- DO NOT EDIT!

workflows.dmri.camino.diffusion
===============================


.. module:: nipype.workflows.dmri.camino.diffusion


.. _nipype.workflows.dmri.camino.diffusion.create_camino_dti_pipeline:

:func:`create_camino_dti_pipeline`
----------------------------------

`Link to code <http://github.com/nipy/nipype/tree/e63e055194d62d2bdc4665688261c03a42fd0025/nipype/workflows/dmri/camino/diffusion.py#L9>`__



Creates a pipeline that does the same diffusion processing as in the
:doc:`../../users/examples/dmri_camino_dti` example script. Given a diffusion-weighted image,
b-values, and b-vectors, the workflow will return the tractography
computed from diffusion tensors and from PICo probabilistic tractography.

Example
~~~~~~~

>>> import os
>>> nipype_camino_dti = create_camino_dti_pipeline("nipype_camino_dti")
>>> nipype_camino_dti.inputs.inputnode.dwi = os.path.abspath('dwi.nii')
>>> nipype_camino_dti.inputs.inputnode.bvecs = os.path.abspath('bvecs')
>>> nipype_camino_dti.inputs.inputnode.bvals = os.path.abspath('bvals')
>>> nipype_camino_dti.run()                  # doctest: +SKIP

Inputs::

    inputnode.dwi
    inputnode.bvecs
    inputnode.bvals

Outputs::

    outputnode.fa
    outputnode.trace
    outputnode.tracts_pico
    outputnode.tracts_dt
    outputnode.tensors


Graph
~~~~~

.. graphviz::

	digraph dtiproc{

	  label="dtiproc";

	  dtiproc_inputnode[label="inputnode (utility)"];

	  dtiproc_outputnode[label="outputnode (utility)"];

	  subgraph cluster_dtiproc_tractography {

	      label="tractography";

	    dtiproc_tractography_inputnode1[label="inputnode1 (utility)"];

	    dtiproc_tractography_image2voxel[label="image2voxel (camino)"];

	    dtiproc_tractography_bet[label="bet (fsl)"];

	    dtiproc_tractography_fsl2scheme[label="fsl2scheme (camino)"];

	    dtiproc_tractography_dtlutgen[label="dtlutgen (camino)"];

	    dtiproc_tractography_dtifit[label="dtifit (camino)"];

	    dtiproc_tractography_dteig[label="dteig (camino)"];

	    dtiproc_tractography_picopdfs[label="picopdfs (camino)"];

	    dtiproc_tractography_trackpico[label="trackpico (camino)"];

	    dtiproc_tractography_cam2trk_pico[label="cam2trk_pico (camino2trackvis)"];

	    dtiproc_tractography_trace[label="trace (camino)"];

	    dtiproc_tractography_analyzeheader_trace[label="analyzeheader_trace (camino)"];

	    dtiproc_tractography_trace2nii[label="trace2nii (misc)"];

	    dtiproc_tractography_trackdt[label="trackdt (camino)"];

	    dtiproc_tractography_cam2trk_dt[label="cam2trk_dt (camino2trackvis)"];

	    dtiproc_tractography_fa[label="fa (camino)"];

	    dtiproc_tractography_analyzeheader_fa[label="analyzeheader_fa (camino)"];

	    dtiproc_tractography_fa2nii[label="fa2nii (misc)"];

	    dtiproc_tractography_inputnode1 -> dtiproc_tractography_trace2nii;

	    dtiproc_tractography_inputnode1 -> dtiproc_tractography_analyzeheader_trace;

	    dtiproc_tractography_inputnode1 -> dtiproc_tractography_analyzeheader_trace;

	    dtiproc_tractography_inputnode1 -> dtiproc_tractography_cam2trk_pico;

	    dtiproc_tractography_inputnode1 -> dtiproc_tractography_cam2trk_pico;

	    dtiproc_tractography_inputnode1 -> dtiproc_tractography_bet;

	    dtiproc_tractography_inputnode1 -> dtiproc_tractography_analyzeheader_fa;

	    dtiproc_tractography_inputnode1 -> dtiproc_tractography_analyzeheader_fa;

	    dtiproc_tractography_inputnode1 -> dtiproc_tractography_image2voxel;

	    dtiproc_tractography_inputnode1 -> dtiproc_tractography_cam2trk_dt;

	    dtiproc_tractography_inputnode1 -> dtiproc_tractography_cam2trk_dt;

	    dtiproc_tractography_inputnode1 -> dtiproc_tractography_fa2nii;

	    dtiproc_tractography_inputnode1 -> dtiproc_tractography_fsl2scheme;

	    dtiproc_tractography_inputnode1 -> dtiproc_tractography_fsl2scheme;

	    dtiproc_tractography_image2voxel -> dtiproc_tractography_dtifit;

	    dtiproc_tractography_bet -> dtiproc_tractography_trackpico;

	    dtiproc_tractography_bet -> dtiproc_tractography_trackdt;

	    dtiproc_tractography_fsl2scheme -> dtiproc_tractography_dtifit;

	    dtiproc_tractography_fsl2scheme -> dtiproc_tractography_dtlutgen;

	    dtiproc_tractography_dtlutgen -> dtiproc_tractography_picopdfs;

	    dtiproc_tractography_dtifit -> dtiproc_tractography_dteig;

	    dtiproc_tractography_dtifit -> dtiproc_tractography_picopdfs;

	    dtiproc_tractography_dtifit -> dtiproc_tractography_trace;

	    dtiproc_tractography_dtifit -> dtiproc_tractography_trackdt;

	    dtiproc_tractography_dtifit -> dtiproc_tractography_fa;

	    dtiproc_tractography_picopdfs -> dtiproc_tractography_trackpico;

	    dtiproc_tractography_trackpico -> dtiproc_tractography_cam2trk_pico;

	    dtiproc_tractography_trace -> dtiproc_tractography_analyzeheader_trace;

	    dtiproc_tractography_trace -> dtiproc_tractography_trace2nii;

	    dtiproc_tractography_analyzeheader_trace -> dtiproc_tractography_trace2nii;

	    dtiproc_tractography_trackdt -> dtiproc_tractography_cam2trk_dt;

	    dtiproc_tractography_fa -> dtiproc_tractography_analyzeheader_fa;

	    dtiproc_tractography_fa -> dtiproc_tractography_fa2nii;

	    dtiproc_tractography_analyzeheader_fa -> dtiproc_tractography_fa2nii;

	  }

	  dtiproc_inputnode -> dtiproc_tractography_inputnode1;

	  dtiproc_inputnode -> dtiproc_tractography_inputnode1;

	  dtiproc_inputnode -> dtiproc_tractography_inputnode1;

	  dtiproc_tractography_cam2trk_dt -> dtiproc_outputnode;

	  dtiproc_tractography_cam2trk_pico -> dtiproc_outputnode;

	  dtiproc_tractography_fa2nii -> dtiproc_outputnode;

	  dtiproc_tractography_trace2nii -> dtiproc_outputnode;

	  dtiproc_tractography_dtifit -> dtiproc_outputnode;

	}

