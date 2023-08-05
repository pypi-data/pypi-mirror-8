.. AUTO-GENERATED FILE -- DO NOT EDIT!

interfaces.mrtrix.preprocess
============================


.. _nipype.interfaces.mrtrix.preprocess.DWI2Tensor:


.. index:: DWI2Tensor

DWI2Tensor
----------

`Link to code <http://github.com/nipy/nipype/tree/e63e055194d62d2bdc4665688261c03a42fd0025/nipype/interfaces/mrtrix/preprocess.py#L127>`__

Wraps command **dwi2tensor**

Converts diffusion-weighted images to tensor images.

Example
~~~~~~~

>>> import nipype.interfaces.mrtrix as mrt
>>> dwi2tensor = mrt.DWI2Tensor()
>>> dwi2tensor.inputs.in_file = 'dwi.mif'
>>> dwi2tensor.inputs.encoding_file = 'encoding.txt'
>>> dwi2tensor.cmdline
'dwi2tensor -grad encoding.txt dwi.mif dwi_tensor.mif'
>>> dwi2tensor.run()                                   # doctest: +SKIP

Inputs::

        [Mandatory]
        in_file: (an existing file name)
                Diffusion-weighted images
                flag: %s, position: -2
        terminal_output: ('stream' or 'allatonce' or 'file' or 'none')
                Control terminal output: `stream` - displays to terminal
                immediately, `allatonce` - waits till command is finished to display
                output, `file` - writes output to file, `none` - output is ignored

        [Optional]
        args: (a string)
                Additional parameters to the command
                flag: %s
        debug: (a boolean)
                Display debugging messages.
                flag: -debug, position: 1
        encoding_file: (a file name)
                Encoding file supplied as a 4xN text file with each line is in the
                format [ X Y Z b ], where [ X Y Z ] describe the direction of the
                applied gradient, and b gives the b-value in units (1000 s/mm^2).
                See FSL2MRTrix()
                flag: -grad %s, position: 2
        environ: (a dictionary with keys which are a value of type 'str' and
                 with values which are a value of type 'str', nipype default value:
                 {})
                Environment variables
        ignore_exception: (a boolean, nipype default value: False)
                Print an error message instead of throwing an exception in case the
                interface fails to run
        ignore_slice_by_volume: (a list of from 2 to 2 items which are an
                 integer)
                Requires two values (i.e. [34 1] for [Slice Volume] Ignores the
                image slices specified when computing the tensor. Slice here means
                the z coordinate of the slice to be ignored.
                flag: -ignoreslices %s, position: 2
        ignore_volumes: (a list of at least 1 items which are an integer)
                Requires two values (i.e. [2 5 6] for [Volumes] Ignores the image
                volumes specified when computing the tensor.
                flag: -ignorevolumes %s, position: 2
        out_filename: (a file name)
                Output tensor filename
                flag: %s, position: -1
        quiet: (a boolean)
                Do not display information messages or progress status.
                flag: -quiet, position: 1

Outputs::

        tensor: (an existing file name)
                path/name of output diffusion tensor image

.. _nipype.interfaces.mrtrix.preprocess.Erode:


.. index:: Erode

Erode
-----

`Link to code <http://github.com/nipy/nipype/tree/e63e055194d62d2bdc4665688261c03a42fd0025/nipype/interfaces/mrtrix/preprocess.py#L440>`__

Wraps command **erode**

Erode (or dilates) a mask (i.e. binary) image

Example
~~~~~~~

>>> import nipype.interfaces.mrtrix as mrt
>>> erode = mrt.Erode()
>>> erode.inputs.in_file = 'mask.mif'
>>> erode.run()                                     # doctest: +SKIP

Inputs::

        [Mandatory]
        in_file: (an existing file name)
                Input mask image to be eroded
                flag: %s, position: -2
        terminal_output: ('stream' or 'allatonce' or 'file' or 'none')
                Control terminal output: `stream` - displays to terminal
                immediately, `allatonce` - waits till command is finished to display
                output, `file` - writes output to file, `none` - output is ignored

        [Optional]
        args: (a string)
                Additional parameters to the command
                flag: %s
        debug: (a boolean)
                Display debugging messages.
                flag: -debug, position: 1
        dilate: (a boolean)
                Perform dilation rather than erosion
                flag: -dilate, position: 1
        environ: (a dictionary with keys which are a value of type 'str' and
                 with values which are a value of type 'str', nipype default value:
                 {})
                Environment variables
        ignore_exception: (a boolean, nipype default value: False)
                Print an error message instead of throwing an exception in case the
                interface fails to run
        number_of_passes: (an integer)
                the number of passes (default: 1)
                flag: -npass %s
        out_filename: (a file name)
                Output image filename
                flag: %s, position: -1
        quiet: (a boolean)
                Do not display information messages or progress status.
                flag: -quiet, position: 1

Outputs::

        out_file: (an existing file name)
                the output image

.. _nipype.interfaces.mrtrix.preprocess.GenerateWhiteMatterMask:


.. index:: GenerateWhiteMatterMask

GenerateWhiteMatterMask
-----------------------

`Link to code <http://github.com/nipy/nipype/tree/e63e055194d62d2bdc4665688261c03a42fd0025/nipype/interfaces/mrtrix/preprocess.py#L396>`__

Wraps command **gen_WM_mask**

Generates a white matter probability mask from the DW images.

Example
~~~~~~~

>>> import nipype.interfaces.mrtrix as mrt
>>> genWM = mrt.GenerateWhiteMatterMask()
>>> genWM.inputs.in_file = 'dwi.mif'
>>> genWM.inputs.encoding_file = 'encoding.txt'
>>> genWM.run()                                     # doctest: +SKIP

Inputs::

        [Mandatory]
        binary_mask: (an existing file name)
                Binary brain mask
                flag: %s, position: -2
        encoding_file: (an existing file name)
                Gradient encoding, supplied as a 4xN text file with each line is in
                the format [ X Y Z b ], where [ X Y Z ] describe the direction of
                the applied gradient, and b gives the b-value in units (1000
                s/mm^2). See FSL2MRTrix
                flag: -grad %s, position: 1
        in_file: (an existing file name)
                Diffusion-weighted images
                flag: %s, position: -3
        terminal_output: ('stream' or 'allatonce' or 'file' or 'none')
                Control terminal output: `stream` - displays to terminal
                immediately, `allatonce` - waits till command is finished to display
                output, `file` - writes output to file, `none` - output is ignored

        [Optional]
        args: (a string)
                Additional parameters to the command
                flag: %s
        environ: (a dictionary with keys which are a value of type 'str' and
                 with values which are a value of type 'str', nipype default value:
                 {})
                Environment variables
        ignore_exception: (a boolean, nipype default value: False)
                Print an error message instead of throwing an exception in case the
                interface fails to run
        noise_level_margin: (a float)
                Specify the width of the margin on either side of the image to be
                used to estimate the noise level (default = 10)
                flag: -margin %s
        out_WMProb_filename: (a file name)
                Output WM probability image filename
                flag: %s, position: -1

Outputs::

        WMprobabilitymap: (an existing file name)
                WMprobabilitymap

.. _nipype.interfaces.mrtrix.preprocess.MRConvert:


.. index:: MRConvert

MRConvert
---------

`Link to code <http://github.com/nipy/nipype/tree/e63e055194d62d2bdc4665688261c03a42fd0025/nipype/interfaces/mrtrix/preprocess.py#L43>`__

Wraps command **mrconvert**

Perform conversion between different file types and optionally extract a subset of the input image.

If used correctly, this program can be a very useful workhorse.
In addition to converting images between different formats, it can
be used to extract specific studies from a data set, extract a specific
region of interest, flip the images, or to scale the intensity of the images.

Example
~~~~~~~

>>> import nipype.interfaces.mrtrix as mrt
>>> mrconvert = mrt.MRConvert()
>>> mrconvert.inputs.in_file = 'dwi_FA.mif'
>>> mrconvert.inputs.out_filename = 'dwi_FA.nii'
>>> mrconvert.run()                                 # doctest: +SKIP

Inputs::

        [Mandatory]
        in_file: (an existing file name)
                voxel-order data filename
                flag: %s, position: -2
        terminal_output: ('stream' or 'allatonce' or 'file' or 'none')
                Control terminal output: `stream` - displays to terminal
                immediately, `allatonce` - waits till command is finished to display
                output, `file` - writes output to file, `none` - output is ignored

        [Optional]
        args: (a string)
                Additional parameters to the command
                flag: %s
        environ: (a dictionary with keys which are a value of type 'str' and
                 with values which are a value of type 'str', nipype default value:
                 {})
                Environment variables
        extension: ('mif' or 'nii' or 'float' or 'char' or 'short' or 'int'
                 or 'long' or 'double', nipype default value: mif)
                "i.e. Bfloat". Can be "char", "short", "int", "long", "float" or
                "double"
        extract_at_axis: (1 or 2 or 3)
                "Extract data only at the coordinates specified. This option
                specifies the Axis. Must be used in conjunction with
                extract_at_coordinate.
                flag: -coord %s, position: 1
        extract_at_coordinate: (a list of from 1 to 3 items which are a
                 float)
                "Extract data only at the coordinates specified. This option
                specifies the coordinates. Must be used in conjunction with
                extract_at_axis. Three comma-separated numbers giving the size of
                each voxel in mm.
                flag: %s, position: 2
        ignore_exception: (a boolean, nipype default value: False)
                Print an error message instead of throwing an exception in case the
                interface fails to run
        layout: ('nii' or 'float' or 'char' or 'short' or 'int' or 'long' or
                 'double')
                specify the layout of the data in memory. The actual layout produced
                will depend on whether the output image format can support it.
                flag: -output %s, position: 2
        offset_bias: (a float)
                Apply offset to the intensity values.
                flag: -scale %d, position: 3
        out_filename: (a file name)
                Output filename
                flag: %s, position: -1
        output_datatype: ('nii' or 'float' or 'char' or 'short' or 'int' or
                 'long' or 'double')
                "i.e. Bfloat". Can be "char", "short", "int", "long", "float" or
                "double"
                flag: -output %s, position: 2
        prs: (a boolean)
                Assume that the DW gradients are specified in the PRS frame (Siemens
                DICOM only).
                flag: -prs, position: 3
        replace_NaN_with_zero: (a boolean)
                Replace all NaN values with zero.
                flag: -zero, position: 3
        resample: (a float)
                Apply scaling to the intensity values.
                flag: -scale %d, position: 3
        voxel_dims: (a list of from 3 to 3 items which are a float)
                Three comma-separated numbers giving the size of each voxel in mm.
                flag: -vox %s, position: 3

Outputs::

        converted: (an existing file name)
                path/name of 4D volume in voxel order

.. _nipype.interfaces.mrtrix.preprocess.MRMultiply:


.. index:: MRMultiply

MRMultiply
----------

`Link to code <http://github.com/nipy/nipype/tree/e63e055194d62d2bdc4665688261c03a42fd0025/nipype/interfaces/mrtrix/preprocess.py#L293>`__

Wraps command **mrmult**

Multiplies two images.

Example
~~~~~~~

>>> import nipype.interfaces.mrtrix as mrt
>>> MRmult = mrt.MRMultiply()
>>> MRmult.inputs.in_files = ['dwi.mif', 'dwi_WMProb.mif']
>>> MRmult.run()                                             # doctest: +SKIP

Inputs::

        [Mandatory]
        in_files: (an existing file name)
                Input images to be multiplied
                flag: %s, position: -2
        terminal_output: ('stream' or 'allatonce' or 'file' or 'none')
                Control terminal output: `stream` - displays to terminal
                immediately, `allatonce` - waits till command is finished to display
                output, `file` - writes output to file, `none` - output is ignored

        [Optional]
        args: (a string)
                Additional parameters to the command
                flag: %s
        debug: (a boolean)
                Display debugging messages.
                flag: -debug, position: 1
        environ: (a dictionary with keys which are a value of type 'str' and
                 with values which are a value of type 'str', nipype default value:
                 {})
                Environment variables
        ignore_exception: (a boolean, nipype default value: False)
                Print an error message instead of throwing an exception in case the
                interface fails to run
        out_filename: (a file name)
                Output image filename
                flag: %s, position: -1
        quiet: (a boolean)
                Do not display information messages or progress status.
                flag: -quiet, position: 1

Outputs::

        out_file: (an existing file name)
                the output image of the multiplication

.. _nipype.interfaces.mrtrix.preprocess.MRTransform:


.. index:: MRTransform

MRTransform
-----------

`Link to code <http://github.com/nipy/nipype/tree/e63e055194d62d2bdc4665688261c03a42fd0025/nipype/interfaces/mrtrix/preprocess.py#L593>`__

Wraps command **mrtransform**

Apply spatial transformations or reslice images

Example
~~~~~~~

>>> MRxform = MRTransform()
>>> MRxform.inputs.in_files = 'anat_coreg.mif'
>>> MRxform.run()                                   # doctest: +SKIP

Inputs::

        [Mandatory]
        in_files: (an existing file name)
                Input images to be transformed
                flag: %s, position: -2
        terminal_output: ('stream' or 'allatonce' or 'file' or 'none')
                Control terminal output: `stream` - displays to terminal
                immediately, `allatonce` - waits till command is finished to display
                output, `file` - writes output to file, `none` - output is ignored

        [Optional]
        args: (a string)
                Additional parameters to the command
                flag: %s
        debug: (a boolean)
                Display debugging messages.
                flag: -debug, position: 1
        environ: (a dictionary with keys which are a value of type 'str' and
                 with values which are a value of type 'str', nipype default value:
                 {})
                Environment variables
        flip_x: (a boolean)
                assume the transform is supplied assuming a coordinate system with
                the x-axis reversed relative to the MRtrix convention (i.e. x
                increases from right to left). This is required to handle transform
                matrices produced by FSL's FLIRT command. This is only used in
                conjunction with the -reference option.
                flag: -flipx, position: 1
        ignore_exception: (a boolean, nipype default value: False)
                Print an error message instead of throwing an exception in case the
                interface fails to run
        invert: (a boolean)
                Invert the specified transform before using it
                flag: -inverse, position: 1
        out_filename: (a file name)
                Output image
                flag: %s, position: -1
        quiet: (a boolean)
                Do not display information messages or progress status.
                flag: -quiet, position: 1
        reference_image: (an existing file name)
                in case the transform supplied maps from the input image onto a
                reference image, use this option to specify the reference. Note that
                this implicitly sets the -replace option.
                flag: -reference %s, position: 1
        replace_transform: (a boolean)
                replace the current transform by that specified, rather than
                applying it to the current transform
                flag: -replace, position: 1
        template_image: (an existing file name)
                Reslice the input image to match the specified template image.
                flag: -template %s, position: 1
        transformation_file: (an existing file name)
                The transform to apply, in the form of a 4x4 ascii file.
                flag: -transform %s, position: 1

Outputs::

        out_file: (an existing file name)
                the output image of the transformation

.. _nipype.interfaces.mrtrix.preprocess.MRTrixViewer:


.. index:: MRTrixViewer

MRTrixViewer
------------

`Link to code <http://github.com/nipy/nipype/tree/e63e055194d62d2bdc4665688261c03a42fd0025/nipype/interfaces/mrtrix/preprocess.py#L338>`__

Wraps command **mrview**

Loads the input images in the MRTrix Viewer.

Example
~~~~~~~

>>> import nipype.interfaces.mrtrix as mrt
>>> MRview = mrt.MRTrixViewer()
>>> MRview.inputs.in_files = 'dwi.mif'
>>> MRview.run()                                    # doctest: +SKIP

Inputs::

        [Mandatory]
        in_files: (an existing file name)
                Input images to be viewed
                flag: %s, position: -2
        terminal_output: ('stream' or 'allatonce' or 'file' or 'none')
                Control terminal output: `stream` - displays to terminal
                immediately, `allatonce` - waits till command is finished to display
                output, `file` - writes output to file, `none` - output is ignored

        [Optional]
        args: (a string)
                Additional parameters to the command
                flag: %s
        debug: (a boolean)
                Display debugging messages.
                flag: -debug, position: 1
        environ: (a dictionary with keys which are a value of type 'str' and
                 with values which are a value of type 'str', nipype default value:
                 {})
                Environment variables
        ignore_exception: (a boolean, nipype default value: False)
                Print an error message instead of throwing an exception in case the
                interface fails to run
        quiet: (a boolean)
                Do not display information messages or progress status.
                flag: -quiet, position: 1

Outputs::

        None

.. _nipype.interfaces.mrtrix.preprocess.MedianFilter3D:


.. index:: MedianFilter3D

MedianFilter3D
--------------

`Link to code <http://github.com/nipy/nipype/tree/e63e055194d62d2bdc4665688261c03a42fd0025/nipype/interfaces/mrtrix/preprocess.py#L538>`__

Wraps command **median3D**

Smooth images using a 3x3x3 median filter.

Example
~~~~~~~

>>> import nipype.interfaces.mrtrix as mrt
>>> median3d = mrt.MedianFilter3D()
>>> median3d.inputs.in_file = 'mask.mif'
>>> median3d.run()                                  # doctest: +SKIP

Inputs::

        [Mandatory]
        in_file: (an existing file name)
                Input images to be smoothed
                flag: %s, position: -2
        terminal_output: ('stream' or 'allatonce' or 'file' or 'none')
                Control terminal output: `stream` - displays to terminal
                immediately, `allatonce` - waits till command is finished to display
                output, `file` - writes output to file, `none` - output is ignored

        [Optional]
        args: (a string)
                Additional parameters to the command
                flag: %s
        debug: (a boolean)
                Display debugging messages.
                flag: -debug, position: 1
        environ: (a dictionary with keys which are a value of type 'str' and
                 with values which are a value of type 'str', nipype default value:
                 {})
                Environment variables
        ignore_exception: (a boolean, nipype default value: False)
                Print an error message instead of throwing an exception in case the
                interface fails to run
        out_filename: (a file name)
                Output image filename
                flag: %s, position: -1
        quiet: (a boolean)
                Do not display information messages or progress status.
                flag: -quiet, position: 1

Outputs::

        out_file: (an existing file name)
                the output image

.. _nipype.interfaces.mrtrix.preprocess.Tensor2ApparentDiffusion:


.. index:: Tensor2ApparentDiffusion

Tensor2ApparentDiffusion
------------------------

`Link to code <http://github.com/nipy/nipype/tree/e63e055194d62d2bdc4665688261c03a42fd0025/nipype/interfaces/mrtrix/preprocess.py#L247>`__

Wraps command **tensor2ADC**

Generates a map of the apparent diffusion coefficient (ADC) in each voxel

Example
~~~~~~~

>>> import nipype.interfaces.mrtrix as mrt
>>> tensor2ADC = mrt.Tensor2ApparentDiffusion()
>>> tensor2ADC.inputs.in_file = 'dwi_tensor.mif'
>>> tensor2ADC.run()                                # doctest: +SKIP

Inputs::

        [Mandatory]
        in_file: (an existing file name)
                Diffusion tensor image
                flag: %s, position: -2
        terminal_output: ('stream' or 'allatonce' or 'file' or 'none')
                Control terminal output: `stream` - displays to terminal
                immediately, `allatonce` - waits till command is finished to display
                output, `file` - writes output to file, `none` - output is ignored

        [Optional]
        args: (a string)
                Additional parameters to the command
                flag: %s
        debug: (a boolean)
                Display debugging messages.
                flag: -debug, position: 1
        environ: (a dictionary with keys which are a value of type 'str' and
                 with values which are a value of type 'str', nipype default value:
                 {})
                Environment variables
        ignore_exception: (a boolean, nipype default value: False)
                Print an error message instead of throwing an exception in case the
                interface fails to run
        out_filename: (a file name)
                Output Fractional Anisotropy filename
                flag: %s, position: -1
        quiet: (a boolean)
                Do not display information messages or progress status.
                flag: -quiet, position: 1

Outputs::

        ADC: (an existing file name)
                the output image of the major eigenvectors of the diffusion tensor
                image.

.. _nipype.interfaces.mrtrix.preprocess.Tensor2FractionalAnisotropy:


.. index:: Tensor2FractionalAnisotropy

Tensor2FractionalAnisotropy
---------------------------

`Link to code <http://github.com/nipy/nipype/tree/e63e055194d62d2bdc4665688261c03a42fd0025/nipype/interfaces/mrtrix/preprocess.py#L202>`__

Wraps command **tensor2FA**

Generates a map of the fractional anisotropy in each voxel.

Example
~~~~~~~

>>> import nipype.interfaces.mrtrix as mrt
>>> tensor2FA = mrt.Tensor2FractionalAnisotropy()
>>> tensor2FA.inputs.in_file = 'dwi_tensor.mif'
>>> tensor2FA.run()                                 # doctest: +SKIP

Inputs::

        [Mandatory]
        in_file: (an existing file name)
                Diffusion tensor image
                flag: %s, position: -2
        terminal_output: ('stream' or 'allatonce' or 'file' or 'none')
                Control terminal output: `stream` - displays to terminal
                immediately, `allatonce` - waits till command is finished to display
                output, `file` - writes output to file, `none` - output is ignored

        [Optional]
        args: (a string)
                Additional parameters to the command
                flag: %s
        debug: (a boolean)
                Display debugging messages.
                flag: -debug, position: 1
        environ: (a dictionary with keys which are a value of type 'str' and
                 with values which are a value of type 'str', nipype default value:
                 {})
                Environment variables
        ignore_exception: (a boolean, nipype default value: False)
                Print an error message instead of throwing an exception in case the
                interface fails to run
        out_filename: (a file name)
                Output Fractional Anisotropy filename
                flag: %s, position: -1
        quiet: (a boolean)
                Do not display information messages or progress status.
                flag: -quiet, position: 1

Outputs::

        FA: (an existing file name)
                the output image of the major eigenvectors of the diffusion tensor
                image.

.. _nipype.interfaces.mrtrix.preprocess.Tensor2Vector:


.. index:: Tensor2Vector

Tensor2Vector
-------------

`Link to code <http://github.com/nipy/nipype/tree/e63e055194d62d2bdc4665688261c03a42fd0025/nipype/interfaces/mrtrix/preprocess.py#L157>`__

Wraps command **tensor2vector**

Generates a map of the major eigenvectors of the tensors in each voxel.

Example
~~~~~~~

>>> import nipype.interfaces.mrtrix as mrt
>>> tensor2vector = mrt.Tensor2Vector()
>>> tensor2vector.inputs.in_file = 'dwi_tensor.mif'
>>> tensor2vector.run()                             # doctest: +SKIP

Inputs::

        [Mandatory]
        in_file: (an existing file name)
                Diffusion tensor image
                flag: %s, position: -2
        terminal_output: ('stream' or 'allatonce' or 'file' or 'none')
                Control terminal output: `stream` - displays to terminal
                immediately, `allatonce` - waits till command is finished to display
                output, `file` - writes output to file, `none` - output is ignored

        [Optional]
        args: (a string)
                Additional parameters to the command
                flag: %s
        debug: (a boolean)
                Display debugging messages.
                flag: -debug, position: 1
        environ: (a dictionary with keys which are a value of type 'str' and
                 with values which are a value of type 'str', nipype default value:
                 {})
                Environment variables
        ignore_exception: (a boolean, nipype default value: False)
                Print an error message instead of throwing an exception in case the
                interface fails to run
        out_filename: (a file name)
                Output vector filename
                flag: %s, position: -1
        quiet: (a boolean)
                Do not display information messages or progress status.
                flag: -quiet, position: 1

Outputs::

        vector: (an existing file name)
                the output image of the major eigenvectors of the diffusion tensor
                image.

.. _nipype.interfaces.mrtrix.preprocess.Threshold:


.. index:: Threshold

Threshold
---------

`Link to code <http://github.com/nipy/nipype/tree/e63e055194d62d2bdc4665688261c03a42fd0025/nipype/interfaces/mrtrix/preprocess.py#L488>`__

Wraps command **threshold**

Create bitwise image by thresholding image intensity.

By default, the threshold level is determined using a histogram analysis
to cut out the background. Otherwise, the threshold intensity can be
specified using command line options.
Note that only the first study is used for thresholding.

Example
~~~~~~~

>>> import nipype.interfaces.mrtrix as mrt
>>> thresh = mrt.Threshold()
>>> thresh.inputs.in_file = 'wm_mask.mif'
>>> thresh.run()                                             # doctest: +SKIP

Inputs::

        [Mandatory]
        in_file: (an existing file name)
                The input image to be thresholded
                flag: %s, position: -2
        terminal_output: ('stream' or 'allatonce' or 'file' or 'none')
                Control terminal output: `stream` - displays to terminal
                immediately, `allatonce` - waits till command is finished to display
                output, `file` - writes output to file, `none` - output is ignored

        [Optional]
        absolute_threshold_value: (a float)
                Specify threshold value as absolute intensity.
                flag: -abs %s
        args: (a string)
                Additional parameters to the command
                flag: %s
        debug: (a boolean)
                Display debugging messages.
                flag: -debug, position: 1
        environ: (a dictionary with keys which are a value of type 'str' and
                 with values which are a value of type 'str', nipype default value:
                 {})
                Environment variables
        ignore_exception: (a boolean, nipype default value: False)
                Print an error message instead of throwing an exception in case the
                interface fails to run
        invert: (a boolean)
                Invert output binary mask
                flag: -invert, position: 1
        out_filename: (a file name)
                The output binary image mask.
                flag: %s, position: -1
        percentage_threshold_value: (a float)
                Specify threshold value as a percentage of the peak intensity in the
                input image.
                flag: -percent %s
        quiet: (a boolean)
                Do not display information messages or progress status.
                flag: -quiet, position: 1
        replace_zeros_with_NaN: (a boolean)
                Replace all zero values with NaN
                flag: -nan, position: 1

Outputs::

        out_file: (an existing file name)
                The output binary image mask.
