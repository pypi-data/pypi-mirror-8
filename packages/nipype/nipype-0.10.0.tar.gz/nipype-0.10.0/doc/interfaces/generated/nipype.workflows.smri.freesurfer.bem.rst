.. AUTO-GENERATED FILE -- DO NOT EDIT!

workflows.smri.freesurfer.bem
=============================


.. module:: nipype.workflows.smri.freesurfer.bem


.. _nipype.workflows.smri.freesurfer.bem.create_bem_flow:

:func:`create_bem_flow`
-----------------------

`Link to code <http://github.com/nipy/nipype/tree/e63e055194d62d2bdc4665688261c03a42fd0025/nipype/workflows/smri/freesurfer/bem.py#L11>`__



Uses MNE's Watershed algorithm to create Boundary Element Meshes (BEM)
 for a subject's brain, inner/outer skull, and skin. The surfaces are
 returned in the desired (by default, stereolithic .stl) format.

Example
~~~~~~~
>>> from nipype.workflows.smri.freesurfer import create_bem_flow
>>> bemflow = create_bem_flow()
>>> bemflow.inputs.inputspec.subject_id = 'subj1'
>>> bemflow.inputs.inputspec.subjects_dir = '.'
>>> bemflow.run()  # doctest: +SKIP


Inputs::

       inputspec.subject_id : freesurfer subject id
       inputspec.subjects_dir : freesurfer subjects directory

Outputs::

       outputspec.meshes : output boundary element meshes in (by default) stereolithographic (.stl) format


Graph
~~~~~

.. graphviz::

	digraph bem{

	  label="bem";

	  bem_inputspec[label="inputspec (utility)"];

	  bem_WatershedBEM[label="WatershedBEM (mne)"];

	  bem_surfconvert[label="surfconvert (freesurfer)"];

	  bem_outputspec[label="outputspec (utility)"];

	  bem_inputspec -> bem_WatershedBEM;

	  bem_inputspec -> bem_WatershedBEM;

	  bem_WatershedBEM -> bem_surfconvert;

	  bem_surfconvert -> bem_outputspec;

	}

