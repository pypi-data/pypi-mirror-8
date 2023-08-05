.. AUTO-GENERATED FILE -- DO NOT EDIT!

workflows.dmri.fsl.artifacts
============================


.. module:: nipype.workflows.dmri.fsl.artifacts


.. _nipype.workflows.dmri.fsl.artifacts.all_fmb_pipeline:

:func:`all_fmb_pipeline`
------------------------

`Link to code <http://github.com/nipy/nipype/tree/e63e055194d62d2bdc4665688261c03a42fd0025/nipype/workflows/dmri/fsl/artifacts.py#L15>`__



Builds a pipeline including three artifact corrections: head-motion
correction (HMC), susceptibility-derived distortion correction (SDC),
and Eddy currents-derived distortion correction (ECC).

The displacement fields from each kind of distortions are combined. Thus,
only one interpolation occurs between input data and result.

.. warning:: this workflow rotates the gradients table (*b*-vectors)
  [Leemans09]_.


Examples
~~~~~~~~

>>> from nipype.workflows.dmri.fsl.artifacts import all_fmb_pipeline
>>> allcorr = all_fmb_pipeline()
>>> allcorr.inputs.inputnode.in_file = 'epi.nii'
>>> allcorr.inputs.inputnode.in_bval = 'diffusion.bval'
>>> allcorr.inputs.inputnode.in_bvec = 'diffusion.bvec'
>>> allcorr.inputs.inputnode.bmap_mag = 'magnitude.nii'
>>> allcorr.inputs.inputnode.bmap_pha = 'phase.nii'
>>> allcorr.run() # doctest: +SKIP


Graph
~~~~~

.. graphviz::

	digraph hmc_sdc_ecc{

	  label="hmc_sdc_ecc";

	  hmc_sdc_ecc_inputnode[label="inputnode (utility)"];

	  hmc_sdc_ecc_b0_avg_pre[label="b0_avg_pre (utility)"];

	  hmc_sdc_ecc_bet_dwi_pre[label="bet_dwi_pre (fsl)"];

	  hmc_sdc_ecc_b0_avg_post[label="b0_avg_post (utility)"];

	  hmc_sdc_ecc_bet_dwi_post[label="bet_dwi_post (fsl)"];

	  hmc_sdc_ecc_outputnode[label="outputnode (utility)"];

	  hmc_sdc_ecc_inputnode -> hmc_sdc_ecc_b0_avg_pre;

	  hmc_sdc_ecc_inputnode -> hmc_sdc_ecc_b0_avg_pre;

	  hmc_sdc_ecc_inputnode -> hmc_sdc_ecc_b0_avg_post;

	  hmc_sdc_ecc_b0_avg_pre -> hmc_sdc_ecc_bet_dwi_pre;

	  subgraph cluster_hmc_sdc_ecc_motion_correct {

	      label="motion_correct";

	    hmc_sdc_ecc_motion_correct_inputnode[label="inputnode (utility)"];

	    hmc_sdc_ecc_motion_correct_SplitDWI[label="SplitDWI (utility)"];

	    hmc_sdc_ecc_motion_correct_InsertRefmat[label="InsertRefmat (utility)"];

	    hmc_sdc_ecc_motion_correct_Rotate_Bvec[label="Rotate_Bvec (utility)"];

	    hmc_sdc_ecc_motion_correct_outputnode[label="outputnode (utility)"];

	    hmc_sdc_ecc_motion_correct_inputnode -> hmc_sdc_ecc_motion_correct_SplitDWI;

	    hmc_sdc_ecc_motion_correct_inputnode -> hmc_sdc_ecc_motion_correct_SplitDWI;

	    hmc_sdc_ecc_motion_correct_inputnode -> hmc_sdc_ecc_motion_correct_SplitDWI;

	    hmc_sdc_ecc_motion_correct_inputnode -> hmc_sdc_ecc_motion_correct_Rotate_Bvec;

	    hmc_sdc_ecc_motion_correct_SplitDWI -> hmc_sdc_ecc_motion_correct_InsertRefmat;

	    subgraph cluster_hmc_sdc_ecc_motion_correct_DWICoregistration {

	            label="DWICoregistration";

	        hmc_sdc_ecc_motion_correct_DWICoregistration_inputnode[label="inputnode (utility)"];

	        hmc_sdc_ecc_motion_correct_DWICoregistration_Bias[label="Bias (ants)"];

	        hmc_sdc_ecc_motion_correct_DWICoregistration_MskDilate[label="MskDilate (fsl)"];

	        hmc_sdc_ecc_motion_correct_DWICoregistration_B0Equalize[label="B0Equalize (utility)"];

	        hmc_sdc_ecc_motion_correct_DWICoregistration_SplitDWIs[label="SplitDWIs (fsl)"];

	        hmc_sdc_ecc_motion_correct_DWICoregistration_DWEqualize[label="DWEqualize (utility)"];

	        hmc_sdc_ecc_motion_correct_DWICoregistration_InitXforms[label="InitXforms (utility)"];

	        hmc_sdc_ecc_motion_correct_DWICoregistration_CoRegistration[label="CoRegistration (fsl)"];

	        hmc_sdc_ecc_motion_correct_DWICoregistration_RemoveNegative[label="RemoveNegative (fsl)"];

	        hmc_sdc_ecc_motion_correct_DWICoregistration_MergeDWIs[label="MergeDWIs (fsl)"];

	        hmc_sdc_ecc_motion_correct_DWICoregistration_outputnode[label="outputnode (utility)"];

	        hmc_sdc_ecc_motion_correct_DWICoregistration_inputnode -> hmc_sdc_ecc_motion_correct_DWICoregistration_MskDilate;

	        hmc_sdc_ecc_motion_correct_DWICoregistration_inputnode -> hmc_sdc_ecc_motion_correct_DWICoregistration_InitXforms;

	        hmc_sdc_ecc_motion_correct_DWICoregistration_inputnode -> hmc_sdc_ecc_motion_correct_DWICoregistration_InitXforms;

	        hmc_sdc_ecc_motion_correct_DWICoregistration_inputnode -> hmc_sdc_ecc_motion_correct_DWICoregistration_SplitDWIs;

	        hmc_sdc_ecc_motion_correct_DWICoregistration_inputnode -> hmc_sdc_ecc_motion_correct_DWICoregistration_Bias;

	        hmc_sdc_ecc_motion_correct_DWICoregistration_inputnode -> hmc_sdc_ecc_motion_correct_DWICoregistration_Bias;

	        hmc_sdc_ecc_motion_correct_DWICoregistration_inputnode -> hmc_sdc_ecc_motion_correct_DWICoregistration_B0Equalize;

	        hmc_sdc_ecc_motion_correct_DWICoregistration_Bias -> hmc_sdc_ecc_motion_correct_DWICoregistration_B0Equalize;

	        hmc_sdc_ecc_motion_correct_DWICoregistration_MskDilate -> hmc_sdc_ecc_motion_correct_DWICoregistration_DWEqualize;

	        hmc_sdc_ecc_motion_correct_DWICoregistration_MskDilate -> hmc_sdc_ecc_motion_correct_DWICoregistration_CoRegistration;

	        hmc_sdc_ecc_motion_correct_DWICoregistration_MskDilate -> hmc_sdc_ecc_motion_correct_DWICoregistration_CoRegistration;

	        hmc_sdc_ecc_motion_correct_DWICoregistration_B0Equalize -> hmc_sdc_ecc_motion_correct_DWICoregistration_CoRegistration;

	        hmc_sdc_ecc_motion_correct_DWICoregistration_SplitDWIs -> hmc_sdc_ecc_motion_correct_DWICoregistration_DWEqualize;

	        hmc_sdc_ecc_motion_correct_DWICoregistration_DWEqualize -> hmc_sdc_ecc_motion_correct_DWICoregistration_CoRegistration;

	        hmc_sdc_ecc_motion_correct_DWICoregistration_InitXforms -> hmc_sdc_ecc_motion_correct_DWICoregistration_CoRegistration;

	        hmc_sdc_ecc_motion_correct_DWICoregistration_CoRegistration -> hmc_sdc_ecc_motion_correct_DWICoregistration_outputnode;

	        hmc_sdc_ecc_motion_correct_DWICoregistration_CoRegistration -> hmc_sdc_ecc_motion_correct_DWICoregistration_RemoveNegative;

	        hmc_sdc_ecc_motion_correct_DWICoregistration_RemoveNegative -> hmc_sdc_ecc_motion_correct_DWICoregistration_MergeDWIs;

	        hmc_sdc_ecc_motion_correct_DWICoregistration_MergeDWIs -> hmc_sdc_ecc_motion_correct_DWICoregistration_outputnode;

	    }

	    hmc_sdc_ecc_motion_correct_InsertRefmat -> hmc_sdc_ecc_motion_correct_Rotate_Bvec;

	    hmc_sdc_ecc_motion_correct_InsertRefmat -> hmc_sdc_ecc_motion_correct_outputnode;

	    hmc_sdc_ecc_motion_correct_Rotate_Bvec -> hmc_sdc_ecc_motion_correct_outputnode;

	    hmc_sdc_ecc_motion_correct_DWICoregistration_outputnode -> hmc_sdc_ecc_motion_correct_InsertRefmat;

	    hmc_sdc_ecc_motion_correct_DWICoregistration_outputnode -> hmc_sdc_ecc_motion_correct_outputnode;

	    hmc_sdc_ecc_motion_correct_inputnode -> hmc_sdc_ecc_motion_correct_DWICoregistration_inputnode;

	    hmc_sdc_ecc_motion_correct_SplitDWI -> hmc_sdc_ecc_motion_correct_DWICoregistration_inputnode;

	    hmc_sdc_ecc_motion_correct_SplitDWI -> hmc_sdc_ecc_motion_correct_DWICoregistration_inputnode;

	    hmc_sdc_ecc_motion_correct_SplitDWI -> hmc_sdc_ecc_motion_correct_DWICoregistration_inputnode;

	  }

	  subgraph cluster_hmc_sdc_ecc_eddy_correct {

	      label="eddy_correct";

	    hmc_sdc_ecc_eddy_correct_inputnode[label="inputnode (utility)"];

	    hmc_sdc_ecc_eddy_correct_ExtractDWI[label="ExtractDWI (utility)"];

	    hmc_sdc_ecc_eddy_correct_b0_avg[label="b0_avg (utility)"];

	    hmc_sdc_ecc_eddy_correct_GatherMatrices[label="GatherMatrices (utility)"];

	    hmc_sdc_ecc_eddy_correct_SplitDWIs[label="SplitDWIs (fsl)"];

	    hmc_sdc_ecc_eddy_correct_ModulateDWIs[label="ModulateDWIs (fsl)"];

	    hmc_sdc_ecc_eddy_correct_RemoveNegative[label="RemoveNegative (fsl)"];

	    hmc_sdc_ecc_eddy_correct_MergeDWIs[label="MergeDWIs (utility)"];

	    hmc_sdc_ecc_eddy_correct_outputnode[label="outputnode (utility)"];

	    hmc_sdc_ecc_eddy_correct_inputnode -> hmc_sdc_ecc_eddy_correct_b0_avg;

	    hmc_sdc_ecc_eddy_correct_inputnode -> hmc_sdc_ecc_eddy_correct_b0_avg;

	    hmc_sdc_ecc_eddy_correct_inputnode -> hmc_sdc_ecc_eddy_correct_GatherMatrices;

	    hmc_sdc_ecc_eddy_correct_inputnode -> hmc_sdc_ecc_eddy_correct_MergeDWIs;

	    hmc_sdc_ecc_eddy_correct_inputnode -> hmc_sdc_ecc_eddy_correct_MergeDWIs;

	    hmc_sdc_ecc_eddy_correct_inputnode -> hmc_sdc_ecc_eddy_correct_ExtractDWI;

	    hmc_sdc_ecc_eddy_correct_inputnode -> hmc_sdc_ecc_eddy_correct_ExtractDWI;

	    subgraph cluster_hmc_sdc_ecc_eddy_correct_DWICoregistration {

	            label="DWICoregistration";

	        hmc_sdc_ecc_eddy_correct_DWICoregistration_inputnode[label="inputnode (utility)"];

	        hmc_sdc_ecc_eddy_correct_DWICoregistration_MskDilate[label="MskDilate (fsl)"];

	        hmc_sdc_ecc_eddy_correct_DWICoregistration_Bias[label="Bias (ants)"];

	        hmc_sdc_ecc_eddy_correct_DWICoregistration_SplitDWIs[label="SplitDWIs (fsl)"];

	        hmc_sdc_ecc_eddy_correct_DWICoregistration_DWEqualize[label="DWEqualize (utility)"];

	        hmc_sdc_ecc_eddy_correct_DWICoregistration_InitXforms[label="InitXforms (utility)"];

	        hmc_sdc_ecc_eddy_correct_DWICoregistration_B0Equalize[label="B0Equalize (utility)"];

	        hmc_sdc_ecc_eddy_correct_DWICoregistration_CoRegistration[label="CoRegistration (fsl)"];

	        hmc_sdc_ecc_eddy_correct_DWICoregistration_RemoveNegative[label="RemoveNegative (fsl)"];

	        hmc_sdc_ecc_eddy_correct_DWICoregistration_MergeDWIs[label="MergeDWIs (fsl)"];

	        hmc_sdc_ecc_eddy_correct_DWICoregistration_outputnode[label="outputnode (utility)"];

	        hmc_sdc_ecc_eddy_correct_DWICoregistration_inputnode -> hmc_sdc_ecc_eddy_correct_DWICoregistration_SplitDWIs;

	        hmc_sdc_ecc_eddy_correct_DWICoregistration_inputnode -> hmc_sdc_ecc_eddy_correct_DWICoregistration_Bias;

	        hmc_sdc_ecc_eddy_correct_DWICoregistration_inputnode -> hmc_sdc_ecc_eddy_correct_DWICoregistration_Bias;

	        hmc_sdc_ecc_eddy_correct_DWICoregistration_inputnode -> hmc_sdc_ecc_eddy_correct_DWICoregistration_InitXforms;

	        hmc_sdc_ecc_eddy_correct_DWICoregistration_inputnode -> hmc_sdc_ecc_eddy_correct_DWICoregistration_InitXforms;

	        hmc_sdc_ecc_eddy_correct_DWICoregistration_inputnode -> hmc_sdc_ecc_eddy_correct_DWICoregistration_B0Equalize;

	        hmc_sdc_ecc_eddy_correct_DWICoregistration_inputnode -> hmc_sdc_ecc_eddy_correct_DWICoregistration_MskDilate;

	        hmc_sdc_ecc_eddy_correct_DWICoregistration_MskDilate -> hmc_sdc_ecc_eddy_correct_DWICoregistration_CoRegistration;

	        hmc_sdc_ecc_eddy_correct_DWICoregistration_MskDilate -> hmc_sdc_ecc_eddy_correct_DWICoregistration_CoRegistration;

	        hmc_sdc_ecc_eddy_correct_DWICoregistration_MskDilate -> hmc_sdc_ecc_eddy_correct_DWICoregistration_DWEqualize;

	        hmc_sdc_ecc_eddy_correct_DWICoregistration_Bias -> hmc_sdc_ecc_eddy_correct_DWICoregistration_B0Equalize;

	        hmc_sdc_ecc_eddy_correct_DWICoregistration_SplitDWIs -> hmc_sdc_ecc_eddy_correct_DWICoregistration_DWEqualize;

	        hmc_sdc_ecc_eddy_correct_DWICoregistration_DWEqualize -> hmc_sdc_ecc_eddy_correct_DWICoregistration_CoRegistration;

	        hmc_sdc_ecc_eddy_correct_DWICoregistration_InitXforms -> hmc_sdc_ecc_eddy_correct_DWICoregistration_CoRegistration;

	        hmc_sdc_ecc_eddy_correct_DWICoregistration_B0Equalize -> hmc_sdc_ecc_eddy_correct_DWICoregistration_CoRegistration;

	        hmc_sdc_ecc_eddy_correct_DWICoregistration_CoRegistration -> hmc_sdc_ecc_eddy_correct_DWICoregistration_RemoveNegative;

	        hmc_sdc_ecc_eddy_correct_DWICoregistration_CoRegistration -> hmc_sdc_ecc_eddy_correct_DWICoregistration_outputnode;

	        hmc_sdc_ecc_eddy_correct_DWICoregistration_RemoveNegative -> hmc_sdc_ecc_eddy_correct_DWICoregistration_MergeDWIs;

	        hmc_sdc_ecc_eddy_correct_DWICoregistration_MergeDWIs -> hmc_sdc_ecc_eddy_correct_DWICoregistration_outputnode;

	    }

	    hmc_sdc_ecc_eddy_correct_GatherMatrices -> hmc_sdc_ecc_eddy_correct_outputnode;

	    hmc_sdc_ecc_eddy_correct_SplitDWIs -> hmc_sdc_ecc_eddy_correct_ModulateDWIs;

	    hmc_sdc_ecc_eddy_correct_ModulateDWIs -> hmc_sdc_ecc_eddy_correct_RemoveNegative;

	    hmc_sdc_ecc_eddy_correct_RemoveNegative -> hmc_sdc_ecc_eddy_correct_MergeDWIs;

	    hmc_sdc_ecc_eddy_correct_MergeDWIs -> hmc_sdc_ecc_eddy_correct_outputnode;

	    hmc_sdc_ecc_eddy_correct_b0_avg -> hmc_sdc_ecc_eddy_correct_DWICoregistration_inputnode;

	    hmc_sdc_ecc_eddy_correct_inputnode -> hmc_sdc_ecc_eddy_correct_DWICoregistration_inputnode;

	    hmc_sdc_ecc_eddy_correct_inputnode -> hmc_sdc_ecc_eddy_correct_DWICoregistration_inputnode;

	    hmc_sdc_ecc_eddy_correct_inputnode -> hmc_sdc_ecc_eddy_correct_DWICoregistration_inputnode;

	    hmc_sdc_ecc_eddy_correct_ExtractDWI -> hmc_sdc_ecc_eddy_correct_DWICoregistration_inputnode;

	    hmc_sdc_ecc_eddy_correct_DWICoregistration_outputnode -> hmc_sdc_ecc_eddy_correct_GatherMatrices;

	    hmc_sdc_ecc_eddy_correct_DWICoregistration_outputnode -> hmc_sdc_ecc_eddy_correct_SplitDWIs;

	    hmc_sdc_ecc_eddy_correct_DWICoregistration_outputnode -> hmc_sdc_ecc_eddy_correct_ModulateDWIs;

	  }

	  hmc_sdc_ecc_b0_avg_post -> hmc_sdc_ecc_bet_dwi_post;

	  hmc_sdc_ecc_bet_dwi_post -> hmc_sdc_ecc_outputnode;

	  subgraph cluster_hmc_sdc_ecc_fmb_correction {

	      label="fmb_correction";

	    hmc_sdc_ecc_fmb_correction_inputnode[label="inputnode (utility)"];

	    hmc_sdc_ecc_fmb_correction_PreparePhase[label="PreparePhase (utility)"];

	    hmc_sdc_ecc_fmb_correction_GetFirst[label="GetFirst (fsl)"];

	    hmc_sdc_ecc_fmb_correction_Bias[label="Bias (ants)"];

	    hmc_sdc_ecc_fmb_correction_b0_avg[label="b0_avg (utility)"];

	    hmc_sdc_ecc_fmb_correction_SplitDWIs[label="SplitDWIs (fsl)"];

	    hmc_sdc_ecc_fmb_correction_BrainExtraction[label="BrainExtraction (fsl)"];

	    hmc_sdc_ecc_fmb_correction_MskDilate[label="MskDilate (fsl)"];

	    hmc_sdc_ecc_fmb_correction_PhaseUnwrap[label="PhaseUnwrap (fsl)"];

	    hmc_sdc_ecc_fmb_correction_ToRadSec[label="ToRadSec (utility)"];

	    hmc_sdc_ecc_fmb_correction_BmapMag2B0[label="BmapMag2B0 (fsl)"];

	    hmc_sdc_ecc_fmb_correction_BmapPha2B0[label="BmapPha2B0 (fsl)"];

	    hmc_sdc_ecc_fmb_correction_PreliminaryFugue[label="PreliminaryFugue (fsl)"];

	    hmc_sdc_ecc_fmb_correction_DemeanFmap[label="DemeanFmap (utility)"];

	    hmc_sdc_ecc_fmb_correction_AddEmptyVol[label="AddEmptyVol (utility)"];

	    hmc_sdc_ecc_fmb_correction_ComputeVSM[label="ComputeVSM (fsl)"];

	    hmc_sdc_ecc_fmb_correction_UnwarpDWIs[label="UnwarpDWIs (fsl)"];

	    hmc_sdc_ecc_fmb_correction_RemoveNegative[label="RemoveNegative (fsl)"];

	    hmc_sdc_ecc_fmb_correction_MergeDWIs[label="MergeDWIs (fsl)"];

	    hmc_sdc_ecc_fmb_correction_outputnode[label="outputnode (utility)"];

	    hmc_sdc_ecc_fmb_correction_inputnode -> hmc_sdc_ecc_fmb_correction_DemeanFmap;

	    hmc_sdc_ecc_fmb_correction_inputnode -> hmc_sdc_ecc_fmb_correction_SplitDWIs;

	    hmc_sdc_ecc_fmb_correction_inputnode -> hmc_sdc_ecc_fmb_correction_PreparePhase;

	    hmc_sdc_ecc_fmb_correction_inputnode -> hmc_sdc_ecc_fmb_correction_ComputeVSM;

	    hmc_sdc_ecc_fmb_correction_inputnode -> hmc_sdc_ecc_fmb_correction_PreliminaryFugue;

	    hmc_sdc_ecc_fmb_correction_inputnode -> hmc_sdc_ecc_fmb_correction_GetFirst;

	    hmc_sdc_ecc_fmb_correction_inputnode -> hmc_sdc_ecc_fmb_correction_BmapMag2B0;

	    hmc_sdc_ecc_fmb_correction_inputnode -> hmc_sdc_ecc_fmb_correction_b0_avg;

	    hmc_sdc_ecc_fmb_correction_inputnode -> hmc_sdc_ecc_fmb_correction_b0_avg;

	    hmc_sdc_ecc_fmb_correction_PreparePhase -> hmc_sdc_ecc_fmb_correction_PhaseUnwrap;

	    hmc_sdc_ecc_fmb_correction_GetFirst -> hmc_sdc_ecc_fmb_correction_Bias;

	    hmc_sdc_ecc_fmb_correction_Bias -> hmc_sdc_ecc_fmb_correction_BrainExtraction;

	    hmc_sdc_ecc_fmb_correction_Bias -> hmc_sdc_ecc_fmb_correction_BmapMag2B0;

	    hmc_sdc_ecc_fmb_correction_Bias -> hmc_sdc_ecc_fmb_correction_PhaseUnwrap;

	    hmc_sdc_ecc_fmb_correction_b0_avg -> hmc_sdc_ecc_fmb_correction_BmapMag2B0;

	    hmc_sdc_ecc_fmb_correction_b0_avg -> hmc_sdc_ecc_fmb_correction_BmapPha2B0;

	    hmc_sdc_ecc_fmb_correction_SplitDWIs -> hmc_sdc_ecc_fmb_correction_UnwarpDWIs;

	    hmc_sdc_ecc_fmb_correction_BrainExtraction -> hmc_sdc_ecc_fmb_correction_MskDilate;

	    hmc_sdc_ecc_fmb_correction_MskDilate -> hmc_sdc_ecc_fmb_correction_PhaseUnwrap;

	    hmc_sdc_ecc_fmb_correction_MskDilate -> hmc_sdc_ecc_fmb_correction_BmapMag2B0;

	    hmc_sdc_ecc_fmb_correction_PhaseUnwrap -> hmc_sdc_ecc_fmb_correction_ToRadSec;

	    hmc_sdc_ecc_fmb_correction_ToRadSec -> hmc_sdc_ecc_fmb_correction_BmapPha2B0;

	    hmc_sdc_ecc_fmb_correction_BmapMag2B0 -> hmc_sdc_ecc_fmb_correction_BmapPha2B0;

	    hmc_sdc_ecc_fmb_correction_BmapPha2B0 -> hmc_sdc_ecc_fmb_correction_PreliminaryFugue;

	    hmc_sdc_ecc_fmb_correction_PreliminaryFugue -> hmc_sdc_ecc_fmb_correction_DemeanFmap;

	    subgraph cluster_hmc_sdc_ecc_fmb_correction_Cleanup {

	            label="Cleanup";

	        hmc_sdc_ecc_fmb_correction_Cleanup_inputnode[label="inputnode (utility)"];

	        hmc_sdc_ecc_fmb_correction_Cleanup_Despike[label="Despike (fsl)"];

	        hmc_sdc_ecc_fmb_correction_Cleanup_MskErode[label="MskErode (fsl)"];

	        hmc_sdc_ecc_fmb_correction_Cleanup_NewMask[label="NewMask (fsl)"];

	        hmc_sdc_ecc_fmb_correction_Cleanup_ApplyMask[label="ApplyMask (fsl)"];

	        hmc_sdc_ecc_fmb_correction_Cleanup_Merge[label="Merge (utility)"];

	        hmc_sdc_ecc_fmb_correction_Cleanup_AddEdge[label="AddEdge (fsl)"];

	        hmc_sdc_ecc_fmb_correction_Cleanup_outputnode[label="outputnode (utility)"];

	        hmc_sdc_ecc_fmb_correction_Cleanup_inputnode -> hmc_sdc_ecc_fmb_correction_Cleanup_MskErode;

	        hmc_sdc_ecc_fmb_correction_Cleanup_inputnode -> hmc_sdc_ecc_fmb_correction_Cleanup_AddEdge;

	        hmc_sdc_ecc_fmb_correction_Cleanup_inputnode -> hmc_sdc_ecc_fmb_correction_Cleanup_Despike;

	        hmc_sdc_ecc_fmb_correction_Cleanup_inputnode -> hmc_sdc_ecc_fmb_correction_Cleanup_Despike;

	        hmc_sdc_ecc_fmb_correction_Cleanup_inputnode -> hmc_sdc_ecc_fmb_correction_Cleanup_NewMask;

	        hmc_sdc_ecc_fmb_correction_Cleanup_Despike -> hmc_sdc_ecc_fmb_correction_Cleanup_ApplyMask;

	        hmc_sdc_ecc_fmb_correction_Cleanup_MskErode -> hmc_sdc_ecc_fmb_correction_Cleanup_Merge;

	        hmc_sdc_ecc_fmb_correction_Cleanup_MskErode -> hmc_sdc_ecc_fmb_correction_Cleanup_NewMask;

	        hmc_sdc_ecc_fmb_correction_Cleanup_NewMask -> hmc_sdc_ecc_fmb_correction_Cleanup_ApplyMask;

	        hmc_sdc_ecc_fmb_correction_Cleanup_ApplyMask -> hmc_sdc_ecc_fmb_correction_Cleanup_Merge;

	        hmc_sdc_ecc_fmb_correction_Cleanup_Merge -> hmc_sdc_ecc_fmb_correction_Cleanup_AddEdge;

	        hmc_sdc_ecc_fmb_correction_Cleanup_AddEdge -> hmc_sdc_ecc_fmb_correction_Cleanup_outputnode;

	    }

	    hmc_sdc_ecc_fmb_correction_AddEmptyVol -> hmc_sdc_ecc_fmb_correction_ComputeVSM;

	    hmc_sdc_ecc_fmb_correction_ComputeVSM -> hmc_sdc_ecc_fmb_correction_outputnode;

	    hmc_sdc_ecc_fmb_correction_ComputeVSM -> hmc_sdc_ecc_fmb_correction_UnwarpDWIs;

	    hmc_sdc_ecc_fmb_correction_UnwarpDWIs -> hmc_sdc_ecc_fmb_correction_RemoveNegative;

	    hmc_sdc_ecc_fmb_correction_RemoveNegative -> hmc_sdc_ecc_fmb_correction_MergeDWIs;

	    hmc_sdc_ecc_fmb_correction_MergeDWIs -> hmc_sdc_ecc_fmb_correction_outputnode;

	    subgraph cluster_hmc_sdc_ecc_fmb_correction_Shiftmap2Warping {

	            label="Shiftmap2Warping";

	        hmc_sdc_ecc_fmb_correction_Shiftmap2Warping_inputnode[label="inputnode (utility)"];

	        hmc_sdc_ecc_fmb_correction_Shiftmap2Warping_Fix_hdr[label="Fix_hdr (utility)"];

	        hmc_sdc_ecc_fmb_correction_Shiftmap2Warping_ScaleField[label="ScaleField (fsl)"];

	        hmc_sdc_ecc_fmb_correction_Shiftmap2Warping_vsm2dfm[label="vsm2dfm (fsl)"];

	        hmc_sdc_ecc_fmb_correction_Shiftmap2Warping_outputnode[label="outputnode (utility)"];

	        hmc_sdc_ecc_fmb_correction_Shiftmap2Warping_inputnode -> hmc_sdc_ecc_fmb_correction_Shiftmap2Warping_vsm2dfm;

	        hmc_sdc_ecc_fmb_correction_Shiftmap2Warping_inputnode -> hmc_sdc_ecc_fmb_correction_Shiftmap2Warping_vsm2dfm;

	        hmc_sdc_ecc_fmb_correction_Shiftmap2Warping_inputnode -> hmc_sdc_ecc_fmb_correction_Shiftmap2Warping_Fix_hdr;

	        hmc_sdc_ecc_fmb_correction_Shiftmap2Warping_inputnode -> hmc_sdc_ecc_fmb_correction_Shiftmap2Warping_Fix_hdr;

	        hmc_sdc_ecc_fmb_correction_Shiftmap2Warping_inputnode -> hmc_sdc_ecc_fmb_correction_Shiftmap2Warping_ScaleField;

	        hmc_sdc_ecc_fmb_correction_Shiftmap2Warping_Fix_hdr -> hmc_sdc_ecc_fmb_correction_Shiftmap2Warping_ScaleField;

	        hmc_sdc_ecc_fmb_correction_Shiftmap2Warping_ScaleField -> hmc_sdc_ecc_fmb_correction_Shiftmap2Warping_vsm2dfm;

	        hmc_sdc_ecc_fmb_correction_Shiftmap2Warping_vsm2dfm -> hmc_sdc_ecc_fmb_correction_Shiftmap2Warping_outputnode;

	    }

	    hmc_sdc_ecc_fmb_correction_ComputeVSM -> hmc_sdc_ecc_fmb_correction_Shiftmap2Warping_inputnode;

	    hmc_sdc_ecc_fmb_correction_Cleanup_outputnode -> hmc_sdc_ecc_fmb_correction_AddEmptyVol;

	    hmc_sdc_ecc_fmb_correction_inputnode -> hmc_sdc_ecc_fmb_correction_Cleanup_inputnode;

	    hmc_sdc_ecc_fmb_correction_MergeDWIs -> hmc_sdc_ecc_fmb_correction_Shiftmap2Warping_inputnode;

	    hmc_sdc_ecc_fmb_correction_DemeanFmap -> hmc_sdc_ecc_fmb_correction_Cleanup_inputnode;

	    hmc_sdc_ecc_fmb_correction_Shiftmap2Warping_outputnode -> hmc_sdc_ecc_fmb_correction_outputnode;

	  }

	  subgraph cluster_hmc_sdc_ecc_UnwarpArtifacts {

	      label="UnwarpArtifacts";

	    hmc_sdc_ecc_UnwarpArtifacts_inputnode[label="inputnode (utility)"];

	    hmc_sdc_ecc_UnwarpArtifacts_SplitDWIs[label="SplitDWIs (fsl)"];

	    hmc_sdc_ecc_UnwarpArtifacts_Reference[label="Reference (utility)"];

	    hmc_sdc_ecc_UnwarpArtifacts_ConvertWarp[label="ConvertWarp (fsl)"];

	    hmc_sdc_ecc_UnwarpArtifacts_CoeffComp[label="CoeffComp (fsl)"];

	    hmc_sdc_ecc_UnwarpArtifacts_JacobianComp[label="JacobianComp (fsl)"];

	    hmc_sdc_ecc_UnwarpArtifacts_UnwarpDWIs[label="UnwarpDWIs (fsl)"];

	    hmc_sdc_ecc_UnwarpArtifacts_ModulateDWIs[label="ModulateDWIs (fsl)"];

	    hmc_sdc_ecc_UnwarpArtifacts_RemoveNegative[label="RemoveNegative (fsl)"];

	    hmc_sdc_ecc_UnwarpArtifacts_MergeDWIs[label="MergeDWIs (fsl)"];

	    hmc_sdc_ecc_UnwarpArtifacts_outputnode[label="outputnode (utility)"];

	    hmc_sdc_ecc_UnwarpArtifacts_inputnode -> hmc_sdc_ecc_UnwarpArtifacts_ConvertWarp;

	    hmc_sdc_ecc_UnwarpArtifacts_inputnode -> hmc_sdc_ecc_UnwarpArtifacts_ConvertWarp;

	    hmc_sdc_ecc_UnwarpArtifacts_inputnode -> hmc_sdc_ecc_UnwarpArtifacts_ConvertWarp;

	    hmc_sdc_ecc_UnwarpArtifacts_inputnode -> hmc_sdc_ecc_UnwarpArtifacts_ConvertWarp;

	    hmc_sdc_ecc_UnwarpArtifacts_inputnode -> hmc_sdc_ecc_UnwarpArtifacts_SplitDWIs;

	    hmc_sdc_ecc_UnwarpArtifacts_SplitDWIs -> hmc_sdc_ecc_UnwarpArtifacts_Reference;

	    hmc_sdc_ecc_UnwarpArtifacts_SplitDWIs -> hmc_sdc_ecc_UnwarpArtifacts_UnwarpDWIs;

	    hmc_sdc_ecc_UnwarpArtifacts_Reference -> hmc_sdc_ecc_UnwarpArtifacts_CoeffComp;

	    hmc_sdc_ecc_UnwarpArtifacts_Reference -> hmc_sdc_ecc_UnwarpArtifacts_UnwarpDWIs;

	    hmc_sdc_ecc_UnwarpArtifacts_Reference -> hmc_sdc_ecc_UnwarpArtifacts_JacobianComp;

	    hmc_sdc_ecc_UnwarpArtifacts_ConvertWarp -> hmc_sdc_ecc_UnwarpArtifacts_CoeffComp;

	    hmc_sdc_ecc_UnwarpArtifacts_ConvertWarp -> hmc_sdc_ecc_UnwarpArtifacts_UnwarpDWIs;

	    hmc_sdc_ecc_UnwarpArtifacts_ConvertWarp -> hmc_sdc_ecc_UnwarpArtifacts_outputnode;

	    hmc_sdc_ecc_UnwarpArtifacts_CoeffComp -> hmc_sdc_ecc_UnwarpArtifacts_JacobianComp;

	    hmc_sdc_ecc_UnwarpArtifacts_CoeffComp -> hmc_sdc_ecc_UnwarpArtifacts_outputnode;

	    hmc_sdc_ecc_UnwarpArtifacts_JacobianComp -> hmc_sdc_ecc_UnwarpArtifacts_ModulateDWIs;

	    hmc_sdc_ecc_UnwarpArtifacts_JacobianComp -> hmc_sdc_ecc_UnwarpArtifacts_outputnode;

	    hmc_sdc_ecc_UnwarpArtifacts_UnwarpDWIs -> hmc_sdc_ecc_UnwarpArtifacts_ModulateDWIs;

	    hmc_sdc_ecc_UnwarpArtifacts_ModulateDWIs -> hmc_sdc_ecc_UnwarpArtifacts_RemoveNegative;

	    hmc_sdc_ecc_UnwarpArtifacts_RemoveNegative -> hmc_sdc_ecc_UnwarpArtifacts_MergeDWIs;

	    hmc_sdc_ecc_UnwarpArtifacts_MergeDWIs -> hmc_sdc_ecc_UnwarpArtifacts_outputnode;

	  }

	  hmc_sdc_ecc_motion_correct_outputnode -> hmc_sdc_ecc_UnwarpArtifacts_inputnode;

	  hmc_sdc_ecc_motion_correct_outputnode -> hmc_sdc_ecc_fmb_correction_inputnode;

	  hmc_sdc_ecc_motion_correct_outputnode -> hmc_sdc_ecc_outputnode;

	  hmc_sdc_ecc_motion_correct_outputnode -> hmc_sdc_ecc_eddy_correct_inputnode;

	  hmc_sdc_ecc_eddy_correct_outputnode -> hmc_sdc_ecc_b0_avg_post;

	  hmc_sdc_ecc_eddy_correct_outputnode -> hmc_sdc_ecc_UnwarpArtifacts_inputnode;

	  hmc_sdc_ecc_fmb_correction_outputnode -> hmc_sdc_ecc_UnwarpArtifacts_inputnode;

	  hmc_sdc_ecc_UnwarpArtifacts_outputnode -> hmc_sdc_ecc_outputnode;

	  hmc_sdc_ecc_bet_dwi_pre -> hmc_sdc_ecc_eddy_correct_inputnode;

	  hmc_sdc_ecc_bet_dwi_pre -> hmc_sdc_ecc_motion_correct_inputnode;

	  hmc_sdc_ecc_bet_dwi_pre -> hmc_sdc_ecc_fmb_correction_inputnode;

	  hmc_sdc_ecc_inputnode -> hmc_sdc_ecc_UnwarpArtifacts_inputnode;

	  hmc_sdc_ecc_inputnode -> hmc_sdc_ecc_eddy_correct_inputnode;

	  hmc_sdc_ecc_inputnode -> hmc_sdc_ecc_eddy_correct_inputnode;

	  hmc_sdc_ecc_inputnode -> hmc_sdc_ecc_motion_correct_inputnode;

	  hmc_sdc_ecc_inputnode -> hmc_sdc_ecc_motion_correct_inputnode;

	  hmc_sdc_ecc_inputnode -> hmc_sdc_ecc_motion_correct_inputnode;

	  hmc_sdc_ecc_inputnode -> hmc_sdc_ecc_fmb_correction_inputnode;

	  hmc_sdc_ecc_inputnode -> hmc_sdc_ecc_fmb_correction_inputnode;

	  hmc_sdc_ecc_inputnode -> hmc_sdc_ecc_fmb_correction_inputnode;

	}


.. _nipype.workflows.dmri.fsl.artifacts.all_fsl_pipeline:

:func:`all_fsl_pipeline`
------------------------

`Link to code <http://github.com/nipy/nipype/tree/e63e055194d62d2bdc4665688261c03a42fd0025/nipype/workflows/dmri/fsl/artifacts.py#L184>`__



Workflow that integrates FSL ``topup`` and ``eddy``.


.. warning:: this workflow rotates the gradients table (*b*-vectors)
  [Leemans09]_.


.. warning:: this workflow does not perform jacobian modulation of each
  *DWI* [Jones10]_.


Examples
~~~~~~~~

>>> from nipype.workflows.dmri.fsl.artifacts import all_fsl_pipeline
>>> allcorr = all_fsl_pipeline()
>>> allcorr.inputs.inputnode.in_file = 'epi.nii'
>>> allcorr.inputs.inputnode.alt_file = 'epi_rev.nii'
>>> allcorr.inputs.inputnode.in_bval = 'diffusion.bval'
>>> allcorr.inputs.inputnode.in_bvec = 'diffusion.bvec'
>>> allcorr.run() # doctest: +SKIP


Graph
~~~~~

.. graphviz::

	digraph fsl_all_correct{

	  label="fsl_all_correct";

	  fsl_all_correct_inputnode[label="inputnode (utility)"];

	  fsl_all_correct_b0_avg_pre[label="b0_avg_pre (utility)"];

	  fsl_all_correct_bet_dwi_pre[label="bet_dwi_pre (fsl)"];

	  fsl_all_correct_fsl_eddy[label="fsl_eddy (fsl)"];

	  fsl_all_correct_b0_avg_post[label="b0_avg_post (utility)"];

	  fsl_all_correct_bet_dwi_post[label="bet_dwi_post (fsl)"];

	  fsl_all_correct_Rotate_Bvec[label="Rotate_Bvec (utility)"];

	  fsl_all_correct_outputnode[label="outputnode (utility)"];

	  fsl_all_correct_inputnode -> fsl_all_correct_Rotate_Bvec;

	  fsl_all_correct_inputnode -> fsl_all_correct_fsl_eddy;

	  fsl_all_correct_inputnode -> fsl_all_correct_fsl_eddy;

	  fsl_all_correct_inputnode -> fsl_all_correct_fsl_eddy;

	  fsl_all_correct_inputnode -> fsl_all_correct_fsl_eddy;

	  fsl_all_correct_inputnode -> fsl_all_correct_b0_avg_post;

	  fsl_all_correct_inputnode -> fsl_all_correct_b0_avg_pre;

	  fsl_all_correct_inputnode -> fsl_all_correct_b0_avg_pre;

	  fsl_all_correct_b0_avg_pre -> fsl_all_correct_bet_dwi_pre;

	  fsl_all_correct_bet_dwi_pre -> fsl_all_correct_fsl_eddy;

	  subgraph cluster_fsl_all_correct_peb_correction {

	      label="peb_correction";

	    fsl_all_correct_peb_correction_inputnode[label="inputnode (utility)"];

	    fsl_all_correct_peb_correction_b0_ref[label="b0_ref (fsl)"];

	    fsl_all_correct_peb_correction_b0_alt[label="b0_alt (fsl)"];

	    fsl_all_correct_peb_correction_b0_list[label="b0_list (utility)"];

	    fsl_all_correct_peb_correction_b0_merged[label="b0_merged (fsl)"];

	    fsl_all_correct_peb_correction_topup[label="topup (fsl)"];

	    fsl_all_correct_peb_correction_unwarp[label="unwarp (fsl)"];

	    fsl_all_correct_peb_correction_outputnode[label="outputnode (utility)"];

	    fsl_all_correct_peb_correction_inputnode -> fsl_all_correct_peb_correction_b0_ref;

	    fsl_all_correct_peb_correction_inputnode -> fsl_all_correct_peb_correction_b0_ref;

	    fsl_all_correct_peb_correction_inputnode -> fsl_all_correct_peb_correction_b0_alt;

	    fsl_all_correct_peb_correction_inputnode -> fsl_all_correct_peb_correction_b0_alt;

	    fsl_all_correct_peb_correction_inputnode -> fsl_all_correct_peb_correction_unwarp;

	    fsl_all_correct_peb_correction_b0_ref -> fsl_all_correct_peb_correction_b0_list;

	    fsl_all_correct_peb_correction_b0_alt -> fsl_all_correct_peb_correction_b0_list;

	    fsl_all_correct_peb_correction_b0_list -> fsl_all_correct_peb_correction_b0_merged;

	    fsl_all_correct_peb_correction_b0_merged -> fsl_all_correct_peb_correction_topup;

	    fsl_all_correct_peb_correction_topup -> fsl_all_correct_peb_correction_unwarp;

	    fsl_all_correct_peb_correction_topup -> fsl_all_correct_peb_correction_unwarp;

	    fsl_all_correct_peb_correction_topup -> fsl_all_correct_peb_correction_unwarp;

	    fsl_all_correct_peb_correction_topup -> fsl_all_correct_peb_correction_outputnode;

	    subgraph cluster_fsl_all_correct_peb_correction_Shiftmap2Warping {

	            label="Shiftmap2Warping";

	        fsl_all_correct_peb_correction_Shiftmap2Warping_inputnode[label="inputnode (utility)"];

	        fsl_all_correct_peb_correction_Shiftmap2Warping_Fix_hdr[label="Fix_hdr (utility)"];

	        fsl_all_correct_peb_correction_Shiftmap2Warping_ScaleField[label="ScaleField (fsl)"];

	        fsl_all_correct_peb_correction_Shiftmap2Warping_vsm2dfm[label="vsm2dfm (fsl)"];

	        fsl_all_correct_peb_correction_Shiftmap2Warping_outputnode[label="outputnode (utility)"];

	        fsl_all_correct_peb_correction_Shiftmap2Warping_inputnode -> fsl_all_correct_peb_correction_Shiftmap2Warping_Fix_hdr;

	        fsl_all_correct_peb_correction_Shiftmap2Warping_inputnode -> fsl_all_correct_peb_correction_Shiftmap2Warping_Fix_hdr;

	        fsl_all_correct_peb_correction_Shiftmap2Warping_inputnode -> fsl_all_correct_peb_correction_Shiftmap2Warping_ScaleField;

	        fsl_all_correct_peb_correction_Shiftmap2Warping_inputnode -> fsl_all_correct_peb_correction_Shiftmap2Warping_vsm2dfm;

	        fsl_all_correct_peb_correction_Shiftmap2Warping_inputnode -> fsl_all_correct_peb_correction_Shiftmap2Warping_vsm2dfm;

	        fsl_all_correct_peb_correction_Shiftmap2Warping_Fix_hdr -> fsl_all_correct_peb_correction_Shiftmap2Warping_ScaleField;

	        fsl_all_correct_peb_correction_Shiftmap2Warping_ScaleField -> fsl_all_correct_peb_correction_Shiftmap2Warping_vsm2dfm;

	        fsl_all_correct_peb_correction_Shiftmap2Warping_vsm2dfm -> fsl_all_correct_peb_correction_Shiftmap2Warping_outputnode;

	    }

	    fsl_all_correct_peb_correction_unwarp -> fsl_all_correct_peb_correction_outputnode;

	    fsl_all_correct_peb_correction_Shiftmap2Warping_outputnode -> fsl_all_correct_peb_correction_outputnode;

	    fsl_all_correct_peb_correction_topup -> fsl_all_correct_peb_correction_Shiftmap2Warping_inputnode;

	    fsl_all_correct_peb_correction_b0_ref -> fsl_all_correct_peb_correction_Shiftmap2Warping_inputnode;

	  }

	  fsl_all_correct_fsl_eddy -> fsl_all_correct_b0_avg_post;

	  fsl_all_correct_fsl_eddy -> fsl_all_correct_Rotate_Bvec;

	  fsl_all_correct_fsl_eddy -> fsl_all_correct_outputnode;

	  fsl_all_correct_b0_avg_post -> fsl_all_correct_bet_dwi_post;

	  fsl_all_correct_bet_dwi_post -> fsl_all_correct_outputnode;

	  fsl_all_correct_Rotate_Bvec -> fsl_all_correct_outputnode;

	  fsl_all_correct_inputnode -> fsl_all_correct_peb_correction_inputnode;

	  fsl_all_correct_inputnode -> fsl_all_correct_peb_correction_inputnode;

	  fsl_all_correct_inputnode -> fsl_all_correct_peb_correction_inputnode;

	  fsl_all_correct_bet_dwi_pre -> fsl_all_correct_peb_correction_inputnode;

	  fsl_all_correct_peb_correction_topup -> fsl_all_correct_fsl_eddy;

	  fsl_all_correct_peb_correction_topup -> fsl_all_correct_fsl_eddy;

	  fsl_all_correct_peb_correction_topup -> fsl_all_correct_fsl_eddy;

	}


.. _nipype.workflows.dmri.fsl.artifacts.all_peb_pipeline:

:func:`all_peb_pipeline`
------------------------

`Link to code <http://github.com/nipy/nipype/tree/e63e055194d62d2bdc4665688261c03a42fd0025/nipype/workflows/dmri/fsl/artifacts.py#L100>`__



Builds a pipeline including three artifact corrections: head-motion
correction (HMC), susceptibility-derived distortion correction (SDC),
and Eddy currents-derived distortion correction (ECC).

.. warning:: this workflow rotates the gradients table (*b*-vectors)
  [Leemans09]_.


Examples
~~~~~~~~

>>> from nipype.workflows.dmri.fsl.artifacts import all_peb_pipeline
>>> allcorr = all_peb_pipeline()
>>> allcorr.inputs.inputnode.in_file = 'epi.nii'
>>> allcorr.inputs.inputnode.alt_file = 'epi_rev.nii'
>>> allcorr.inputs.inputnode.in_bval = 'diffusion.bval'
>>> allcorr.inputs.inputnode.in_bvec = 'diffusion.bvec'
>>> allcorr.run() # doctest: +SKIP


Graph
~~~~~

.. graphviz::

	digraph hmc_sdc_ecc{

	  label="hmc_sdc_ecc";

	  hmc_sdc_ecc_inputnode[label="inputnode (utility)"];

	  hmc_sdc_ecc_b0_avg_pre[label="b0_avg_pre (utility)"];

	  hmc_sdc_ecc_bet_dwi_pre[label="bet_dwi_pre (fsl)"];

	  hmc_sdc_ecc_b0_avg_post[label="b0_avg_post (utility)"];

	  hmc_sdc_ecc_bet_dwi_post[label="bet_dwi_post (fsl)"];

	  hmc_sdc_ecc_outputnode[label="outputnode (utility)"];

	  hmc_sdc_ecc_inputnode -> hmc_sdc_ecc_b0_avg_post;

	  hmc_sdc_ecc_inputnode -> hmc_sdc_ecc_b0_avg_pre;

	  hmc_sdc_ecc_inputnode -> hmc_sdc_ecc_b0_avg_pre;

	  hmc_sdc_ecc_b0_avg_pre -> hmc_sdc_ecc_bet_dwi_pre;

	  subgraph cluster_hmc_sdc_ecc_motion_correct {

	      label="motion_correct";

	    hmc_sdc_ecc_motion_correct_inputnode[label="inputnode (utility)"];

	    hmc_sdc_ecc_motion_correct_SplitDWI[label="SplitDWI (utility)"];

	    hmc_sdc_ecc_motion_correct_InsertRefmat[label="InsertRefmat (utility)"];

	    hmc_sdc_ecc_motion_correct_Rotate_Bvec[label="Rotate_Bvec (utility)"];

	    hmc_sdc_ecc_motion_correct_outputnode[label="outputnode (utility)"];

	    hmc_sdc_ecc_motion_correct_inputnode -> hmc_sdc_ecc_motion_correct_SplitDWI;

	    hmc_sdc_ecc_motion_correct_inputnode -> hmc_sdc_ecc_motion_correct_SplitDWI;

	    hmc_sdc_ecc_motion_correct_inputnode -> hmc_sdc_ecc_motion_correct_SplitDWI;

	    hmc_sdc_ecc_motion_correct_inputnode -> hmc_sdc_ecc_motion_correct_Rotate_Bvec;

	    hmc_sdc_ecc_motion_correct_SplitDWI -> hmc_sdc_ecc_motion_correct_InsertRefmat;

	    subgraph cluster_hmc_sdc_ecc_motion_correct_DWICoregistration {

	            label="DWICoregistration";

	        hmc_sdc_ecc_motion_correct_DWICoregistration_inputnode[label="inputnode (utility)"];

	        hmc_sdc_ecc_motion_correct_DWICoregistration_InitXforms[label="InitXforms (utility)"];

	        hmc_sdc_ecc_motion_correct_DWICoregistration_Bias[label="Bias (ants)"];

	        hmc_sdc_ecc_motion_correct_DWICoregistration_B0Equalize[label="B0Equalize (utility)"];

	        hmc_sdc_ecc_motion_correct_DWICoregistration_MskDilate[label="MskDilate (fsl)"];

	        hmc_sdc_ecc_motion_correct_DWICoregistration_SplitDWIs[label="SplitDWIs (fsl)"];

	        hmc_sdc_ecc_motion_correct_DWICoregistration_DWEqualize[label="DWEqualize (utility)"];

	        hmc_sdc_ecc_motion_correct_DWICoregistration_CoRegistration[label="CoRegistration (fsl)"];

	        hmc_sdc_ecc_motion_correct_DWICoregistration_RemoveNegative[label="RemoveNegative (fsl)"];

	        hmc_sdc_ecc_motion_correct_DWICoregistration_MergeDWIs[label="MergeDWIs (fsl)"];

	        hmc_sdc_ecc_motion_correct_DWICoregistration_outputnode[label="outputnode (utility)"];

	        hmc_sdc_ecc_motion_correct_DWICoregistration_inputnode -> hmc_sdc_ecc_motion_correct_DWICoregistration_SplitDWIs;

	        hmc_sdc_ecc_motion_correct_DWICoregistration_inputnode -> hmc_sdc_ecc_motion_correct_DWICoregistration_Bias;

	        hmc_sdc_ecc_motion_correct_DWICoregistration_inputnode -> hmc_sdc_ecc_motion_correct_DWICoregistration_Bias;

	        hmc_sdc_ecc_motion_correct_DWICoregistration_inputnode -> hmc_sdc_ecc_motion_correct_DWICoregistration_InitXforms;

	        hmc_sdc_ecc_motion_correct_DWICoregistration_inputnode -> hmc_sdc_ecc_motion_correct_DWICoregistration_InitXforms;

	        hmc_sdc_ecc_motion_correct_DWICoregistration_inputnode -> hmc_sdc_ecc_motion_correct_DWICoregistration_B0Equalize;

	        hmc_sdc_ecc_motion_correct_DWICoregistration_inputnode -> hmc_sdc_ecc_motion_correct_DWICoregistration_MskDilate;

	        hmc_sdc_ecc_motion_correct_DWICoregistration_InitXforms -> hmc_sdc_ecc_motion_correct_DWICoregistration_CoRegistration;

	        hmc_sdc_ecc_motion_correct_DWICoregistration_Bias -> hmc_sdc_ecc_motion_correct_DWICoregistration_B0Equalize;

	        hmc_sdc_ecc_motion_correct_DWICoregistration_B0Equalize -> hmc_sdc_ecc_motion_correct_DWICoregistration_CoRegistration;

	        hmc_sdc_ecc_motion_correct_DWICoregistration_MskDilate -> hmc_sdc_ecc_motion_correct_DWICoregistration_CoRegistration;

	        hmc_sdc_ecc_motion_correct_DWICoregistration_MskDilate -> hmc_sdc_ecc_motion_correct_DWICoregistration_CoRegistration;

	        hmc_sdc_ecc_motion_correct_DWICoregistration_MskDilate -> hmc_sdc_ecc_motion_correct_DWICoregistration_DWEqualize;

	        hmc_sdc_ecc_motion_correct_DWICoregistration_SplitDWIs -> hmc_sdc_ecc_motion_correct_DWICoregistration_DWEqualize;

	        hmc_sdc_ecc_motion_correct_DWICoregistration_DWEqualize -> hmc_sdc_ecc_motion_correct_DWICoregistration_CoRegistration;

	        hmc_sdc_ecc_motion_correct_DWICoregistration_CoRegistration -> hmc_sdc_ecc_motion_correct_DWICoregistration_RemoveNegative;

	        hmc_sdc_ecc_motion_correct_DWICoregistration_CoRegistration -> hmc_sdc_ecc_motion_correct_DWICoregistration_outputnode;

	        hmc_sdc_ecc_motion_correct_DWICoregistration_RemoveNegative -> hmc_sdc_ecc_motion_correct_DWICoregistration_MergeDWIs;

	        hmc_sdc_ecc_motion_correct_DWICoregistration_MergeDWIs -> hmc_sdc_ecc_motion_correct_DWICoregistration_outputnode;

	    }

	    hmc_sdc_ecc_motion_correct_InsertRefmat -> hmc_sdc_ecc_motion_correct_Rotate_Bvec;

	    hmc_sdc_ecc_motion_correct_InsertRefmat -> hmc_sdc_ecc_motion_correct_outputnode;

	    hmc_sdc_ecc_motion_correct_Rotate_Bvec -> hmc_sdc_ecc_motion_correct_outputnode;

	    hmc_sdc_ecc_motion_correct_inputnode -> hmc_sdc_ecc_motion_correct_DWICoregistration_inputnode;

	    hmc_sdc_ecc_motion_correct_SplitDWI -> hmc_sdc_ecc_motion_correct_DWICoregistration_inputnode;

	    hmc_sdc_ecc_motion_correct_SplitDWI -> hmc_sdc_ecc_motion_correct_DWICoregistration_inputnode;

	    hmc_sdc_ecc_motion_correct_SplitDWI -> hmc_sdc_ecc_motion_correct_DWICoregistration_inputnode;

	    hmc_sdc_ecc_motion_correct_DWICoregistration_outputnode -> hmc_sdc_ecc_motion_correct_InsertRefmat;

	    hmc_sdc_ecc_motion_correct_DWICoregistration_outputnode -> hmc_sdc_ecc_motion_correct_outputnode;

	  }

	  subgraph cluster_hmc_sdc_ecc_eddy_correct {

	      label="eddy_correct";

	    hmc_sdc_ecc_eddy_correct_inputnode[label="inputnode (utility)"];

	    hmc_sdc_ecc_eddy_correct_b0_avg[label="b0_avg (utility)"];

	    hmc_sdc_ecc_eddy_correct_ExtractDWI[label="ExtractDWI (utility)"];

	    hmc_sdc_ecc_eddy_correct_GatherMatrices[label="GatherMatrices (utility)"];

	    hmc_sdc_ecc_eddy_correct_SplitDWIs[label="SplitDWIs (fsl)"];

	    hmc_sdc_ecc_eddy_correct_ModulateDWIs[label="ModulateDWIs (fsl)"];

	    hmc_sdc_ecc_eddy_correct_RemoveNegative[label="RemoveNegative (fsl)"];

	    hmc_sdc_ecc_eddy_correct_MergeDWIs[label="MergeDWIs (utility)"];

	    hmc_sdc_ecc_eddy_correct_outputnode[label="outputnode (utility)"];

	    hmc_sdc_ecc_eddy_correct_inputnode -> hmc_sdc_ecc_eddy_correct_GatherMatrices;

	    hmc_sdc_ecc_eddy_correct_inputnode -> hmc_sdc_ecc_eddy_correct_b0_avg;

	    hmc_sdc_ecc_eddy_correct_inputnode -> hmc_sdc_ecc_eddy_correct_b0_avg;

	    hmc_sdc_ecc_eddy_correct_inputnode -> hmc_sdc_ecc_eddy_correct_MergeDWIs;

	    hmc_sdc_ecc_eddy_correct_inputnode -> hmc_sdc_ecc_eddy_correct_MergeDWIs;

	    hmc_sdc_ecc_eddy_correct_inputnode -> hmc_sdc_ecc_eddy_correct_ExtractDWI;

	    hmc_sdc_ecc_eddy_correct_inputnode -> hmc_sdc_ecc_eddy_correct_ExtractDWI;

	    subgraph cluster_hmc_sdc_ecc_eddy_correct_DWICoregistration {

	            label="DWICoregistration";

	        hmc_sdc_ecc_eddy_correct_DWICoregistration_inputnode[label="inputnode (utility)"];

	        hmc_sdc_ecc_eddy_correct_DWICoregistration_MskDilate[label="MskDilate (fsl)"];

	        hmc_sdc_ecc_eddy_correct_DWICoregistration_Bias[label="Bias (ants)"];

	        hmc_sdc_ecc_eddy_correct_DWICoregistration_InitXforms[label="InitXforms (utility)"];

	        hmc_sdc_ecc_eddy_correct_DWICoregistration_SplitDWIs[label="SplitDWIs (fsl)"];

	        hmc_sdc_ecc_eddy_correct_DWICoregistration_DWEqualize[label="DWEqualize (utility)"];

	        hmc_sdc_ecc_eddy_correct_DWICoregistration_B0Equalize[label="B0Equalize (utility)"];

	        hmc_sdc_ecc_eddy_correct_DWICoregistration_CoRegistration[label="CoRegistration (fsl)"];

	        hmc_sdc_ecc_eddy_correct_DWICoregistration_RemoveNegative[label="RemoveNegative (fsl)"];

	        hmc_sdc_ecc_eddy_correct_DWICoregistration_MergeDWIs[label="MergeDWIs (fsl)"];

	        hmc_sdc_ecc_eddy_correct_DWICoregistration_outputnode[label="outputnode (utility)"];

	        hmc_sdc_ecc_eddy_correct_DWICoregistration_inputnode -> hmc_sdc_ecc_eddy_correct_DWICoregistration_InitXforms;

	        hmc_sdc_ecc_eddy_correct_DWICoregistration_inputnode -> hmc_sdc_ecc_eddy_correct_DWICoregistration_InitXforms;

	        hmc_sdc_ecc_eddy_correct_DWICoregistration_inputnode -> hmc_sdc_ecc_eddy_correct_DWICoregistration_SplitDWIs;

	        hmc_sdc_ecc_eddy_correct_DWICoregistration_inputnode -> hmc_sdc_ecc_eddy_correct_DWICoregistration_B0Equalize;

	        hmc_sdc_ecc_eddy_correct_DWICoregistration_inputnode -> hmc_sdc_ecc_eddy_correct_DWICoregistration_Bias;

	        hmc_sdc_ecc_eddy_correct_DWICoregistration_inputnode -> hmc_sdc_ecc_eddy_correct_DWICoregistration_Bias;

	        hmc_sdc_ecc_eddy_correct_DWICoregistration_inputnode -> hmc_sdc_ecc_eddy_correct_DWICoregistration_MskDilate;

	        hmc_sdc_ecc_eddy_correct_DWICoregistration_MskDilate -> hmc_sdc_ecc_eddy_correct_DWICoregistration_CoRegistration;

	        hmc_sdc_ecc_eddy_correct_DWICoregistration_MskDilate -> hmc_sdc_ecc_eddy_correct_DWICoregistration_CoRegistration;

	        hmc_sdc_ecc_eddy_correct_DWICoregistration_MskDilate -> hmc_sdc_ecc_eddy_correct_DWICoregistration_DWEqualize;

	        hmc_sdc_ecc_eddy_correct_DWICoregistration_Bias -> hmc_sdc_ecc_eddy_correct_DWICoregistration_B0Equalize;

	        hmc_sdc_ecc_eddy_correct_DWICoregistration_InitXforms -> hmc_sdc_ecc_eddy_correct_DWICoregistration_CoRegistration;

	        hmc_sdc_ecc_eddy_correct_DWICoregistration_SplitDWIs -> hmc_sdc_ecc_eddy_correct_DWICoregistration_DWEqualize;

	        hmc_sdc_ecc_eddy_correct_DWICoregistration_DWEqualize -> hmc_sdc_ecc_eddy_correct_DWICoregistration_CoRegistration;

	        hmc_sdc_ecc_eddy_correct_DWICoregistration_B0Equalize -> hmc_sdc_ecc_eddy_correct_DWICoregistration_CoRegistration;

	        hmc_sdc_ecc_eddy_correct_DWICoregistration_CoRegistration -> hmc_sdc_ecc_eddy_correct_DWICoregistration_RemoveNegative;

	        hmc_sdc_ecc_eddy_correct_DWICoregistration_CoRegistration -> hmc_sdc_ecc_eddy_correct_DWICoregistration_outputnode;

	        hmc_sdc_ecc_eddy_correct_DWICoregistration_RemoveNegative -> hmc_sdc_ecc_eddy_correct_DWICoregistration_MergeDWIs;

	        hmc_sdc_ecc_eddy_correct_DWICoregistration_MergeDWIs -> hmc_sdc_ecc_eddy_correct_DWICoregistration_outputnode;

	    }

	    hmc_sdc_ecc_eddy_correct_GatherMatrices -> hmc_sdc_ecc_eddy_correct_outputnode;

	    hmc_sdc_ecc_eddy_correct_SplitDWIs -> hmc_sdc_ecc_eddy_correct_ModulateDWIs;

	    hmc_sdc_ecc_eddy_correct_ModulateDWIs -> hmc_sdc_ecc_eddy_correct_RemoveNegative;

	    hmc_sdc_ecc_eddy_correct_RemoveNegative -> hmc_sdc_ecc_eddy_correct_MergeDWIs;

	    hmc_sdc_ecc_eddy_correct_MergeDWIs -> hmc_sdc_ecc_eddy_correct_outputnode;

	    hmc_sdc_ecc_eddy_correct_inputnode -> hmc_sdc_ecc_eddy_correct_DWICoregistration_inputnode;

	    hmc_sdc_ecc_eddy_correct_inputnode -> hmc_sdc_ecc_eddy_correct_DWICoregistration_inputnode;

	    hmc_sdc_ecc_eddy_correct_inputnode -> hmc_sdc_ecc_eddy_correct_DWICoregistration_inputnode;

	    hmc_sdc_ecc_eddy_correct_ExtractDWI -> hmc_sdc_ecc_eddy_correct_DWICoregistration_inputnode;

	    hmc_sdc_ecc_eddy_correct_b0_avg -> hmc_sdc_ecc_eddy_correct_DWICoregistration_inputnode;

	    hmc_sdc_ecc_eddy_correct_DWICoregistration_outputnode -> hmc_sdc_ecc_eddy_correct_ModulateDWIs;

	    hmc_sdc_ecc_eddy_correct_DWICoregistration_outputnode -> hmc_sdc_ecc_eddy_correct_GatherMatrices;

	    hmc_sdc_ecc_eddy_correct_DWICoregistration_outputnode -> hmc_sdc_ecc_eddy_correct_SplitDWIs;

	  }

	  hmc_sdc_ecc_b0_avg_post -> hmc_sdc_ecc_bet_dwi_post;

	  subgraph cluster_hmc_sdc_ecc_peb_correction {

	      label="peb_correction";

	    hmc_sdc_ecc_peb_correction_inputnode[label="inputnode (utility)"];

	    hmc_sdc_ecc_peb_correction_b0_ref[label="b0_ref (fsl)"];

	    hmc_sdc_ecc_peb_correction_b0_alt[label="b0_alt (fsl)"];

	    hmc_sdc_ecc_peb_correction_b0_list[label="b0_list (utility)"];

	    hmc_sdc_ecc_peb_correction_b0_merged[label="b0_merged (fsl)"];

	    hmc_sdc_ecc_peb_correction_topup[label="topup (fsl)"];

	    hmc_sdc_ecc_peb_correction_unwarp[label="unwarp (fsl)"];

	    hmc_sdc_ecc_peb_correction_outputnode[label="outputnode (utility)"];

	    hmc_sdc_ecc_peb_correction_inputnode -> hmc_sdc_ecc_peb_correction_b0_alt;

	    hmc_sdc_ecc_peb_correction_inputnode -> hmc_sdc_ecc_peb_correction_b0_alt;

	    hmc_sdc_ecc_peb_correction_inputnode -> hmc_sdc_ecc_peb_correction_b0_ref;

	    hmc_sdc_ecc_peb_correction_inputnode -> hmc_sdc_ecc_peb_correction_b0_ref;

	    hmc_sdc_ecc_peb_correction_inputnode -> hmc_sdc_ecc_peb_correction_unwarp;

	    hmc_sdc_ecc_peb_correction_b0_ref -> hmc_sdc_ecc_peb_correction_b0_list;

	    hmc_sdc_ecc_peb_correction_b0_alt -> hmc_sdc_ecc_peb_correction_b0_list;

	    hmc_sdc_ecc_peb_correction_b0_list -> hmc_sdc_ecc_peb_correction_b0_merged;

	    hmc_sdc_ecc_peb_correction_b0_merged -> hmc_sdc_ecc_peb_correction_topup;

	    hmc_sdc_ecc_peb_correction_topup -> hmc_sdc_ecc_peb_correction_unwarp;

	    hmc_sdc_ecc_peb_correction_topup -> hmc_sdc_ecc_peb_correction_unwarp;

	    hmc_sdc_ecc_peb_correction_topup -> hmc_sdc_ecc_peb_correction_unwarp;

	    hmc_sdc_ecc_peb_correction_topup -> hmc_sdc_ecc_peb_correction_outputnode;

	    subgraph cluster_hmc_sdc_ecc_peb_correction_Shiftmap2Warping {

	            label="Shiftmap2Warping";

	        hmc_sdc_ecc_peb_correction_Shiftmap2Warping_inputnode[label="inputnode (utility)"];

	        hmc_sdc_ecc_peb_correction_Shiftmap2Warping_Fix_hdr[label="Fix_hdr (utility)"];

	        hmc_sdc_ecc_peb_correction_Shiftmap2Warping_ScaleField[label="ScaleField (fsl)"];

	        hmc_sdc_ecc_peb_correction_Shiftmap2Warping_vsm2dfm[label="vsm2dfm (fsl)"];

	        hmc_sdc_ecc_peb_correction_Shiftmap2Warping_outputnode[label="outputnode (utility)"];

	        hmc_sdc_ecc_peb_correction_Shiftmap2Warping_inputnode -> hmc_sdc_ecc_peb_correction_Shiftmap2Warping_vsm2dfm;

	        hmc_sdc_ecc_peb_correction_Shiftmap2Warping_inputnode -> hmc_sdc_ecc_peb_correction_Shiftmap2Warping_vsm2dfm;

	        hmc_sdc_ecc_peb_correction_Shiftmap2Warping_inputnode -> hmc_sdc_ecc_peb_correction_Shiftmap2Warping_Fix_hdr;

	        hmc_sdc_ecc_peb_correction_Shiftmap2Warping_inputnode -> hmc_sdc_ecc_peb_correction_Shiftmap2Warping_Fix_hdr;

	        hmc_sdc_ecc_peb_correction_Shiftmap2Warping_inputnode -> hmc_sdc_ecc_peb_correction_Shiftmap2Warping_ScaleField;

	        hmc_sdc_ecc_peb_correction_Shiftmap2Warping_Fix_hdr -> hmc_sdc_ecc_peb_correction_Shiftmap2Warping_ScaleField;

	        hmc_sdc_ecc_peb_correction_Shiftmap2Warping_ScaleField -> hmc_sdc_ecc_peb_correction_Shiftmap2Warping_vsm2dfm;

	        hmc_sdc_ecc_peb_correction_Shiftmap2Warping_vsm2dfm -> hmc_sdc_ecc_peb_correction_Shiftmap2Warping_outputnode;

	    }

	    hmc_sdc_ecc_peb_correction_unwarp -> hmc_sdc_ecc_peb_correction_outputnode;

	    hmc_sdc_ecc_peb_correction_topup -> hmc_sdc_ecc_peb_correction_Shiftmap2Warping_inputnode;

	    hmc_sdc_ecc_peb_correction_Shiftmap2Warping_outputnode -> hmc_sdc_ecc_peb_correction_outputnode;

	    hmc_sdc_ecc_peb_correction_b0_ref -> hmc_sdc_ecc_peb_correction_Shiftmap2Warping_inputnode;

	  }

	  subgraph cluster_hmc_sdc_ecc_UnwarpArtifacts {

	      label="UnwarpArtifacts";

	    hmc_sdc_ecc_UnwarpArtifacts_inputnode[label="inputnode (utility)"];

	    hmc_sdc_ecc_UnwarpArtifacts_ConvertWarp[label="ConvertWarp (fsl)"];

	    hmc_sdc_ecc_UnwarpArtifacts_SplitDWIs[label="SplitDWIs (fsl)"];

	    hmc_sdc_ecc_UnwarpArtifacts_Reference[label="Reference (utility)"];

	    hmc_sdc_ecc_UnwarpArtifacts_UnwarpDWIs[label="UnwarpDWIs (fsl)"];

	    hmc_sdc_ecc_UnwarpArtifacts_CoeffComp[label="CoeffComp (fsl)"];

	    hmc_sdc_ecc_UnwarpArtifacts_JacobianComp[label="JacobianComp (fsl)"];

	    hmc_sdc_ecc_UnwarpArtifacts_ModulateDWIs[label="ModulateDWIs (fsl)"];

	    hmc_sdc_ecc_UnwarpArtifacts_RemoveNegative[label="RemoveNegative (fsl)"];

	    hmc_sdc_ecc_UnwarpArtifacts_MergeDWIs[label="MergeDWIs (fsl)"];

	    hmc_sdc_ecc_UnwarpArtifacts_outputnode[label="outputnode (utility)"];

	    hmc_sdc_ecc_UnwarpArtifacts_inputnode -> hmc_sdc_ecc_UnwarpArtifacts_ConvertWarp;

	    hmc_sdc_ecc_UnwarpArtifacts_inputnode -> hmc_sdc_ecc_UnwarpArtifacts_ConvertWarp;

	    hmc_sdc_ecc_UnwarpArtifacts_inputnode -> hmc_sdc_ecc_UnwarpArtifacts_ConvertWarp;

	    hmc_sdc_ecc_UnwarpArtifacts_inputnode -> hmc_sdc_ecc_UnwarpArtifacts_ConvertWarp;

	    hmc_sdc_ecc_UnwarpArtifacts_inputnode -> hmc_sdc_ecc_UnwarpArtifacts_SplitDWIs;

	    hmc_sdc_ecc_UnwarpArtifacts_ConvertWarp -> hmc_sdc_ecc_UnwarpArtifacts_CoeffComp;

	    hmc_sdc_ecc_UnwarpArtifacts_ConvertWarp -> hmc_sdc_ecc_UnwarpArtifacts_UnwarpDWIs;

	    hmc_sdc_ecc_UnwarpArtifacts_ConvertWarp -> hmc_sdc_ecc_UnwarpArtifacts_outputnode;

	    hmc_sdc_ecc_UnwarpArtifacts_SplitDWIs -> hmc_sdc_ecc_UnwarpArtifacts_Reference;

	    hmc_sdc_ecc_UnwarpArtifacts_SplitDWIs -> hmc_sdc_ecc_UnwarpArtifacts_UnwarpDWIs;

	    hmc_sdc_ecc_UnwarpArtifacts_Reference -> hmc_sdc_ecc_UnwarpArtifacts_CoeffComp;

	    hmc_sdc_ecc_UnwarpArtifacts_Reference -> hmc_sdc_ecc_UnwarpArtifacts_UnwarpDWIs;

	    hmc_sdc_ecc_UnwarpArtifacts_Reference -> hmc_sdc_ecc_UnwarpArtifacts_JacobianComp;

	    hmc_sdc_ecc_UnwarpArtifacts_UnwarpDWIs -> hmc_sdc_ecc_UnwarpArtifacts_ModulateDWIs;

	    hmc_sdc_ecc_UnwarpArtifacts_CoeffComp -> hmc_sdc_ecc_UnwarpArtifacts_JacobianComp;

	    hmc_sdc_ecc_UnwarpArtifacts_CoeffComp -> hmc_sdc_ecc_UnwarpArtifacts_outputnode;

	    hmc_sdc_ecc_UnwarpArtifacts_JacobianComp -> hmc_sdc_ecc_UnwarpArtifacts_ModulateDWIs;

	    hmc_sdc_ecc_UnwarpArtifacts_JacobianComp -> hmc_sdc_ecc_UnwarpArtifacts_outputnode;

	    hmc_sdc_ecc_UnwarpArtifacts_ModulateDWIs -> hmc_sdc_ecc_UnwarpArtifacts_RemoveNegative;

	    hmc_sdc_ecc_UnwarpArtifacts_RemoveNegative -> hmc_sdc_ecc_UnwarpArtifacts_MergeDWIs;

	    hmc_sdc_ecc_UnwarpArtifacts_MergeDWIs -> hmc_sdc_ecc_UnwarpArtifacts_outputnode;

	  }

	  hmc_sdc_ecc_bet_dwi_post -> hmc_sdc_ecc_outputnode;

	  hmc_sdc_ecc_peb_correction_outputnode -> hmc_sdc_ecc_UnwarpArtifacts_inputnode;

	  hmc_sdc_ecc_inputnode -> hmc_sdc_ecc_peb_correction_inputnode;

	  hmc_sdc_ecc_inputnode -> hmc_sdc_ecc_peb_correction_inputnode;

	  hmc_sdc_ecc_inputnode -> hmc_sdc_ecc_UnwarpArtifacts_inputnode;

	  hmc_sdc_ecc_inputnode -> hmc_sdc_ecc_motion_correct_inputnode;

	  hmc_sdc_ecc_inputnode -> hmc_sdc_ecc_motion_correct_inputnode;

	  hmc_sdc_ecc_inputnode -> hmc_sdc_ecc_motion_correct_inputnode;

	  hmc_sdc_ecc_inputnode -> hmc_sdc_ecc_eddy_correct_inputnode;

	  hmc_sdc_ecc_inputnode -> hmc_sdc_ecc_eddy_correct_inputnode;

	  hmc_sdc_ecc_bet_dwi_pre -> hmc_sdc_ecc_motion_correct_inputnode;

	  hmc_sdc_ecc_bet_dwi_pre -> hmc_sdc_ecc_eddy_correct_inputnode;

	  hmc_sdc_ecc_bet_dwi_pre -> hmc_sdc_ecc_peb_correction_inputnode;

	  hmc_sdc_ecc_UnwarpArtifacts_outputnode -> hmc_sdc_ecc_outputnode;

	  hmc_sdc_ecc_motion_correct_outputnode -> hmc_sdc_ecc_peb_correction_inputnode;

	  hmc_sdc_ecc_motion_correct_outputnode -> hmc_sdc_ecc_outputnode;

	  hmc_sdc_ecc_motion_correct_outputnode -> hmc_sdc_ecc_eddy_correct_inputnode;

	  hmc_sdc_ecc_motion_correct_outputnode -> hmc_sdc_ecc_UnwarpArtifacts_inputnode;

	  hmc_sdc_ecc_eddy_correct_outputnode -> hmc_sdc_ecc_UnwarpArtifacts_inputnode;

	  hmc_sdc_ecc_eddy_correct_outputnode -> hmc_sdc_ecc_b0_avg_post;

	}


.. _nipype.workflows.dmri.fsl.artifacts.ecc_pipeline:

:func:`ecc_pipeline`
--------------------

`Link to code <http://github.com/nipy/nipype/tree/e63e055194d62d2bdc4665688261c03a42fd0025/nipype/workflows/dmri/fsl/artifacts.py#L385>`__



ECC stands for Eddy currents correction.

Creates a pipeline that corrects for artifacts induced by Eddy currents in
dMRI sequences.
It takes a series of diffusion weighted images and linearly co-registers
them to one reference image (the average of all b0s in the dataset).

DWIs are also modulated by the determinant of the Jacobian as indicated by
[Jones10]_ and [Rohde04]_.

A list of rigid transformation matrices can be provided, sourcing from a
:func:`.hmc_pipeline` workflow, to initialize registrations in a *motion
free* framework.

A list of affine transformation matrices is available as output, so that
transforms can be chained (discussion
`here <https://github.com/nipy/nipype/pull/530#issuecomment-14505042>`_).

.. admonition:: References

  .. [Jones10] Jones DK, `The signal intensity must be modulated by the
    determinant of the Jacobian when correcting for eddy currents in
    diffusion MRI
    <http://cds.ismrm.org/protected/10MProceedings/files/1644_129.pdf>`_,
    Proc. ISMRM 18th Annual Meeting, (2010).

  .. [Rohde04] Rohde et al., `Comprehensive Approach for Correction of
    Motion and Distortion in Diffusion-Weighted MRI
    <http://stbb.nichd.nih.gov/pdf/com_app_cor_mri04.pdf>`_, MRM
    51:103-114 (2004).

Example
~~~~~~~

>>> from nipype.workflows.dmri.fsl.artifacts import ecc_pipeline
>>> ecc = ecc_pipeline()
>>> ecc.inputs.inputnode.in_file = 'diffusion.nii'
>>> ecc.inputs.inputnode.in_bval = 'diffusion.bval'
>>> ecc.inputs.inputnode.in_mask = 'mask.nii'
>>> ecc.run() # doctest: +SKIP

Inputs::

    inputnode.in_file - input dwi file
    inputnode.in_mask - weights mask of reference image (a file with data range sin [0.0, 1.0], indicating the weight of each voxel when computing the metric.
    inputnode.in_bval - b-values table
    inputnode.in_xfms - list of matrices to initialize registration (from head-motion correction)

Outputs::

    outputnode.out_file - corrected dwi file
    outputnode.out_xfms - list of transformation matrices


Graph
~~~~~

.. graphviz::

	digraph eddy_correct{

	  label="eddy_correct";

	  eddy_correct_inputnode[label="inputnode (utility)"];

	  eddy_correct_b0_avg[label="b0_avg (utility)"];

	  eddy_correct_ExtractDWI[label="ExtractDWI (utility)"];

	  eddy_correct_GatherMatrices[label="GatherMatrices (utility)"];

	  eddy_correct_SplitDWIs[label="SplitDWIs (fsl)"];

	  eddy_correct_ModulateDWIs[label="ModulateDWIs (fsl)"];

	  eddy_correct_RemoveNegative[label="RemoveNegative (fsl)"];

	  eddy_correct_MergeDWIs[label="MergeDWIs (utility)"];

	  eddy_correct_outputnode[label="outputnode (utility)"];

	  eddy_correct_inputnode -> eddy_correct_GatherMatrices;

	  eddy_correct_inputnode -> eddy_correct_b0_avg;

	  eddy_correct_inputnode -> eddy_correct_b0_avg;

	  eddy_correct_inputnode -> eddy_correct_MergeDWIs;

	  eddy_correct_inputnode -> eddy_correct_MergeDWIs;

	  eddy_correct_inputnode -> eddy_correct_ExtractDWI;

	  eddy_correct_inputnode -> eddy_correct_ExtractDWI;

	  subgraph cluster_eddy_correct_DWICoregistration {

	      label="DWICoregistration";

	    eddy_correct_DWICoregistration_inputnode[label="inputnode (utility)"];

	    eddy_correct_DWICoregistration_InitXforms[label="InitXforms (utility)"];

	    eddy_correct_DWICoregistration_Bias[label="Bias (ants)"];

	    eddy_correct_DWICoregistration_B0Equalize[label="B0Equalize (utility)"];

	    eddy_correct_DWICoregistration_SplitDWIs[label="SplitDWIs (fsl)"];

	    eddy_correct_DWICoregistration_MskDilate[label="MskDilate (fsl)"];

	    eddy_correct_DWICoregistration_DWEqualize[label="DWEqualize (utility)"];

	    eddy_correct_DWICoregistration_CoRegistration[label="CoRegistration (fsl)"];

	    eddy_correct_DWICoregistration_RemoveNegative[label="RemoveNegative (fsl)"];

	    eddy_correct_DWICoregistration_MergeDWIs[label="MergeDWIs (fsl)"];

	    eddy_correct_DWICoregistration_outputnode[label="outputnode (utility)"];

	    eddy_correct_DWICoregistration_inputnode -> eddy_correct_DWICoregistration_InitXforms;

	    eddy_correct_DWICoregistration_inputnode -> eddy_correct_DWICoregistration_InitXforms;

	    eddy_correct_DWICoregistration_inputnode -> eddy_correct_DWICoregistration_Bias;

	    eddy_correct_DWICoregistration_inputnode -> eddy_correct_DWICoregistration_Bias;

	    eddy_correct_DWICoregistration_inputnode -> eddy_correct_DWICoregistration_B0Equalize;

	    eddy_correct_DWICoregistration_inputnode -> eddy_correct_DWICoregistration_SplitDWIs;

	    eddy_correct_DWICoregistration_inputnode -> eddy_correct_DWICoregistration_MskDilate;

	    eddy_correct_DWICoregistration_InitXforms -> eddy_correct_DWICoregistration_CoRegistration;

	    eddy_correct_DWICoregistration_Bias -> eddy_correct_DWICoregistration_B0Equalize;

	    eddy_correct_DWICoregistration_B0Equalize -> eddy_correct_DWICoregistration_CoRegistration;

	    eddy_correct_DWICoregistration_SplitDWIs -> eddy_correct_DWICoregistration_DWEqualize;

	    eddy_correct_DWICoregistration_MskDilate -> eddy_correct_DWICoregistration_CoRegistration;

	    eddy_correct_DWICoregistration_MskDilate -> eddy_correct_DWICoregistration_CoRegistration;

	    eddy_correct_DWICoregistration_MskDilate -> eddy_correct_DWICoregistration_DWEqualize;

	    eddy_correct_DWICoregistration_DWEqualize -> eddy_correct_DWICoregistration_CoRegistration;

	    eddy_correct_DWICoregistration_CoRegistration -> eddy_correct_DWICoregistration_RemoveNegative;

	    eddy_correct_DWICoregistration_CoRegistration -> eddy_correct_DWICoregistration_outputnode;

	    eddy_correct_DWICoregistration_RemoveNegative -> eddy_correct_DWICoregistration_MergeDWIs;

	    eddy_correct_DWICoregistration_MergeDWIs -> eddy_correct_DWICoregistration_outputnode;

	  }

	  eddy_correct_GatherMatrices -> eddy_correct_outputnode;

	  eddy_correct_SplitDWIs -> eddy_correct_ModulateDWIs;

	  eddy_correct_ModulateDWIs -> eddy_correct_RemoveNegative;

	  eddy_correct_RemoveNegative -> eddy_correct_MergeDWIs;

	  eddy_correct_MergeDWIs -> eddy_correct_outputnode;

	  eddy_correct_ExtractDWI -> eddy_correct_DWICoregistration_inputnode;

	  eddy_correct_DWICoregistration_outputnode -> eddy_correct_GatherMatrices;

	  eddy_correct_DWICoregistration_outputnode -> eddy_correct_ModulateDWIs;

	  eddy_correct_DWICoregistration_outputnode -> eddy_correct_SplitDWIs;

	  eddy_correct_b0_avg -> eddy_correct_DWICoregistration_inputnode;

	  eddy_correct_inputnode -> eddy_correct_DWICoregistration_inputnode;

	  eddy_correct_inputnode -> eddy_correct_DWICoregistration_inputnode;

	  eddy_correct_inputnode -> eddy_correct_DWICoregistration_inputnode;

	}


.. _nipype.workflows.dmri.fsl.artifacts.hmc_pipeline:

:func:`hmc_pipeline`
--------------------

`Link to code <http://github.com/nipy/nipype/tree/e63e055194d62d2bdc4665688261c03a42fd0025/nipype/workflows/dmri/fsl/artifacts.py#L277>`__



HMC stands for head-motion correction.

Creates a pipeline that corrects for head motion artifacts in dMRI
sequences.
It takes a series of diffusion weighted images and rigidly co-registers
them to one reference image. Finally, the `b`-matrix is rotated accordingly
[Leemans09]_ making use of the rotation matrix obtained by FLIRT.

Search angles have been limited to 4 degrees, based on results in
[Yendiki13]_.

A list of rigid transformation matrices is provided, so that transforms
can be chained.
This is useful to correct for artifacts with only one interpolation process
(as previously discussed `here
<https://github.com/nipy/nipype/pull/530#issuecomment-14505042>`_),
and also to compute nuisance regressors as proposed by [Yendiki13]_.

.. warning:: This workflow rotates the `b`-vectors, so please be advised
  that not all the dicom converters ensure the consistency between the
  resulting nifti orientation and the gradients table (e.g. dcm2nii
  checks it).

.. admonition:: References

  .. [Leemans09] Leemans A, and Jones DK, `The B-matrix must be rotated
    when correcting for subject motion in DTI data
    <http://dx.doi.org/10.1002/mrm.21890>`_,
    Magn Reson Med. 61(6):1336-49. 2009. doi: 10.1002/mrm.21890.

  .. [Yendiki13] Yendiki A et al., `Spurious group differences due to head
    motion in a diffusion MRI study
    <http://dx.doi.org/10.1016/j.neuroimage.2013.11.027>`_.
    Neuroimage. 21(88C):79-90. 2013. doi: 10.1016/j.neuroimage.2013.11.027

Example
~~~~~~~

>>> from nipype.workflows.dmri.fsl.artifacts import hmc_pipeline
>>> hmc = hmc_pipeline()
>>> hmc.inputs.inputnode.in_file = 'diffusion.nii'
>>> hmc.inputs.inputnode.in_bvec = 'diffusion.bvec'
>>> hmc.inputs.inputnode.in_bval = 'diffusion.bval'
>>> hmc.inputs.inputnode.in_mask = 'mask.nii'
>>> hmc.run() # doctest: +SKIP

Inputs::

    inputnode.in_file - input dwi file
    inputnode.in_mask - weights mask of reference image (a file with data range in [0.0, 1.0], indicating the weight of each voxel when computing the metric.
    inputnode.in_bvec - gradients file (b-vectors)
    inputnode.ref_num (optional, default=0) index of the b0 volume that should be taken as reference

Outputs::

    outputnode.out_file - corrected dwi file
    outputnode.out_bvec - rotated gradient vectors table
    outputnode.out_xfms - list of transformation matrices


Graph
~~~~~

.. graphviz::

	digraph motion_correct{

	  label="motion_correct";

	  motion_correct_inputnode[label="inputnode (utility)"];

	  motion_correct_SplitDWI[label="SplitDWI (utility)"];

	  motion_correct_InsertRefmat[label="InsertRefmat (utility)"];

	  motion_correct_Rotate_Bvec[label="Rotate_Bvec (utility)"];

	  motion_correct_outputnode[label="outputnode (utility)"];

	  motion_correct_inputnode -> motion_correct_SplitDWI;

	  motion_correct_inputnode -> motion_correct_SplitDWI;

	  motion_correct_inputnode -> motion_correct_SplitDWI;

	  motion_correct_inputnode -> motion_correct_Rotate_Bvec;

	  motion_correct_SplitDWI -> motion_correct_InsertRefmat;

	  subgraph cluster_motion_correct_DWICoregistration {

	      label="DWICoregistration";

	    motion_correct_DWICoregistration_inputnode[label="inputnode (utility)"];

	    motion_correct_DWICoregistration_InitXforms[label="InitXforms (utility)"];

	    motion_correct_DWICoregistration_SplitDWIs[label="SplitDWIs (fsl)"];

	    motion_correct_DWICoregistration_MskDilate[label="MskDilate (fsl)"];

	    motion_correct_DWICoregistration_DWEqualize[label="DWEqualize (utility)"];

	    motion_correct_DWICoregistration_Bias[label="Bias (ants)"];

	    motion_correct_DWICoregistration_B0Equalize[label="B0Equalize (utility)"];

	    motion_correct_DWICoregistration_CoRegistration[label="CoRegistration (fsl)"];

	    motion_correct_DWICoregistration_RemoveNegative[label="RemoveNegative (fsl)"];

	    motion_correct_DWICoregistration_MergeDWIs[label="MergeDWIs (fsl)"];

	    motion_correct_DWICoregistration_outputnode[label="outputnode (utility)"];

	    motion_correct_DWICoregistration_inputnode -> motion_correct_DWICoregistration_InitXforms;

	    motion_correct_DWICoregistration_inputnode -> motion_correct_DWICoregistration_InitXforms;

	    motion_correct_DWICoregistration_inputnode -> motion_correct_DWICoregistration_MskDilate;

	    motion_correct_DWICoregistration_inputnode -> motion_correct_DWICoregistration_Bias;

	    motion_correct_DWICoregistration_inputnode -> motion_correct_DWICoregistration_Bias;

	    motion_correct_DWICoregistration_inputnode -> motion_correct_DWICoregistration_SplitDWIs;

	    motion_correct_DWICoregistration_inputnode -> motion_correct_DWICoregistration_B0Equalize;

	    motion_correct_DWICoregistration_InitXforms -> motion_correct_DWICoregistration_CoRegistration;

	    motion_correct_DWICoregistration_SplitDWIs -> motion_correct_DWICoregistration_DWEqualize;

	    motion_correct_DWICoregistration_MskDilate -> motion_correct_DWICoregistration_CoRegistration;

	    motion_correct_DWICoregistration_MskDilate -> motion_correct_DWICoregistration_CoRegistration;

	    motion_correct_DWICoregistration_MskDilate -> motion_correct_DWICoregistration_DWEqualize;

	    motion_correct_DWICoregistration_DWEqualize -> motion_correct_DWICoregistration_CoRegistration;

	    motion_correct_DWICoregistration_Bias -> motion_correct_DWICoregistration_B0Equalize;

	    motion_correct_DWICoregistration_B0Equalize -> motion_correct_DWICoregistration_CoRegistration;

	    motion_correct_DWICoregistration_CoRegistration -> motion_correct_DWICoregistration_RemoveNegative;

	    motion_correct_DWICoregistration_CoRegistration -> motion_correct_DWICoregistration_outputnode;

	    motion_correct_DWICoregistration_RemoveNegative -> motion_correct_DWICoregistration_MergeDWIs;

	    motion_correct_DWICoregistration_MergeDWIs -> motion_correct_DWICoregistration_outputnode;

	  }

	  motion_correct_InsertRefmat -> motion_correct_Rotate_Bvec;

	  motion_correct_InsertRefmat -> motion_correct_outputnode;

	  motion_correct_Rotate_Bvec -> motion_correct_outputnode;

	  motion_correct_SplitDWI -> motion_correct_DWICoregistration_inputnode;

	  motion_correct_SplitDWI -> motion_correct_DWICoregistration_inputnode;

	  motion_correct_SplitDWI -> motion_correct_DWICoregistration_inputnode;

	  motion_correct_DWICoregistration_outputnode -> motion_correct_InsertRefmat;

	  motion_correct_DWICoregistration_outputnode -> motion_correct_outputnode;

	  motion_correct_inputnode -> motion_correct_DWICoregistration_inputnode;

	}


.. _nipype.workflows.dmri.fsl.artifacts.remove_bias:

:func:`remove_bias`
-------------------

`Link to code <http://github.com/nipy/nipype/tree/e63e055194d62d2bdc4665688261c03a42fd0025/nipype/workflows/dmri/fsl/artifacts.py#L754>`__



This workflow estimates a single multiplicative bias field from the
averaged *b0* image, as suggested in [Jeurissen2014]_.

.. admonition:: References

  .. [Jeurissen2014] Jeurissen B. et al., `Multi-tissue constrained
    spherical deconvolution for improved analysis of multi-shell diffusion
    MRI data <http://dx.doi.org/10.1016/j.neuroimage.2014.07.061>`_.
    NeuroImage (2014). doi: 10.1016/j.neuroimage.2014.07.061


Example
~~~~~~~

>>> from nipype.workflows.dmri.fsl.artifacts import remove_bias
>>> bias = remove_bias()
>>> bias.inputs.inputnode.in_file = 'epi.nii'
>>> bias.inputs.inputnode.in_bval = 'diffusion.bval'
>>> bias.inputs.inputnode.in_mask = 'mask.nii'
>>> bias.run() # doctest: +SKIP


Graph
~~~~~

.. graphviz::

	digraph bias_correct{

	  label="bias_correct";

	  bias_correct_inputnode[label="inputnode (utility)"];

	  bias_correct_b0_avg[label="b0_avg (utility)"];

	  bias_correct_SplitDWIs[label="SplitDWIs (fsl)"];

	  bias_correct_Bias_b0[label="Bias_b0 (ants)"];

	  bias_correct_RemoveBiasOfDWIs[label="RemoveBiasOfDWIs (fsl)"];

	  bias_correct_RemoveNegative[label="RemoveNegative (fsl)"];

	  bias_correct_MergeDWIs[label="MergeDWIs (fsl)"];

	  bias_correct_outputnode[label="outputnode (utility)"];

	  bias_correct_inputnode -> bias_correct_b0_avg;

	  bias_correct_inputnode -> bias_correct_b0_avg;

	  bias_correct_inputnode -> bias_correct_Bias_b0;

	  bias_correct_inputnode -> bias_correct_SplitDWIs;

	  bias_correct_b0_avg -> bias_correct_Bias_b0;

	  bias_correct_SplitDWIs -> bias_correct_RemoveBiasOfDWIs;

	  bias_correct_Bias_b0 -> bias_correct_RemoveBiasOfDWIs;

	  bias_correct_RemoveBiasOfDWIs -> bias_correct_RemoveNegative;

	  bias_correct_RemoveNegative -> bias_correct_MergeDWIs;

	  bias_correct_MergeDWIs -> bias_correct_outputnode;

	}


.. _nipype.workflows.dmri.fsl.artifacts.sdc_fmb:

:func:`sdc_fmb`
---------------

`Link to code <http://github.com/nipy/nipype/tree/e63e055194d62d2bdc4665688261c03a42fd0025/nipype/workflows/dmri/fsl/artifacts.py#L503>`__



SDC stands for susceptibility distortion correction. FMB stands for
fieldmap-based.

The fieldmap based method (FMB) implements SDC by using a mapping of the
B0 field as proposed by [Jezzard95]_. This workflow uses the implementation
of FSL (`FUGUE <http://fsl.fmrib.ox.ac.uk/fsl/fslwiki/FUGUE>`_). Phase
unwrapping is performed using `PRELUDE
<http://fsl.fmrib.ox.ac.uk/fsl/fsl-4.1.9/fugue/prelude.html>`_
[Jenkinson03]_. Preparation of the fieldmap is performed reproducing the
script in FSL `fsl_prepare_fieldmap
<http://fsl.fmrib.ox.ac.uk/fsl/fslwiki/FUGUE/Guide#SIEMENS_data>`_.

Example
~~~~~~~

>>> from nipype.workflows.dmri.fsl.artifacts import sdc_fmb
>>> fmb = sdc_fmb()
>>> fmb.inputs.inputnode.in_file = 'diffusion.nii'
>>> fmb.inputs.inputnode.in_bval = 'diffusion.bval'
>>> fmb.inputs.inputnode.in_mask = 'mask.nii'
>>> fmb.inputs.inputnode.bmap_mag = 'magnitude.nii'
>>> fmb.inputs.inputnode.bmap_pha = 'phase.nii'
>>> fmb.run() # doctest: +SKIP

.. warning:: Only SIEMENS format fieldmaps are supported.

.. admonition:: References

  .. [Jezzard95] Jezzard P, and Balaban RS, `Correction for geometric
    distortion in echo planar images from B0 field variations
    <http://dx.doi.org/10.1002/mrm.1910340111>`_,
    MRM 34(1):65-73. (1995). doi: 10.1002/mrm.1910340111.

  .. [Jenkinson03] Jenkinson M., `Fast, automated, N-dimensional
    phase-unwrapping algorithm <http://dx.doi.org/10.1002/mrm.10354>`_,
    MRM 49(1):193-197, 2003, doi: 10.1002/mrm.10354.


Graph
~~~~~

.. graphviz::

	digraph fmb_correction{

	  label="fmb_correction";

	  fmb_correction_inputnode[label="inputnode (utility)"];

	  fmb_correction_PreparePhase[label="PreparePhase (utility)"];

	  fmb_correction_b0_avg[label="b0_avg (utility)"];

	  fmb_correction_GetFirst[label="GetFirst (fsl)"];

	  fmb_correction_Bias[label="Bias (ants)"];

	  fmb_correction_BrainExtraction[label="BrainExtraction (fsl)"];

	  fmb_correction_MskDilate[label="MskDilate (fsl)"];

	  fmb_correction_PhaseUnwrap[label="PhaseUnwrap (fsl)"];

	  fmb_correction_ToRadSec[label="ToRadSec (utility)"];

	  fmb_correction_BmapMag2B0[label="BmapMag2B0 (fsl)"];

	  fmb_correction_BmapPha2B0[label="BmapPha2B0 (fsl)"];

	  fmb_correction_PreliminaryFugue[label="PreliminaryFugue (fsl)"];

	  fmb_correction_DemeanFmap[label="DemeanFmap (utility)"];

	  fmb_correction_AddEmptyVol[label="AddEmptyVol (utility)"];

	  fmb_correction_ComputeVSM[label="ComputeVSM (fsl)"];

	  fmb_correction_SplitDWIs[label="SplitDWIs (fsl)"];

	  fmb_correction_UnwarpDWIs[label="UnwarpDWIs (fsl)"];

	  fmb_correction_RemoveNegative[label="RemoveNegative (fsl)"];

	  fmb_correction_MergeDWIs[label="MergeDWIs (fsl)"];

	  fmb_correction_outputnode[label="outputnode (utility)"];

	  fmb_correction_inputnode -> fmb_correction_PreparePhase;

	  fmb_correction_inputnode -> fmb_correction_b0_avg;

	  fmb_correction_inputnode -> fmb_correction_b0_avg;

	  fmb_correction_inputnode -> fmb_correction_ComputeVSM;

	  fmb_correction_inputnode -> fmb_correction_PreliminaryFugue;

	  fmb_correction_inputnode -> fmb_correction_GetFirst;

	  fmb_correction_inputnode -> fmb_correction_BmapMag2B0;

	  fmb_correction_inputnode -> fmb_correction_DemeanFmap;

	  fmb_correction_inputnode -> fmb_correction_SplitDWIs;

	  fmb_correction_PreparePhase -> fmb_correction_PhaseUnwrap;

	  fmb_correction_b0_avg -> fmb_correction_BmapMag2B0;

	  fmb_correction_b0_avg -> fmb_correction_BmapPha2B0;

	  fmb_correction_GetFirst -> fmb_correction_Bias;

	  fmb_correction_Bias -> fmb_correction_PhaseUnwrap;

	  fmb_correction_Bias -> fmb_correction_BrainExtraction;

	  fmb_correction_Bias -> fmb_correction_BmapMag2B0;

	  fmb_correction_BrainExtraction -> fmb_correction_MskDilate;

	  fmb_correction_MskDilate -> fmb_correction_PhaseUnwrap;

	  fmb_correction_MskDilate -> fmb_correction_BmapMag2B0;

	  fmb_correction_PhaseUnwrap -> fmb_correction_ToRadSec;

	  fmb_correction_ToRadSec -> fmb_correction_BmapPha2B0;

	  fmb_correction_BmapMag2B0 -> fmb_correction_BmapPha2B0;

	  fmb_correction_BmapPha2B0 -> fmb_correction_PreliminaryFugue;

	  fmb_correction_PreliminaryFugue -> fmb_correction_DemeanFmap;

	  subgraph cluster_fmb_correction_Cleanup {

	      label="Cleanup";

	    fmb_correction_Cleanup_inputnode[label="inputnode (utility)"];

	    fmb_correction_Cleanup_Despike[label="Despike (fsl)"];

	    fmb_correction_Cleanup_MskErode[label="MskErode (fsl)"];

	    fmb_correction_Cleanup_NewMask[label="NewMask (fsl)"];

	    fmb_correction_Cleanup_ApplyMask[label="ApplyMask (fsl)"];

	    fmb_correction_Cleanup_Merge[label="Merge (utility)"];

	    fmb_correction_Cleanup_AddEdge[label="AddEdge (fsl)"];

	    fmb_correction_Cleanup_outputnode[label="outputnode (utility)"];

	    fmb_correction_Cleanup_inputnode -> fmb_correction_Cleanup_MskErode;

	    fmb_correction_Cleanup_inputnode -> fmb_correction_Cleanup_Despike;

	    fmb_correction_Cleanup_inputnode -> fmb_correction_Cleanup_Despike;

	    fmb_correction_Cleanup_inputnode -> fmb_correction_Cleanup_AddEdge;

	    fmb_correction_Cleanup_inputnode -> fmb_correction_Cleanup_NewMask;

	    fmb_correction_Cleanup_Despike -> fmb_correction_Cleanup_ApplyMask;

	    fmb_correction_Cleanup_MskErode -> fmb_correction_Cleanup_NewMask;

	    fmb_correction_Cleanup_MskErode -> fmb_correction_Cleanup_Merge;

	    fmb_correction_Cleanup_NewMask -> fmb_correction_Cleanup_ApplyMask;

	    fmb_correction_Cleanup_ApplyMask -> fmb_correction_Cleanup_Merge;

	    fmb_correction_Cleanup_Merge -> fmb_correction_Cleanup_AddEdge;

	    fmb_correction_Cleanup_AddEdge -> fmb_correction_Cleanup_outputnode;

	  }

	  fmb_correction_AddEmptyVol -> fmb_correction_ComputeVSM;

	  fmb_correction_ComputeVSM -> fmb_correction_outputnode;

	  fmb_correction_ComputeVSM -> fmb_correction_UnwarpDWIs;

	  fmb_correction_SplitDWIs -> fmb_correction_UnwarpDWIs;

	  fmb_correction_UnwarpDWIs -> fmb_correction_RemoveNegative;

	  fmb_correction_RemoveNegative -> fmb_correction_MergeDWIs;

	  fmb_correction_MergeDWIs -> fmb_correction_outputnode;

	  subgraph cluster_fmb_correction_Shiftmap2Warping {

	      label="Shiftmap2Warping";

	    fmb_correction_Shiftmap2Warping_inputnode[label="inputnode (utility)"];

	    fmb_correction_Shiftmap2Warping_Fix_hdr[label="Fix_hdr (utility)"];

	    fmb_correction_Shiftmap2Warping_ScaleField[label="ScaleField (fsl)"];

	    fmb_correction_Shiftmap2Warping_vsm2dfm[label="vsm2dfm (fsl)"];

	    fmb_correction_Shiftmap2Warping_outputnode[label="outputnode (utility)"];

	    fmb_correction_Shiftmap2Warping_inputnode -> fmb_correction_Shiftmap2Warping_ScaleField;

	    fmb_correction_Shiftmap2Warping_inputnode -> fmb_correction_Shiftmap2Warping_Fix_hdr;

	    fmb_correction_Shiftmap2Warping_inputnode -> fmb_correction_Shiftmap2Warping_Fix_hdr;

	    fmb_correction_Shiftmap2Warping_inputnode -> fmb_correction_Shiftmap2Warping_vsm2dfm;

	    fmb_correction_Shiftmap2Warping_inputnode -> fmb_correction_Shiftmap2Warping_vsm2dfm;

	    fmb_correction_Shiftmap2Warping_Fix_hdr -> fmb_correction_Shiftmap2Warping_ScaleField;

	    fmb_correction_Shiftmap2Warping_ScaleField -> fmb_correction_Shiftmap2Warping_vsm2dfm;

	    fmb_correction_Shiftmap2Warping_vsm2dfm -> fmb_correction_Shiftmap2Warping_outputnode;

	  }

	  fmb_correction_inputnode -> fmb_correction_Cleanup_inputnode;

	  fmb_correction_MergeDWIs -> fmb_correction_Shiftmap2Warping_inputnode;

	  fmb_correction_DemeanFmap -> fmb_correction_Cleanup_inputnode;

	  fmb_correction_Cleanup_outputnode -> fmb_correction_AddEmptyVol;

	  fmb_correction_Shiftmap2Warping_outputnode -> fmb_correction_outputnode;

	  fmb_correction_ComputeVSM -> fmb_correction_Shiftmap2Warping_inputnode;

	}


.. _nipype.workflows.dmri.fsl.artifacts.sdc_peb:

:func:`sdc_peb`
---------------

`Link to code <http://github.com/nipy/nipype/tree/e63e055194d62d2bdc4665688261c03a42fd0025/nipype/workflows/dmri/fsl/artifacts.py#L649>`__



SDC stands for susceptibility distortion correction. PEB stands for
phase-encoding-based.

The phase-encoding-based (PEB) method implements SDC by acquiring
diffusion images with two different enconding directions [Andersson2003]_.
The most typical case is acquiring with opposed phase-gradient blips
(e.g. *A>>>P* and *P>>>A*, or equivalently, *-y* and *y*)
as in [Chiou2000]_, but it is also possible to use orthogonal
configurations [Cordes2000]_ (e.g. *A>>>P* and *L>>>R*,
or equivalently *-y* and *x*).
This workflow uses the implementation of FSL
(`TOPUP <http://fsl.fmrib.ox.ac.uk/fsl/fslwiki/TOPUP>`_).

Example
~~~~~~~

>>> from nipype.workflows.dmri.fsl.artifacts import sdc_peb
>>> peb = sdc_peb()
>>> peb.inputs.inputnode.in_file = 'epi.nii'
>>> peb.inputs.inputnode.alt_file = 'epi_rev.nii'
>>> peb.inputs.inputnode.in_bval = 'diffusion.bval'
>>> peb.inputs.inputnode.in_mask = 'mask.nii'
>>> peb.run() # doctest: +SKIP

.. admonition:: References

  .. [Andersson2003] Andersson JL et al., `How to correct susceptibility
    distortions in spin-echo echo-planar images: application to diffusion
    tensor imaging <http://dx.doi.org/10.1016/S1053-8119(03)00336-7>`_.
    Neuroimage. 2003 Oct;20(2):870-88. doi: 10.1016/S1053-8119(03)00336-7

  .. [Cordes2000] Cordes D et al., Geometric distortion correction in EPI
    using two images with orthogonal phase-encoding directions, in Proc.
    ISMRM (8), p.1712, Denver, US, 2000.

  .. [Chiou2000] Chiou JY, and Nalcioglu O, A simple method to correct
    off-resonance related distortion in echo planar imaging, in Proc.
    ISMRM (8), p.1712, Denver, US, 2000.


Graph
~~~~~

.. graphviz::

	digraph peb_correction{

	  label="peb_correction";

	  peb_correction_inputnode[label="inputnode (utility)"];

	  peb_correction_b0_alt[label="b0_alt (fsl)"];

	  peb_correction_b0_ref[label="b0_ref (fsl)"];

	  peb_correction_b0_list[label="b0_list (utility)"];

	  peb_correction_b0_merged[label="b0_merged (fsl)"];

	  peb_correction_topup[label="topup (fsl)"];

	  peb_correction_unwarp[label="unwarp (fsl)"];

	  peb_correction_outputnode[label="outputnode (utility)"];

	  peb_correction_inputnode -> peb_correction_b0_alt;

	  peb_correction_inputnode -> peb_correction_b0_alt;

	  peb_correction_inputnode -> peb_correction_b0_ref;

	  peb_correction_inputnode -> peb_correction_b0_ref;

	  peb_correction_inputnode -> peb_correction_unwarp;

	  peb_correction_b0_alt -> peb_correction_b0_list;

	  peb_correction_b0_ref -> peb_correction_b0_list;

	  peb_correction_b0_list -> peb_correction_b0_merged;

	  peb_correction_b0_merged -> peb_correction_topup;

	  peb_correction_topup -> peb_correction_unwarp;

	  peb_correction_topup -> peb_correction_unwarp;

	  peb_correction_topup -> peb_correction_unwarp;

	  peb_correction_topup -> peb_correction_outputnode;

	  subgraph cluster_peb_correction_Shiftmap2Warping {

	      label="Shiftmap2Warping";

	    peb_correction_Shiftmap2Warping_inputnode[label="inputnode (utility)"];

	    peb_correction_Shiftmap2Warping_Fix_hdr[label="Fix_hdr (utility)"];

	    peb_correction_Shiftmap2Warping_ScaleField[label="ScaleField (fsl)"];

	    peb_correction_Shiftmap2Warping_vsm2dfm[label="vsm2dfm (fsl)"];

	    peb_correction_Shiftmap2Warping_outputnode[label="outputnode (utility)"];

	    peb_correction_Shiftmap2Warping_inputnode -> peb_correction_Shiftmap2Warping_ScaleField;

	    peb_correction_Shiftmap2Warping_inputnode -> peb_correction_Shiftmap2Warping_Fix_hdr;

	    peb_correction_Shiftmap2Warping_inputnode -> peb_correction_Shiftmap2Warping_Fix_hdr;

	    peb_correction_Shiftmap2Warping_inputnode -> peb_correction_Shiftmap2Warping_vsm2dfm;

	    peb_correction_Shiftmap2Warping_inputnode -> peb_correction_Shiftmap2Warping_vsm2dfm;

	    peb_correction_Shiftmap2Warping_Fix_hdr -> peb_correction_Shiftmap2Warping_ScaleField;

	    peb_correction_Shiftmap2Warping_ScaleField -> peb_correction_Shiftmap2Warping_vsm2dfm;

	    peb_correction_Shiftmap2Warping_vsm2dfm -> peb_correction_Shiftmap2Warping_outputnode;

	  }

	  peb_correction_unwarp -> peb_correction_outputnode;

	  peb_correction_topup -> peb_correction_Shiftmap2Warping_inputnode;

	  peb_correction_b0_ref -> peb_correction_Shiftmap2Warping_inputnode;

	  peb_correction_Shiftmap2Warping_outputnode -> peb_correction_outputnode;

	}

