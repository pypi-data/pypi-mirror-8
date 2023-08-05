.. AUTO-GENERATED FILE -- DO NOT EDIT!

workflows.dmri.fsl.tbss
=======================


.. module:: nipype.workflows.dmri.fsl.tbss


.. _nipype.workflows.dmri.fsl.tbss.create_tbss_1_preproc:

:func:`create_tbss_1_preproc`
-----------------------------

`Link to code <http://github.com/nipy/nipype/tree/e63e055194d62d2bdc4665688261c03a42fd0025/nipype/workflows/dmri/fsl/tbss.py#L23>`__



Preprocess FA data for TBSS: erodes a little and zero end slicers and
creates masks(for use in FLIRT & FNIRT from FSL).
A pipeline that does the same as tbss_1_preproc script in FSL

Example
~~~~~~~

>>> from nipype.workflows.dmri.fsl import tbss
>>> tbss1 = tbss.create_tbss_1_preproc()
>>> tbss1.inputs.inputnode.fa_list = ['s1_FA.nii', 's2_FA.nii', 's3_FA.nii']

Inputs::

    inputnode.fa_list

Outputs::

    outputnode.fa_list
    outputnode.mask_list
    outputnode.slices


Graph
~~~~~

.. graphviz::

	digraph tbss_1_preproc{

	  label="tbss_1_preproc";

	  tbss_1_preproc_inputnode[label="inputnode (utility)"];

	  tbss_1_preproc_prepfa[label="prepfa (fsl)"];

	  tbss_1_preproc_getmask1[label="getmask1 (fsl)"];

	  tbss_1_preproc_slicer[label="slicer (fsl)"];

	  tbss_1_preproc_getmask2[label="getmask2 (fsl)"];

	  tbss_1_preproc_outputnode[label="outputnode (utility)"];

	  tbss_1_preproc_inputnode -> tbss_1_preproc_prepfa;

	  tbss_1_preproc_inputnode -> tbss_1_preproc_prepfa;

	  tbss_1_preproc_prepfa -> tbss_1_preproc_outputnode;

	  tbss_1_preproc_prepfa -> tbss_1_preproc_getmask1;

	  tbss_1_preproc_prepfa -> tbss_1_preproc_slicer;

	  tbss_1_preproc_getmask1 -> tbss_1_preproc_getmask2;

	  tbss_1_preproc_getmask1 -> tbss_1_preproc_getmask2;

	  tbss_1_preproc_slicer -> tbss_1_preproc_outputnode;

	  tbss_1_preproc_getmask2 -> tbss_1_preproc_outputnode;

	}


.. _nipype.workflows.dmri.fsl.tbss.create_tbss_2_reg:

:func:`create_tbss_2_reg`
-------------------------

`Link to code <http://github.com/nipy/nipype/tree/e63e055194d62d2bdc4665688261c03a42fd0025/nipype/workflows/dmri/fsl/tbss.py#L94>`__



TBSS nonlinear registration:
A pipeline that does the same as 'tbss_2_reg -t' script in FSL. '-n' option
is not supported at the moment.

Example
~~~~~~~

>>> from nipype.workflows.dmri.fsl import tbss
>>> tbss2 = create_tbss_2_reg(name="tbss2")
>>> tbss2.inputs.inputnode.target = fsl.Info.standard_image("FMRIB58_FA_1mm.nii.gz")  # doctest: +SKIP
>>> tbss2.inputs.inputnode.fa_list = ['s1_FA.nii', 's2_FA.nii', 's3_FA.nii']
>>> tbss2.inputs.inputnode.mask_list = ['s1_mask.nii', 's2_mask.nii', 's3_mask.nii']

Inputs::

    inputnode.fa_list
    inputnode.mask_list
    inputnode.target

Outputs::

    outputnode.field_list


Graph
~~~~~

.. graphviz::

	digraph tbss_2_reg{

	  label="tbss_2_reg";

	  tbss_2_reg_inputnode[label="inputnode (utility)"];

	  tbss_2_reg_flirt[label="flirt (fsl)"];

	  tbss_2_reg_fnirt[label="fnirt (fsl)"];

	  tbss_2_reg_outputnode[label="outputnode (utility)"];

	  tbss_2_reg_inputnode -> tbss_2_reg_flirt;

	  tbss_2_reg_inputnode -> tbss_2_reg_flirt;

	  tbss_2_reg_inputnode -> tbss_2_reg_flirt;

	  tbss_2_reg_inputnode -> tbss_2_reg_fnirt;

	  tbss_2_reg_inputnode -> tbss_2_reg_fnirt;

	  tbss_2_reg_inputnode -> tbss_2_reg_fnirt;

	  tbss_2_reg_flirt -> tbss_2_reg_fnirt;

	  tbss_2_reg_fnirt -> tbss_2_reg_outputnode;

	}


.. _nipype.workflows.dmri.fsl.tbss.create_tbss_3_postreg:

:func:`create_tbss_3_postreg`
-----------------------------

`Link to code <http://github.com/nipy/nipype/tree/e63e055194d62d2bdc4665688261c03a42fd0025/nipype/workflows/dmri/fsl/tbss.py#L166>`__



Post-registration processing: derive mean_FA and mean_FA_skeleton from
mean of all subjects in study. Target is assumed to be FMRIB58_FA_1mm.
A pipeline that does the same as 'tbss_3_postreg -S' script from FSL
Setting 'estimate_skeleton to False will use precomputed FMRIB58_FA-skeleton_1mm
skeleton (same as 'tbss_3_postreg -T').

Example
~~~~~~~

>>> from nipype.workflows.dmri.fsl import tbss
>>> tbss3 = tbss.create_tbss_3_postreg()
>>> tbss3.inputs.inputnode.fa_list = ['s1_wrapped_FA.nii', 's2_wrapped_FA.nii', 's3_wrapped_FA.nii']

Inputs::

    inputnode.field_list
    inputnode.fa_list

Outputs::

    outputnode.groupmask
    outputnode.skeleton_file
    outputnode.meanfa_file
    outputnode.mergefa_file


Graph
~~~~~

.. graphviz::

	digraph tbss_3_postreg{

	  label="tbss_3_postreg";

	  tbss_3_postreg_inputnode[label="inputnode (utility)"];

	  tbss_3_postreg_applywarp[label="applywarp (fsl)"];

	  tbss_3_postreg_mergefa[label="mergefa (fsl)"];

	  tbss_3_postreg_groupmask[label="groupmask (fsl)"];

	  tbss_3_postreg_maskgroup[label="maskgroup (fsl)"];

	  tbss_3_postreg_meanfa[label="meanfa (fsl)"];

	  tbss_3_postreg_makeskeleton[label="makeskeleton (fsl)"];

	  tbss_3_postreg_outputnode[label="outputnode (utility)"];

	  tbss_3_postreg_inputnode -> tbss_3_postreg_applywarp;

	  tbss_3_postreg_inputnode -> tbss_3_postreg_applywarp;

	  tbss_3_postreg_applywarp -> tbss_3_postreg_mergefa;

	  tbss_3_postreg_mergefa -> tbss_3_postreg_groupmask;

	  tbss_3_postreg_mergefa -> tbss_3_postreg_maskgroup;

	  tbss_3_postreg_groupmask -> tbss_3_postreg_maskgroup;

	  tbss_3_postreg_groupmask -> tbss_3_postreg_outputnode;

	  tbss_3_postreg_maskgroup -> tbss_3_postreg_outputnode;

	  tbss_3_postreg_maskgroup -> tbss_3_postreg_meanfa;

	  tbss_3_postreg_meanfa -> tbss_3_postreg_outputnode;

	  tbss_3_postreg_meanfa -> tbss_3_postreg_makeskeleton;

	  tbss_3_postreg_makeskeleton -> tbss_3_postreg_outputnode;

	}


.. _nipype.workflows.dmri.fsl.tbss.create_tbss_4_prestats:

:func:`create_tbss_4_prestats`
------------------------------

`Link to code <http://github.com/nipy/nipype/tree/e63e055194d62d2bdc4665688261c03a42fd0025/nipype/workflows/dmri/fsl/tbss.py#L293>`__



Post-registration processing:Creating skeleton mask using a threshold
 projecting all FA data onto skeleton.
A pipeline that does the same as tbss_4_prestats script from FSL

Example
~~~~~~~

>>> from nipype.workflows.dmri.fsl import tbss
>>> tbss4 = tbss.create_tbss_4_prestats(name='tbss4')
>>> tbss4.inputs.inputnode.skeleton_thresh = 0.2

Inputs::

    inputnode.skeleton_thresh
    inputnode.groupmask
    inputnode.skeleton_file
    inputnode.meanfa_file
    inputnode.mergefa_file

Outputs::

    outputnode.all_FA_skeletonised
    outputnode.mean_FA_skeleton_mask
    outputnode.distance_map
    outputnode.skeleton_file


Graph
~~~~~

.. graphviz::

	digraph tbss_4_prestats{

	  label="tbss_4_prestats";

	  tbss_4_prestats_inputnode[label="inputnode (utility)"];

	  tbss_4_prestats_skeletonmask[label="skeletonmask (fsl)"];

	  tbss_4_prestats_invertmask[label="invertmask (fsl)"];

	  tbss_4_prestats_distancemap[label="distancemap (fsl)"];

	  tbss_4_prestats_projectfa[label="projectfa (fsl)"];

	  tbss_4_prestats_outputnode[label="outputnode (utility)"];

	  tbss_4_prestats_inputnode -> tbss_4_prestats_projectfa;

	  tbss_4_prestats_inputnode -> tbss_4_prestats_projectfa;

	  tbss_4_prestats_inputnode -> tbss_4_prestats_projectfa;

	  tbss_4_prestats_inputnode -> tbss_4_prestats_invertmask;

	  tbss_4_prestats_inputnode -> tbss_4_prestats_skeletonmask;

	  tbss_4_prestats_inputnode -> tbss_4_prestats_skeletonmask;

	  tbss_4_prestats_skeletonmask -> tbss_4_prestats_invertmask;

	  tbss_4_prestats_skeletonmask -> tbss_4_prestats_outputnode;

	  tbss_4_prestats_invertmask -> tbss_4_prestats_distancemap;

	  tbss_4_prestats_distancemap -> tbss_4_prestats_projectfa;

	  tbss_4_prestats_distancemap -> tbss_4_prestats_outputnode;

	  tbss_4_prestats_projectfa -> tbss_4_prestats_outputnode;

	  tbss_4_prestats_projectfa -> tbss_4_prestats_outputnode;

	}


.. _nipype.workflows.dmri.fsl.tbss.create_tbss_all:

:func:`create_tbss_all`
-----------------------

`Link to code <http://github.com/nipy/nipype/tree/e63e055194d62d2bdc4665688261c03a42fd0025/nipype/workflows/dmri/fsl/tbss.py#L382>`__



Create a pipeline that combines create_tbss_* pipelines

Example
~~~~~~~

>>> from nipype.workflows.dmri.fsl import tbss
>>> tbss = tbss.create_tbss_all('tbss')
>>> tbss.inputs.inputnode.skeleton_thresh = 0.2

Inputs::

    inputnode.fa_list
    inputnode.skeleton_thresh

Outputs::

    outputnode.meanfa_file
    outputnode.projectedfa_file
    outputnode.skeleton_file
    outputnode.skeleton_mask


Graph
~~~~~

.. graphviz::

	digraph tbss_all{

	  label="tbss_all";

	  tbss_all_inputnode[label="inputnode (utility)"];

	  tbss_all_outputnode[label="outputnode (utility)"];

	  tbss_all_outputall_node[label="outputall_node (utility)"];

	  subgraph cluster_tbss_all_tbss1 {

	      label="tbss1";

	    tbss_all_tbss1_inputnode[label="inputnode (utility)"];

	    tbss_all_tbss1_prepfa[label="prepfa (fsl)"];

	    tbss_all_tbss1_getmask1[label="getmask1 (fsl)"];

	    tbss_all_tbss1_getmask2[label="getmask2 (fsl)"];

	    tbss_all_tbss1_slicer[label="slicer (fsl)"];

	    tbss_all_tbss1_outputnode[label="outputnode (utility)"];

	    tbss_all_tbss1_inputnode -> tbss_all_tbss1_prepfa;

	    tbss_all_tbss1_inputnode -> tbss_all_tbss1_prepfa;

	    tbss_all_tbss1_prepfa -> tbss_all_tbss1_slicer;

	    tbss_all_tbss1_prepfa -> tbss_all_tbss1_getmask1;

	    tbss_all_tbss1_prepfa -> tbss_all_tbss1_outputnode;

	    tbss_all_tbss1_getmask1 -> tbss_all_tbss1_getmask2;

	    tbss_all_tbss1_getmask1 -> tbss_all_tbss1_getmask2;

	    tbss_all_tbss1_getmask2 -> tbss_all_tbss1_outputnode;

	    tbss_all_tbss1_slicer -> tbss_all_tbss1_outputnode;

	  }

	  subgraph cluster_tbss_all_tbss2 {

	      label="tbss2";

	    tbss_all_tbss2_inputnode[label="inputnode (utility)"];

	    tbss_all_tbss2_flirt[label="flirt (fsl)"];

	    tbss_all_tbss2_fnirt[label="fnirt (fsl)"];

	    tbss_all_tbss2_outputnode[label="outputnode (utility)"];

	    tbss_all_tbss2_inputnode -> tbss_all_tbss2_flirt;

	    tbss_all_tbss2_inputnode -> tbss_all_tbss2_flirt;

	    tbss_all_tbss2_inputnode -> tbss_all_tbss2_flirt;

	    tbss_all_tbss2_inputnode -> tbss_all_tbss2_fnirt;

	    tbss_all_tbss2_inputnode -> tbss_all_tbss2_fnirt;

	    tbss_all_tbss2_inputnode -> tbss_all_tbss2_fnirt;

	    tbss_all_tbss2_flirt -> tbss_all_tbss2_fnirt;

	    tbss_all_tbss2_fnirt -> tbss_all_tbss2_outputnode;

	  }

	  subgraph cluster_tbss_all_tbss3 {

	      label="tbss3";

	    tbss_all_tbss3_inputnode[label="inputnode (utility)"];

	    tbss_all_tbss3_applywarp[label="applywarp (fsl)"];

	    tbss_all_tbss3_mergefa[label="mergefa (fsl)"];

	    tbss_all_tbss3_groupmask[label="groupmask (fsl)"];

	    tbss_all_tbss3_maskgroup[label="maskgroup (fsl)"];

	    tbss_all_tbss3_meanfa[label="meanfa (fsl)"];

	    tbss_all_tbss3_makeskeleton[label="makeskeleton (fsl)"];

	    tbss_all_tbss3_outputnode[label="outputnode (utility)"];

	    tbss_all_tbss3_inputnode -> tbss_all_tbss3_applywarp;

	    tbss_all_tbss3_inputnode -> tbss_all_tbss3_applywarp;

	    tbss_all_tbss3_applywarp -> tbss_all_tbss3_mergefa;

	    tbss_all_tbss3_mergefa -> tbss_all_tbss3_groupmask;

	    tbss_all_tbss3_mergefa -> tbss_all_tbss3_maskgroup;

	    tbss_all_tbss3_groupmask -> tbss_all_tbss3_outputnode;

	    tbss_all_tbss3_groupmask -> tbss_all_tbss3_maskgroup;

	    tbss_all_tbss3_maskgroup -> tbss_all_tbss3_meanfa;

	    tbss_all_tbss3_maskgroup -> tbss_all_tbss3_outputnode;

	    tbss_all_tbss3_meanfa -> tbss_all_tbss3_makeskeleton;

	    tbss_all_tbss3_meanfa -> tbss_all_tbss3_outputnode;

	    tbss_all_tbss3_makeskeleton -> tbss_all_tbss3_outputnode;

	  }

	  subgraph cluster_tbss_all_tbss4 {

	      label="tbss4";

	    tbss_all_tbss4_inputnode[label="inputnode (utility)"];

	    tbss_all_tbss4_skeletonmask[label="skeletonmask (fsl)"];

	    tbss_all_tbss4_invertmask[label="invertmask (fsl)"];

	    tbss_all_tbss4_distancemap[label="distancemap (fsl)"];

	    tbss_all_tbss4_projectfa[label="projectfa (fsl)"];

	    tbss_all_tbss4_outputnode[label="outputnode (utility)"];

	    tbss_all_tbss4_inputnode -> tbss_all_tbss4_invertmask;

	    tbss_all_tbss4_inputnode -> tbss_all_tbss4_skeletonmask;

	    tbss_all_tbss4_inputnode -> tbss_all_tbss4_skeletonmask;

	    tbss_all_tbss4_inputnode -> tbss_all_tbss4_projectfa;

	    tbss_all_tbss4_inputnode -> tbss_all_tbss4_projectfa;

	    tbss_all_tbss4_inputnode -> tbss_all_tbss4_projectfa;

	    tbss_all_tbss4_skeletonmask -> tbss_all_tbss4_invertmask;

	    tbss_all_tbss4_skeletonmask -> tbss_all_tbss4_outputnode;

	    tbss_all_tbss4_invertmask -> tbss_all_tbss4_distancemap;

	    tbss_all_tbss4_distancemap -> tbss_all_tbss4_projectfa;

	    tbss_all_tbss4_distancemap -> tbss_all_tbss4_outputnode;

	    tbss_all_tbss4_projectfa -> tbss_all_tbss4_outputnode;

	    tbss_all_tbss4_projectfa -> tbss_all_tbss4_outputnode;

	  }

	  tbss_all_tbss2_outputnode -> tbss_all_tbss3_inputnode;

	  tbss_all_tbss2_outputnode -> tbss_all_outputall_node;

	  tbss_all_tbss3_outputnode -> tbss_all_outputall_node;

	  tbss_all_tbss3_outputnode -> tbss_all_outputall_node;

	  tbss_all_tbss3_outputnode -> tbss_all_outputall_node;

	  tbss_all_tbss3_outputnode -> tbss_all_outputall_node;

	  tbss_all_tbss3_outputnode -> tbss_all_tbss4_inputnode;

	  tbss_all_tbss3_outputnode -> tbss_all_tbss4_inputnode;

	  tbss_all_tbss3_outputnode -> tbss_all_tbss4_inputnode;

	  tbss_all_tbss3_outputnode -> tbss_all_tbss4_inputnode;

	  tbss_all_tbss3_outputnode -> tbss_all_outputnode;

	  tbss_all_tbss3_outputnode -> tbss_all_outputnode;

	  tbss_all_tbss3_outputnode -> tbss_all_outputnode;

	  tbss_all_tbss3_outputnode -> tbss_all_outputnode;

	  tbss_all_inputnode -> tbss_all_tbss1_inputnode;

	  tbss_all_inputnode -> tbss_all_tbss4_inputnode;

	  tbss_all_tbss4_outputnode -> tbss_all_outputnode;

	  tbss_all_tbss4_outputnode -> tbss_all_outputnode;

	  tbss_all_tbss4_outputnode -> tbss_all_outputnode;

	  tbss_all_tbss4_outputnode -> tbss_all_outputnode;

	  tbss_all_tbss4_outputnode -> tbss_all_outputall_node;

	  tbss_all_tbss4_outputnode -> tbss_all_outputall_node;

	  tbss_all_tbss4_outputnode -> tbss_all_outputall_node;

	  tbss_all_tbss1_outputnode -> tbss_all_outputall_node;

	  tbss_all_tbss1_outputnode -> tbss_all_outputall_node;

	  tbss_all_tbss1_outputnode -> tbss_all_tbss2_inputnode;

	  tbss_all_tbss1_outputnode -> tbss_all_tbss2_inputnode;

	  tbss_all_tbss1_outputnode -> tbss_all_tbss3_inputnode;

	}


.. _nipype.workflows.dmri.fsl.tbss.create_tbss_non_FA:

:func:`create_tbss_non_FA`
--------------------------

`Link to code <http://github.com/nipy/nipype/tree/e63e055194d62d2bdc4665688261c03a42fd0025/nipype/workflows/dmri/fsl/tbss.py#L492>`__



A pipeline that implement tbss_non_FA in FSL

Example
~~~~~~~

>>> from nipype.workflows.dmri.fsl import tbss
>>> tbss_MD = tbss.create_tbss_non_FA()
>>> tbss_MD.inputs.inputnode.file_list = []
>>> tbss_MD.inputs.inputnode.field_list = []
>>> tbss_MD.inputs.inputnode.skeleton_thresh = 0.2
>>> tbss_MD.inputs.inputnode.groupmask = './xxx'
>>> tbss_MD.inputs.inputnode.meanfa_file = './xxx'
>>> tbss_MD.inputs.inputnode.distance_map = []

Inputs::

    inputnode.file_list
    inputnode.field_list
    inputnode.skeleton_thresh
    inputnode.groupmask
    inputnode.meanfa_file
    inputnode.distance_map

Outputs::

    outputnode.projected_nonFA_file


Graph
~~~~~

.. graphviz::

	digraph tbss_non_FA{

	  label="tbss_non_FA";

	  tbss_non_FA_inputnode[label="inputnode (utility)"];

	  tbss_non_FA_applywarp[label="applywarp (fsl)"];

	  tbss_non_FA_merge[label="merge (fsl)"];

	  tbss_non_FA_maskgroup[label="maskgroup (fsl)"];

	  tbss_non_FA_projectfa[label="projectfa (fsl)"];

	  tbss_non_FA_outputnode[label="outputnode (utility)"];

	  tbss_non_FA_inputnode -> tbss_non_FA_applywarp;

	  tbss_non_FA_inputnode -> tbss_non_FA_applywarp;

	  tbss_non_FA_inputnode -> tbss_non_FA_maskgroup;

	  tbss_non_FA_inputnode -> tbss_non_FA_projectfa;

	  tbss_non_FA_inputnode -> tbss_non_FA_projectfa;

	  tbss_non_FA_inputnode -> tbss_non_FA_projectfa;

	  tbss_non_FA_applywarp -> tbss_non_FA_merge;

	  tbss_non_FA_merge -> tbss_non_FA_maskgroup;

	  tbss_non_FA_maskgroup -> tbss_non_FA_projectfa;

	  tbss_non_FA_projectfa -> tbss_non_FA_outputnode;

	}


.. _nipype.workflows.dmri.fsl.tbss.tbss1_op_string:

:func:`tbss1_op_string`
-----------------------

`Link to code <http://github.com/nipy/nipype/tree/e63e055194d62d2bdc4665688261c03a42fd0025/nipype/workflows/dmri/fsl/tbss.py#L12>`__






.. _nipype.workflows.dmri.fsl.tbss.tbss4_op_string:

:func:`tbss4_op_string`
-----------------------

`Link to code <http://github.com/nipy/nipype/tree/e63e055194d62d2bdc4665688261c03a42fd0025/nipype/workflows/dmri/fsl/tbss.py#L288>`__





