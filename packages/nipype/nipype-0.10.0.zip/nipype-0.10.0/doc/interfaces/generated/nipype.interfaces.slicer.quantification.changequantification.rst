.. AUTO-GENERATED FILE -- DO NOT EDIT!

interfaces.slicer.quantification.changequantification
=====================================================


.. _nipype.interfaces.slicer.quantification.changequantification.IntensityDifferenceMetric:


.. index:: IntensityDifferenceMetric

IntensityDifferenceMetric
-------------------------

`Link to code <http://github.com/nipy/nipype/tree/e63e055194d62d2bdc4665688261c03a42fd0025/nipype/interfaces/slicer/quantification/changequantification.py#L24>`__

Wraps command **IntensityDifferenceMetric **

title:
  Intensity Difference Change Detection (FAST)


category:
  Quantification.ChangeQuantification


description:
  Quantifies the changes between two spatially aligned images based on the pixel-wise difference of image intensities.


version: 0.1

contributor: Andrey Fedorov

acknowledgements:

Inputs::

        [Mandatory]
        terminal_output: ('stream' or 'allatonce' or 'file' or 'none')
                Control terminal output: `stream` - displays to terminal
                immediately, `allatonce` - waits till command is finished to display
                output, `file` - writes output to file, `none` - output is ignored

        [Optional]
        args: (a string)
                Additional parameters to the command
                flag: %s
        baselineSegmentationVolume: (an existing file name)
                Label volume that contains segmentation of the structure of interest
                in the baseline volume.
                flag: %s, position: -3
        baselineVolume: (an existing file name)
                Baseline volume to be compared to
                flag: %s, position: -4
        changingBandSize: (an integer)
                How far (in mm) from the boundary of the segmentation should the
                intensity changes be considered.
                flag: --changingBandSize %d
        environ: (a dictionary with keys which are a value of type 'str' and
                 with values which are a value of type 'str', nipype default value:
                 {})
                Environment variables
        followupVolume: (an existing file name)
                Followup volume to be compare to the baseline
                flag: %s, position: -2
        ignore_exception: (a boolean, nipype default value: False)
                Print an error message instead of throwing an exception in case the
                interface fails to run
        outputVolume: (a boolean or a file name)
                Output volume to keep the results of change quantification.
                flag: %s, position: -1
        reportFileName: (a boolean or a file name)
                Report file name
                flag: --reportFileName %s
        sensitivityThreshold: (a float)
                This parameter should be between 0 and 1, and defines how sensitive
                the metric should be to the intensity changes.
                flag: --sensitivityThreshold %f

Outputs::

        outputVolume: (an existing file name)
                Output volume to keep the results of change quantification.
        reportFileName: (an existing file name)
                Report file name
