.. AUTO-GENERATED FILE -- DO NOT EDIT!

interfaces.dipy.tensors
=======================


.. _nipype.interfaces.dipy.tensors.TensorMode:


.. index:: TensorMode

TensorMode
----------

`Link to code <http://github.com/nipy/nipype/tree/e63e055194d62d2bdc4665688261c03a42fd0025/nipype/interfaces/dipy/tensors.py#L46>`__

Creates a map of the mode of the diffusion tensors given a set of
diffusion-weighted images, as well as their associated b-values and
b-vectors. Fits the diffusion tensors and calculates tensor mode
with Dipy.

.. [1] Daniel B. Ennis and G. Kindlmann, "Orthogonal Tensor
    Invariants and the Analysis of Diffusion Tensor Magnetic Resonance
    Images", Magnetic Resonance in Medicine, vol. 55, no. 1, pp. 136-146,
    2006.

Example
~~~~~~~

>>> import nipype.interfaces.dipy as dipy
>>> mode = dipy.TensorMode()
>>> mode.inputs.in_file = 'diffusion.nii'
>>> mode.inputs.bvecs = 'bvecs'
>>> mode.inputs.bvals = 'bvals'
>>> mode.run()                                   # doctest: +SKIP

Inputs::

        [Mandatory]
        bvals: (an existing file name)
                The input b-value text file
        bvecs: (an existing file name)
                The input b-vector text file
        in_file: (an existing file name)
                The input 4D diffusion-weighted image file

        [Optional]
        out_filename: (a file name)
                The output filename for the Tensor mode image

Outputs::

        out_file: (an existing file name)
