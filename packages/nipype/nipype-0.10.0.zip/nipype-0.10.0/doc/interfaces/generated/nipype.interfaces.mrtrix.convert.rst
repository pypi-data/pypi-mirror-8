.. AUTO-GENERATED FILE -- DO NOT EDIT!

interfaces.mrtrix.convert
=========================


.. _nipype.interfaces.mrtrix.convert.MRTrix2TrackVis:


.. index:: MRTrix2TrackVis

MRTrix2TrackVis
---------------

`Link to code <http://github.com/nipy/nipype/tree/e63e055194d62d2bdc4665688261c03a42fd0025/nipype/interfaces/mrtrix/convert.py#L155>`__

Converts MRtrix (.tck) tract files into TrackVis (.trk) format
using functions from dipy

Example
~~~~~~~

>>> import nipype.interfaces.mrtrix as mrt
>>> tck2trk = mrt.MRTrix2TrackVis()
>>> tck2trk.inputs.in_file = 'dwi_CSD_tracked.tck'
>>> tck2trk.inputs.image_file = 'diffusion.nii'
>>> tck2trk.run()                                   # doctest: +SKIP

Inputs::

        [Mandatory]
        in_file: (an existing file name)
                The input file for the tracks in MRTrix (.tck) format

        [Optional]
        image_file: (an existing file name)
                The image the tracks were generated from
        matrix_file: (an existing file name)
                A transformation matrix to apply to the tracts after they have been
                generated (from FLIRT - affine transformation from image_file to
                registration_image_file)
        out_filename: (a file name, nipype default value: converted.trk)
                The output filename for the tracks in TrackVis (.trk) format
        registration_image_file: (an existing file name)
                The final image the tracks should be registered to.

Outputs::

        out_file: (an existing file name)

.. module:: nipype.interfaces.mrtrix.convert


.. _nipype.interfaces.mrtrix.convert.read_mrtrix_header:

:func:`read_mrtrix_header`
--------------------------

`Link to code <http://github.com/nipy/nipype/tree/e63e055194d62d2bdc4665688261c03a42fd0025/nipype/interfaces/mrtrix/convert.py#L52>`__






.. _nipype.interfaces.mrtrix.convert.read_mrtrix_streamlines:

:func:`read_mrtrix_streamlines`
-------------------------------

`Link to code <http://github.com/nipy/nipype/tree/e63e055194d62d2bdc4665688261c03a42fd0025/nipype/interfaces/mrtrix/convert.py#L72>`__






.. _nipype.interfaces.mrtrix.convert.read_mrtrix_tracks:

:func:`read_mrtrix_tracks`
--------------------------

`Link to code <http://github.com/nipy/nipype/tree/e63e055194d62d2bdc4665688261c03a42fd0025/nipype/interfaces/mrtrix/convert.py#L47>`__






.. _nipype.interfaces.mrtrix.convert.transform_to_affine:

:func:`transform_to_affine`
---------------------------

`Link to code <http://github.com/nipy/nipype/tree/e63e055194d62d2bdc4665688261c03a42fd0025/nipype/interfaces/mrtrix/convert.py#L39>`__





