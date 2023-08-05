.. AUTO-GENERATED FILE -- DO NOT EDIT!

algorithms.misc
===============


.. _nipype.algorithms.misc.AddCSVColumn:


.. index:: AddCSVColumn

AddCSVColumn
------------

`Link to code <http://github.com/nipy/nipype/tree/e63e055194d62d2bdc4665688261c03a42fd0025/nipype/algorithms/misc.py#L742>`__

Short interface to add an extra column and field to a text file

Example
~~~~~~~

>>> from nipype.algorithms import misc
>>> addcol = misc.AddCSVColumn()
>>> addcol.inputs.in_file = 'degree.csv'
>>> addcol.inputs.extra_column_heading = 'group'
>>> addcol.inputs.extra_field = 'male'
>>> addcol.run() # doctest: +SKIP

Inputs::

        [Mandatory]
        in_file: (an existing file name)
                Input comma-separated value (CSV) files

        [Optional]
        extra_column_heading: (a string)
                New heading to add for the added field.
        extra_field: (a string)
                New field to add to each row. This is useful for saving the group or
                subject ID in the file.
        out_file: (a file name, nipype default value: extra_heading.csv)
                Output filename for merged CSV file

Outputs::

        csv_file: (a file name)
                Output CSV file containing columns

.. _nipype.algorithms.misc.AddCSVRow:


.. index:: AddCSVRow

AddCSVRow
---------

`Link to code <http://github.com/nipy/nipype/tree/e63e055194d62d2bdc4665688261c03a42fd0025/nipype/algorithms/misc.py#L806>`__

Simple interface to add an extra row to a csv file

.. note:: Requires `pandas <http://pandas.pydata.org/>`_

.. warning:: Multi-platform thread-safe execution is possible with
    `lockfile <https://pythonhosted.org/lockfile/lockfile.html>`_. Please recall that (1)
    this module is alpha software; and (2) it should be installed for thread-safe writing.
    If lockfile is not installed, then the interface is not thread-safe.


Example
~~~~~~~

>>> from nipype.algorithms import misc
>>> addrow = misc.AddCSVRow()
>>> addrow.inputs.in_file = 'scores.csv'
>>> addrow.inputs.si = 0.74
>>> addrow.inputs.di = 0.93
>>> addrow.subject_id = 'S400'
>>> addrow.inputs.list_of_values = [ 0.4, 0.7, 0.3 ]
>>> addrow.run() # doctest: +SKIP

Inputs::

        [Mandatory]
        in_file: (a file name)
                Input comma-separated value (CSV) files

        [Optional]
        _outputs: (a dictionary with keys which are any value and with values
                 which are any value, nipype default value: {})
        ignore_exception: (a boolean, nipype default value: False)
                Print an error message instead of throwing an exception in case the
                interface fails to run

Outputs::

        csv_file: (a file name)
                Output CSV file containing rows

.. _nipype.algorithms.misc.AddNoise:


.. index:: AddNoise

AddNoise
--------

`Link to code <http://github.com/nipy/nipype/tree/e63e055194d62d2bdc4665688261c03a42fd0025/nipype/algorithms/misc.py#L980>`__

Corrupts with noise the input image


Example
~~~~~~~
>>> from nipype.algorithms.misc import AddNoise
>>> noise = AddNoise()
>>> noise.inputs.in_file = 'T1.nii'
>>> noise.inputs.in_mask = 'mask.nii'
>>> noise.snr = 30.0
>>> noise.run() # doctest: +SKIP

Inputs::

        [Mandatory]
        bg_dist: ('normal' or 'rayleigh', nipype default value: normal)
                desired noise distribution, currently only normal is implemented
        dist: ('normal' or 'rician', nipype default value: normal)
                desired noise distribution
        in_file: (an existing file name)
                input image that will be corrupted with noise

        [Optional]
        in_mask: (an existing file name)
                input mask, voxels outside this mask will be considered background
        out_file: (a file name)
                desired output filename
        snr: (a float, nipype default value: 10.0)
                desired output SNR in dB

Outputs::

        out_file: (an existing file name)
                corrupted image

.. _nipype.algorithms.misc.CalculateNormalizedMoments:


.. index:: CalculateNormalizedMoments

CalculateNormalizedMoments
--------------------------

`Link to code <http://github.com/nipy/nipype/tree/e63e055194d62d2bdc4665688261c03a42fd0025/nipype/algorithms/misc.py#L919>`__

Calculates moments of timeseries.

Example
~~~~~~~

>>> from nipype.algorithms import misc
>>> skew = misc.CalculateNormalizedMoments()
>>> skew.inputs.moment = 3
>>> skew.inputs.timeseries_file = 'timeseries.txt'
>>> skew.run() # doctest: +SKIP

Inputs::

        [Mandatory]
        moment: (an integer)
                Define which moment should be calculated, 3 for skewness, 4 for
                kurtosis.
        timeseries_file: (an existing file name)
                Text file with timeseries in columns and timepoints in rows,
                whitespace separated

        [Optional]

Outputs::

        moments: (a list of items which are a float)
                Moments

.. _nipype.algorithms.misc.CreateNifti:


.. index:: CreateNifti

CreateNifti
-----------

`Link to code <http://github.com/nipy/nipype/tree/e63e055194d62d2bdc4665688261c03a42fd0025/nipype/algorithms/misc.py#L230>`__

Creates a nifti volume

Inputs::

        [Mandatory]
        data_file: (an existing file name)
                ANALYZE img file
        header_file: (an existing file name)
                corresponding ANALYZE hdr file

        [Optional]
        affine: (an array)
                affine transformation array
        ignore_exception: (a boolean, nipype default value: False)
                Print an error message instead of throwing an exception in case the
                interface fails to run

Outputs::

        nifti_file: (an existing file name)

.. _nipype.algorithms.misc.Distance:


.. index:: Distance

Distance
--------

`Link to code <http://github.com/nipy/nipype/tree/e63e055194d62d2bdc4665688261c03a42fd0025/nipype/algorithms/misc.py#L1443>`__

Calculates distance between two volumes.

.. deprecated:: 0.10.0
   Use :py:class:`nipype.algorithms.metrics.Distance` instead.

Inputs::

        [Mandatory]
        volume1: (an existing file name)
                Has to have the same dimensions as volume2.
        volume2: (an existing file name)
                Has to have the same dimensions as volume1.

        [Optional]
        ignore_exception: (a boolean, nipype default value: False)
                Print an error message instead of throwing an exception in case the
                interface fails to run
        mask_volume: (an existing file name)
                calculate overlap only within this mask.
        method: ('eucl_min' or 'eucl_cog' or 'eucl_mean' or 'eucl_wmean' or
                 'eucl_max', nipype default value: eucl_min)
                ""eucl_min": Euclidean distance between two closest points
                "eucl_cog": mean Euclidian distance between the Center of Gravity of
                volume1 and CoGs of volume2 "eucl_mean": mean Euclidian minimum
                distance of all volume2 voxels to volume1 "eucl_wmean": mean
                Euclidian minimum distance of all volume2 voxels to volume1 weighted
                by their values "eucl_max": maximum over minimum Euclidian distances
                of all volume2 voxels to volume1 (also known as the Hausdorff
                distance)

Outputs::

        distance: (a float)
        histogram: (a file name)
        point1: (an array with shape (3,))
        point2: (an array with shape (3,))

.. _nipype.algorithms.misc.FuzzyOverlap:


.. index:: FuzzyOverlap

FuzzyOverlap
------------

`Link to code <http://github.com/nipy/nipype/tree/e63e055194d62d2bdc4665688261c03a42fd0025/nipype/algorithms/misc.py#L1469>`__

Calculates various overlap measures between two maps, using a fuzzy
definition.

.. deprecated:: 0.10.0
   Use :py:class:`nipype.algorithms.metrics.FuzzyOverlap` instead.

Inputs::

        [Mandatory]
        in_ref: (an existing file name)
                Reference image. Requires the same dimensions as in_tst.
        in_tst: (an existing file name)
                Test image. Requires the same dimensions as in_ref.

        [Optional]
        ignore_exception: (a boolean, nipype default value: False)
                Print an error message instead of throwing an exception in case the
                interface fails to run
        out_file: (a file name, nipype default value: diff.nii)
                alternative name for resulting difference-map
        weighting: ('none' or 'volume' or 'squared_vol', nipype default
                 value: none)
                'none': no class-overlap weighting is performed. 'volume': computed
                class-overlaps are weighted by class volume 'squared_vol': computed
                class-overlaps are weighted by the squared volume of the class

Outputs::

        class_fdi: (a list of items which are a float)
                Array containing the fDIs of each computed class
        class_fji: (a list of items which are a float)
                Array containing the fJIs of each computed class
        dice: (a float)
                Fuzzy Dice Index (fDI), all the classes
        diff_file: (an existing file name)
                resulting difference-map of all classes, using the chosen weighting
        jaccard: (a float)
                Fuzzy Jaccard Index (fJI), all the classes

.. _nipype.algorithms.misc.Gunzip:


.. index:: Gunzip

Gunzip
------

`Link to code <http://github.com/nipy/nipype/tree/e63e055194d62d2bdc4665688261c03a42fd0025/nipype/algorithms/misc.py#L351>`__

Gunzip wrapper

Inputs::

        [Mandatory]
        in_file: (an existing file name)

        [Optional]
        ignore_exception: (a boolean, nipype default value: False)
                Print an error message instead of throwing an exception in case the
                interface fails to run

Outputs::

        out_file: (an existing file name)

.. _nipype.algorithms.misc.Matlab2CSV:


.. index:: Matlab2CSV

Matlab2CSV
----------

`Link to code <http://github.com/nipy/nipype/tree/e63e055194d62d2bdc4665688261c03a42fd0025/nipype/algorithms/misc.py#L415>`__

Simple interface to save the components of a MATLAB .mat file as a text
file with comma-separated values (CSVs).

CSV files are easily loaded in R, for use in statistical processing.
For further information, see cran.r-project.org/doc/manuals/R-data.pdf

Example
~~~~~~~

>>> from nipype.algorithms import misc
>>> mat2csv = misc.Matlab2CSV()
>>> mat2csv.inputs.in_file = 'cmatrix.mat'
>>> mat2csv.run() # doctest: +SKIP

Inputs::

        [Mandatory]
        in_file: (an existing file name)
                Input MATLAB .mat file

        [Optional]
        reshape_matrix: (a boolean, nipype default value: True)
                The output of this interface is meant for R, so matrices will be
                reshaped to vectors by default.

Outputs::

        csv_files: (a file name)

.. _nipype.algorithms.misc.MergeCSVFiles:


.. index:: MergeCSVFiles

MergeCSVFiles
-------------

`Link to code <http://github.com/nipy/nipype/tree/e63e055194d62d2bdc4665688261c03a42fd0025/nipype/algorithms/misc.py#L607>`__

This interface is designed to facilitate data loading in the R environment.
It takes input CSV files and merges them into a single CSV file.
If provided, it will also incorporate column heading names into the
resulting CSV file.

CSV files are easily loaded in R, for use in statistical processing.
For further information, see cran.r-project.org/doc/manuals/R-data.pdf

Example
~~~~~~~

>>> from nipype.algorithms import misc
>>> mat2csv = misc.MergeCSVFiles()
>>> mat2csv.inputs.in_files = ['degree.mat','clustering.mat']
>>> mat2csv.inputs.column_headings = ['degree','clustering']
>>> mat2csv.run() # doctest: +SKIP

Inputs::

        [Mandatory]
        in_files: (an existing file name)
                Input comma-separated value (CSV) files

        [Optional]
        column_headings: (a list of items which are a string)
                List of column headings to save in merged CSV file (must be equal to
                number of input files). If left undefined, these will be pulled from
                the input filenames.
        extra_column_heading: (a string)
                New heading to add for the added field.
        extra_field: (a string)
                New field to add to each row. This is useful for saving the group or
                subject ID in the file.
        out_file: (a file name, nipype default value: merged.csv)
                Output filename for merged CSV file
        row_heading_title: (a string, nipype default value: label)
                Column heading for the row headings added
        row_headings: (a list of items which are a string)
                List of row headings to save in merged CSV file (must be equal to
                number of rows in the input files).

Outputs::

        csv_file: (a file name)
                Output CSV file containing columns

.. _nipype.algorithms.misc.MergeROIs:


.. index:: MergeROIs

MergeROIs
---------

`Link to code <http://github.com/nipy/nipype/tree/e63e055194d62d2bdc4665688261c03a42fd0025/nipype/algorithms/misc.py#L1186>`__

Splits a 3D image in small chunks to enable parallel processing.
ROIs keep time series structure in 4D images.

Example
~~~~~~~

>>> from nipype.algorithms import misc
>>> rois = misc.MergeROIs()
>>> rois.inputs.in_files = ['roi%02d.nii' % i for i in xrange(1, 6)]
>>> rois.inputs.in_reference = 'mask.nii'
>>> rois.inputs.in_index = ['roi%02d_idx.npz' % i for i in xrange(1, 6)]
>>> rois.run() # doctest: +SKIP

Inputs::

        [Mandatory]

        [Optional]
        in_files: (an existing file name)
        in_index: (an existing file name)
                array keeping original locations
        in_reference: (an existing file name)
                reference file

Outputs::

        merged_file: (an existing file name)
                the recomposed file

.. _nipype.algorithms.misc.ModifyAffine:


.. index:: ModifyAffine

ModifyAffine
------------

`Link to code <http://github.com/nipy/nipype/tree/e63e055194d62d2bdc4665688261c03a42fd0025/nipype/algorithms/misc.py#L187>`__

Left multiplies the affine matrix with a specified values. Saves the volume
as a nifti file.

Inputs::

        [Mandatory]
        volumes: (an existing file name)
                volumes which affine matrices will be modified

        [Optional]
        ignore_exception: (a boolean, nipype default value: False)
                Print an error message instead of throwing an exception in case the
                interface fails to run
        transformation_matrix: (an array with shape (4, 4), nipype default
                 value: (<bound method Array.copy_default_value of
                 <traits.trait_numeric.Array object at 0x10e678e50>>, (array([[ 1.,
                 0.,  0.,  0.],        [ 0.,  1.,  0.,  0.],        [ 0.,  0.,  1.,
                 0.],        [ 0.,  0.,  0.,  1.]]),), None))
                transformation matrix that will be left multiplied by the affine
                matrix

Outputs::

        transformed_volumes: (a file name)

.. _nipype.algorithms.misc.NormalizeProbabilityMapSet:


.. index:: NormalizeProbabilityMapSet

NormalizeProbabilityMapSet
--------------------------

`Link to code <http://github.com/nipy/nipype/tree/e63e055194d62d2bdc4665688261c03a42fd0025/nipype/algorithms/misc.py#L1084>`__

Returns the input tissue probability maps (tpms, aka volume fractions)
normalized to sum up 1.0 at each voxel within the mask.

.. note:: Please recall this is not a spatial normalization algorithm


Example
~~~~~~~

>>> from nipype.algorithms import misc
>>> normalize = misc.NormalizeProbabilityMapSet()
>>> normalize.inputs.in_files = [ 'tpm_00.nii.gz', 'tpm_01.nii.gz', 'tpm_02.nii.gz' ]
>>> normalize.inputs.in_mask = 'tpms_msk.nii.gz'
>>> normalize.run() # doctest: +SKIP

Inputs::

        [Mandatory]

        [Optional]
        in_files: (an existing file name)
        in_mask: (an existing file name)
                Masked voxels must sum up 1.0, 0.0 otherwise.

Outputs::

        out_files: (an existing file name)
                normalized maps

.. _nipype.algorithms.misc.Overlap:


.. index:: Overlap

Overlap
-------

`Link to code <http://github.com/nipy/nipype/tree/e63e055194d62d2bdc4665688261c03a42fd0025/nipype/algorithms/misc.py#L1456>`__

Calculates various overlap measures between two maps.

.. deprecated:: 0.10.0
   Use :py:class:`nipype.algorithms.metrics.Overlap` instead.

Inputs::

        [Mandatory]
        bg_overlap: (a boolean, nipype default value: False)
                consider zeros as a label
        vol_units: ('voxel' or 'mm', nipype default value: voxel)
                units for volumes
        volume1: (an existing file name)
                Has to have the same dimensions as volume2.
        volume2: (an existing file name)
                Has to have the same dimensions as volume1.

        [Optional]
        ignore_exception: (a boolean, nipype default value: False)
                Print an error message instead of throwing an exception in case the
                interface fails to run
        mask_volume: (an existing file name)
                calculate overlap only within this mask.
        out_file: (a file name, nipype default value: diff.nii)
        weighting: ('none' or 'volume' or 'squared_vol', nipype default
                 value: none)
                'none': no class-overlap weighting is performed. 'volume': computed
                class-overlaps are weighted by class volume 'squared_vol': computed
                class-overlaps are weighted by the squared volume of the class

Outputs::

        dice: (a float)
                averaged dice index
        diff_file: (an existing file name)
                error map of differences
        jaccard: (a float)
                averaged jaccard index
        labels: (a list of items which are an integer)
                detected labels
        roi_di: (a list of items which are a float)
                the Dice index (DI) per ROI
        roi_ji: (a list of items which are a float)
                the Jaccard index (JI) per ROI
        roi_voldiff: (a list of items which are a float)
                volume differences of ROIs
        volume_difference: (a float)
                averaged volume difference

.. _nipype.algorithms.misc.PickAtlas:


.. index:: PickAtlas

PickAtlas
---------

`Link to code <http://github.com/nipy/nipype/tree/e63e055194d62d2bdc4665688261c03a42fd0025/nipype/algorithms/misc.py#L67>`__

Returns ROI masks given an atlas and a list of labels. Supports dilation
and left right masking (assuming the atlas is properly aligned).

Inputs::

        [Mandatory]
        atlas: (an existing file name)
                Location of the atlas that will be used.
        labels: (an integer or a list of items which are an integer)
                Labels of regions that will be included in the mask. Must be
                compatible with the atlas used.

        [Optional]
        dilation_size: (an integer, nipype default value: 0)
                Defines how much the mask will be dilated (expanded in 3D).
        hemi: ('both' or 'left' or 'right', nipype default value: both)
                Restrict the mask to only one hemisphere: left or right
        ignore_exception: (a boolean, nipype default value: False)
                Print an error message instead of throwing an exception in case the
                interface fails to run
        output_file: (a file name)
                Where to store the output mask.

Outputs::

        mask_file: (an existing file name)
                output mask file

.. _nipype.algorithms.misc.SimpleThreshold:


.. index:: SimpleThreshold

SimpleThreshold
---------------

`Link to code <http://github.com/nipy/nipype/tree/e63e055194d62d2bdc4665688261c03a42fd0025/nipype/algorithms/misc.py#L135>`__

Applies a threshold to input volumes

Inputs::

        [Mandatory]
        threshold: (a float)
                volumes to be thresholdedeverything below this value will be set to
                zero
        volumes: (an existing file name)
                volumes to be thresholded

        [Optional]
        ignore_exception: (a boolean, nipype default value: False)
                Print an error message instead of throwing an exception in case the
                interface fails to run

Outputs::

        thresholded_volumes: (an existing file name)
                thresholded volumes

.. _nipype.algorithms.misc.SplitROIs:


.. index:: SplitROIs

SplitROIs
---------

`Link to code <http://github.com/nipy/nipype/tree/e63e055194d62d2bdc4665688261c03a42fd0025/nipype/algorithms/misc.py#L1136>`__

Splits a 3D image in small chunks to enable parallel processing.
ROIs keep time series structure in 4D images.
>>> from nipype.algorithms import misc
>>> rois = misc.SplitROIs()
>>> rois.inputs.in_file = 'diffusion.nii'
>>> rois.inputs.in_mask = 'mask.nii'
>>> rois.run() # doctest: +SKIP

Inputs::

        [Mandatory]
        in_file: (an existing file name)
                file to be splitted

        [Optional]
        in_mask: (an existing file name)
                only process files inside mask
        roi_size: (a tuple of the form: (an integer, an integer, an integer))
                desired ROI size

Outputs::

        out_files: (an existing file name)
                the resulting ROIs
        out_index: (an existing file name)
                arrays keeping original locations
        out_masks: (an existing file name)
                a mask indicating valid values

.. _nipype.algorithms.misc.TSNR:


.. index:: TSNR

TSNR
----

`Link to code <http://github.com/nipy/nipype/tree/e63e055194d62d2bdc4665688261c03a42fd0025/nipype/algorithms/misc.py#L274>`__

Computes the time-course SNR for a time series

Typically you want to run this on a realigned time-series.

Example
~~~~~~~

>>> tsnr = TSNR()
>>> tsnr.inputs.in_file = 'functional.nii'
>>> res = tsnr.run() # doctest: +SKIP

Inputs::

        [Mandatory]
        in_file: (an existing file name)
                realigned 4D file or a list of 3D files

        [Optional]
        ignore_exception: (a boolean, nipype default value: False)
                Print an error message instead of throwing an exception in case the
                interface fails to run
        regress_poly: (an integer >= 1)
                Remove polynomials

Outputs::

        detrended_file: (a file name)
                detrended input file
        mean_file: (an existing file name)
                mean image file
        stddev_file: (an existing file name)
                std dev image file
        tsnr_file: (an existing file name)
                tsnr image file

.. module:: nipype.algorithms.misc


.. _nipype.algorithms.misc.calc_moments:

:func:`calc_moments`
--------------------

`Link to code <http://github.com/nipy/nipype/tree/e63e055194d62d2bdc4665688261c03a42fd0025/nipype/algorithms/misc.py#L946>`__



Returns nth moment (3 for skewness, 4 for kurtosis) of timeseries
(list of values; one per timeseries).

Keyword arguments:
timeseries_file -- text file with white space separated timepoints in rows


.. _nipype.algorithms.misc.makefmtlist:

:func:`makefmtlist`
-------------------

`Link to code <http://github.com/nipy/nipype/tree/e63e055194d62d2bdc4665688261c03a42fd0025/nipype/algorithms/misc.py#L560>`__






.. _nipype.algorithms.misc.maketypelist:

:func:`maketypelist`
--------------------

`Link to code <http://github.com/nipy/nipype/tree/e63e055194d62d2bdc4665688261c03a42fd0025/nipype/algorithms/misc.py#L544>`__






.. _nipype.algorithms.misc.matlab2csv:

:func:`matlab2csv`
------------------

`Link to code <http://github.com/nipy/nipype/tree/e63e055194d62d2bdc4665688261c03a42fd0025/nipype/algorithms/misc.py#L387>`__






.. _nipype.algorithms.misc.merge_csvs:

:func:`merge_csvs`
------------------

`Link to code <http://github.com/nipy/nipype/tree/e63e055194d62d2bdc4665688261c03a42fd0025/nipype/algorithms/misc.py#L494>`__






.. _nipype.algorithms.misc.merge_rois:

:func:`merge_rois`
------------------

`Link to code <http://github.com/nipy/nipype/tree/e63e055194d62d2bdc4665688261c03a42fd0025/nipype/algorithms/misc.py#L1352>`__



Re-builds an image resulting from a parallelized processing


.. _nipype.algorithms.misc.normalize_tpms:

:func:`normalize_tpms`
----------------------

`Link to code <http://github.com/nipy/nipype/tree/e63e055194d62d2bdc4665688261c03a42fd0025/nipype/algorithms/misc.py#L1218>`__



Returns the input tissue probability maps (tpms, aka volume fractions)
normalized to sum up 1.0 at each voxel within the mask.


.. _nipype.algorithms.misc.remove_identical_paths:

:func:`remove_identical_paths`
------------------------------

`Link to code <http://github.com/nipy/nipype/tree/e63e055194d62d2bdc4665688261c03a42fd0025/nipype/algorithms/misc.py#L524>`__






.. _nipype.algorithms.misc.replaceext:

:func:`replaceext`
------------------

`Link to code <http://github.com/nipy/nipype/tree/e63e055194d62d2bdc4665688261c03a42fd0025/nipype/algorithms/misc.py#L378>`__






.. _nipype.algorithms.misc.split_rois:

:func:`split_rois`
------------------

`Link to code <http://github.com/nipy/nipype/tree/e63e055194d62d2bdc4665688261c03a42fd0025/nipype/algorithms/misc.py#L1277>`__



Splits an image in ROIs for parallel processing

