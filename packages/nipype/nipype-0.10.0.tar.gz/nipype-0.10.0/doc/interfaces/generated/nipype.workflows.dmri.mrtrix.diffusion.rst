.. AUTO-GENERATED FILE -- DO NOT EDIT!

workflows.dmri.mrtrix.diffusion
===============================


.. module:: nipype.workflows.dmri.mrtrix.diffusion


.. _nipype.workflows.dmri.mrtrix.diffusion.create_mrtrix_dti_pipeline:

:func:`create_mrtrix_dti_pipeline`
----------------------------------

`Link to code <http://github.com/nipy/nipype/tree/e63e055194d62d2bdc4665688261c03a42fd0025/nipype/workflows/dmri/mrtrix/diffusion.py#L6>`__



Creates a pipeline that does the same diffusion processing as in the
:doc:`../../users/examples/dmri_mrtrix_dti` example script. Given a diffusion-weighted image,
b-values, and b-vectors, the workflow will return the tractography
computed from spherical deconvolution and probabilistic streamline tractography

Example
~~~~~~~

>>> dti = create_mrtrix_dti_pipeline("mrtrix_dti")
>>> dti.inputs.inputnode.dwi = 'data.nii'
>>> dti.inputs.inputnode.bvals = 'bvals'
>>> dti.inputs.inputnode.bvecs = 'bvecs'
>>> dti.run()                  # doctest: +SKIP

Inputs::

    inputnode.dwi
    inputnode.bvecs
    inputnode.bvals

Outputs::

    outputnode.fa
    outputnode.tdi
    outputnode.tracts_tck
    outputnode.tracts_trk
    outputnode.csdeconv


Graph
~~~~~

.. graphviz::

	digraph dtiproc{

	  label="dtiproc";

	  dtiproc_inputnode[label="inputnode (utility)"];

	  dtiproc_bet[label="bet (fsl)"];

	  dtiproc_fsl2mrtrix[label="fsl2mrtrix (mrtrix)"];

	  dtiproc_MRconvert[label="MRconvert (mrtrix)"];

	  dtiproc_threshold_b0[label="threshold_b0 (mrtrix)"];

	  dtiproc_median3D[label="median3D (mrtrix)"];

	  dtiproc_erode_mask_firstpass[label="erode_mask_firstpass (mrtrix)"];

	  dtiproc_erode_mask_secondpass[label="erode_mask_secondpass (mrtrix)"];

	  dtiproc_dwi2tensor[label="dwi2tensor (mrtrix)"];

	  dtiproc_tensor2vector[label="tensor2vector (mrtrix)"];

	  dtiproc_tensor2adc[label="tensor2adc (mrtrix)"];

	  dtiproc_gen_WM_mask[label="gen_WM_mask (mrtrix)"];

	  dtiproc_threshold_wmmask[label="threshold_wmmask (mrtrix)"];

	  dtiproc_tensor2fa[label="tensor2fa (mrtrix)"];

	  dtiproc_MRmultiply_merge[label="MRmultiply_merge (utility)"];

	  dtiproc_MRmultiply[label="MRmultiply (mrtrix)"];

	  dtiproc_threshold_FA[label="threshold_FA (mrtrix)"];

	  dtiproc_estimateresponse[label="estimateresponse (mrtrix)"];

	  dtiproc_csdeconv[label="csdeconv (mrtrix)"];

	  dtiproc_CSDstreamtrack[label="CSDstreamtrack (mrtrix)"];

	  dtiproc_tracks2prob[label="tracks2prob (mrtrix)"];

	  dtiproc_tck2trk[label="tck2trk (mrtrix)"];

	  dtiproc_outputnode[label="outputnode (utility)"];

	  dtiproc_inputnode -> dtiproc_tck2trk;

	  dtiproc_inputnode -> dtiproc_tracks2prob;

	  dtiproc_inputnode -> dtiproc_gen_WM_mask;

	  dtiproc_inputnode -> dtiproc_fsl2mrtrix;

	  dtiproc_inputnode -> dtiproc_fsl2mrtrix;

	  dtiproc_inputnode -> dtiproc_estimateresponse;

	  dtiproc_inputnode -> dtiproc_csdeconv;

	  dtiproc_inputnode -> dtiproc_dwi2tensor;

	  dtiproc_inputnode -> dtiproc_MRconvert;

	  dtiproc_inputnode -> dtiproc_bet;

	  dtiproc_bet -> dtiproc_gen_WM_mask;

	  dtiproc_fsl2mrtrix -> dtiproc_dwi2tensor;

	  dtiproc_fsl2mrtrix -> dtiproc_csdeconv;

	  dtiproc_fsl2mrtrix -> dtiproc_gen_WM_mask;

	  dtiproc_fsl2mrtrix -> dtiproc_estimateresponse;

	  dtiproc_MRconvert -> dtiproc_threshold_b0;

	  dtiproc_threshold_b0 -> dtiproc_median3D;

	  dtiproc_median3D -> dtiproc_erode_mask_firstpass;

	  dtiproc_erode_mask_firstpass -> dtiproc_erode_mask_secondpass;

	  dtiproc_erode_mask_secondpass -> dtiproc_MRmultiply_merge;

	  dtiproc_dwi2tensor -> dtiproc_tensor2vector;

	  dtiproc_dwi2tensor -> dtiproc_tensor2fa;

	  dtiproc_dwi2tensor -> dtiproc_tensor2adc;

	  dtiproc_gen_WM_mask -> dtiproc_threshold_wmmask;

	  dtiproc_gen_WM_mask -> dtiproc_csdeconv;

	  dtiproc_threshold_wmmask -> dtiproc_CSDstreamtrack;

	  dtiproc_tensor2fa -> dtiproc_MRmultiply_merge;

	  dtiproc_tensor2fa -> dtiproc_outputnode;

	  dtiproc_MRmultiply_merge -> dtiproc_MRmultiply;

	  dtiproc_MRmultiply -> dtiproc_threshold_FA;

	  dtiproc_threshold_FA -> dtiproc_estimateresponse;

	  dtiproc_estimateresponse -> dtiproc_csdeconv;

	  dtiproc_csdeconv -> dtiproc_CSDstreamtrack;

	  dtiproc_csdeconv -> dtiproc_outputnode;

	  dtiproc_CSDstreamtrack -> dtiproc_tracks2prob;

	  dtiproc_CSDstreamtrack -> dtiproc_tck2trk;

	  dtiproc_CSDstreamtrack -> dtiproc_outputnode;

	  dtiproc_tracks2prob -> dtiproc_outputnode;

	  dtiproc_tck2trk -> dtiproc_outputnode;

	}

