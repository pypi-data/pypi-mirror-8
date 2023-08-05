.. AUTO-GENERATED FILE -- DO NOT EDIT!

interfaces.slicer.filtering.arithmetic
======================================


.. _nipype.interfaces.slicer.filtering.arithmetic.AddScalarVolumes:


.. index:: AddScalarVolumes

AddScalarVolumes
----------------

`Link to code <http://github.com/nipy/nipype/tree/e63e055194d62d2bdc4665688261c03a42fd0025/nipype/interfaces/slicer/filtering/arithmetic.py#L123>`__

Wraps command **AddScalarVolumes **

title: Add Scalar Volumes

category: Filtering.Arithmetic

description: Adds two images. Although all image types are supported on input, only signed types are produced. The two images do not have to have the same dimensions.

version: 0.1.0.$Revision: 19608 $(alpha)

documentation-url: http://slicer.org/slicerWiki/index.php/Documentation/4.1/Modules/Add

contributor: Bill Lorensen (GE)

acknowledgements: This work is part of the National Alliance for Medical Image Computing (NAMIC), funded by the National Institutes of Health through the NIH Roadmap for Medical Research, Grant U54 EB005149.

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
        environ: (a dictionary with keys which are a value of type 'str' and
                 with values which are a value of type 'str', nipype default value:
                 {})
                Environment variables
        ignore_exception: (a boolean, nipype default value: False)
                Print an error message instead of throwing an exception in case the
                interface fails to run
        inputVolume1: (an existing file name)
                Input volume 1
                flag: %s, position: -3
        inputVolume2: (an existing file name)
                Input volume 2
                flag: %s, position: -2
        order: ('0' or '1' or '2' or '3')
                Interpolation order if two images are in different coordinate frames
                or have different sampling.
                flag: --order %s
        outputVolume: (a boolean or a file name)
                Volume1 + Volume2
                flag: %s, position: -1

Outputs::

        outputVolume: (an existing file name)
                Volume1 + Volume2

.. _nipype.interfaces.slicer.filtering.arithmetic.CastScalarVolume:


.. index:: CastScalarVolume

CastScalarVolume
----------------

`Link to code <http://github.com/nipy/nipype/tree/e63e055194d62d2bdc4665688261c03a42fd0025/nipype/interfaces/slicer/filtering/arithmetic.py#L156>`__

Wraps command **CastScalarVolume **

title: Cast Scalar Volume

category: Filtering.Arithmetic

description: Cast a volume to a given data type.
Use at your own risk when casting an input volume into a lower precision type!
Allows casting to the same type as the input volume.

version: 0.1.0.$Revision: 2104 $(alpha)

documentation-url: http://wiki.slicer.org/slicerWiki/index.php/Documentation/4.1/Modules/Cast

contributor: Nicole Aucoin (SPL, BWH), Ron Kikinis (SPL, BWH)

acknowledgements: This work is part of the National Alliance for Medical Image Computing (NAMIC), funded by the National Institutes of Health through the NIH Roadmap for Medical Research, Grant U54 EB005149.

Inputs::

        [Mandatory]
        terminal_output: ('stream' or 'allatonce' or 'file' or 'none')
                Control terminal output: `stream` - displays to terminal
                immediately, `allatonce` - waits till command is finished to display
                output, `file` - writes output to file, `none` - output is ignored

        [Optional]
        InputVolume: (an existing file name)
                Input volume, the volume to cast.
                flag: %s, position: -2
        OutputVolume: (a boolean or a file name)
                Output volume, cast to the new type.
                flag: %s, position: -1
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
        type: ('Char' or 'UnsignedChar' or 'Short' or 'UnsignedShort' or
                 'Int' or 'UnsignedInt' or 'Float' or 'Double')
                Type for the new output volume.
                flag: --type %s

Outputs::

        OutputVolume: (an existing file name)
                Output volume, cast to the new type.

.. _nipype.interfaces.slicer.filtering.arithmetic.MaskScalarVolume:


.. index:: MaskScalarVolume

MaskScalarVolume
----------------

`Link to code <http://github.com/nipy/nipype/tree/e63e055194d62d2bdc4665688261c03a42fd0025/nipype/interfaces/slicer/filtering/arithmetic.py#L55>`__

Wraps command **MaskScalarVolume **

title: Mask Scalar Volume

category: Filtering.Arithmetic

description: Masks two images. The output image is set to 0 everywhere except where the chosen label from the mask volume is present, at which point it will retain it's original values. Although all image types are supported on input, only signed types are produced. The two images do not have to have the same dimensions.

version: 0.1.0.$Revision: 8595 $(alpha)

documentation-url: http://wiki.slicer.org/slicerWiki/index.php/Documentation/4.1/Modules/Mask

contributor: Nicole Aucoin (SPL, BWH), Ron Kikinis (SPL, BWH)

acknowledgements: This work is part of the National Alliance for Medical Image Computing (NAMIC), funded by the National Institutes of Health through the NIH Roadmap for Medical Research, Grant U54 EB005149.

Inputs::

        [Mandatory]
        terminal_output: ('stream' or 'allatonce' or 'file' or 'none')
                Control terminal output: `stream` - displays to terminal
                immediately, `allatonce` - waits till command is finished to display
                output, `file` - writes output to file, `none` - output is ignored

        [Optional]
        InputVolume: (an existing file name)
                Input volume to be masked
                flag: %s, position: -3
        MaskVolume: (an existing file name)
                Label volume containing the mask
                flag: %s, position: -2
        OutputVolume: (a boolean or a file name)
                Output volume: Input Volume masked by label value from Mask Volume
                flag: %s, position: -1
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
        label: (an integer)
                Label value in the Mask Volume to use as the mask
                flag: --label %d
        replace: (an integer)
                Value to use for the output volume outside of the mask
                flag: --replace %d

Outputs::

        OutputVolume: (an existing file name)
                Output volume: Input Volume masked by label value from Mask Volume

.. _nipype.interfaces.slicer.filtering.arithmetic.MultiplyScalarVolumes:


.. index:: MultiplyScalarVolumes

MultiplyScalarVolumes
---------------------

`Link to code <http://github.com/nipy/nipype/tree/e63e055194d62d2bdc4665688261c03a42fd0025/nipype/interfaces/slicer/filtering/arithmetic.py#L20>`__

Wraps command **MultiplyScalarVolumes **

title: Multiply Scalar Volumes

category: Filtering.Arithmetic

description: Multiplies two images. Although all image types are supported on input, only signed types are produced. The two images do not have to have the same dimensions.

version: 0.1.0.$Revision: 8595 $(alpha)

documentation-url: http://wiki.slicer.org/slicerWiki/index.php/Documentation/4.1/Modules/Multiply

contributor: Bill Lorensen (GE)

acknowledgements: This work is part of the National Alliance for Medical Image Computing (NAMIC), funded by the National Institutes of Health through the NIH Roadmap for Medical Research, Grant U54 EB005149.

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
        environ: (a dictionary with keys which are a value of type 'str' and
                 with values which are a value of type 'str', nipype default value:
                 {})
                Environment variables
        ignore_exception: (a boolean, nipype default value: False)
                Print an error message instead of throwing an exception in case the
                interface fails to run
        inputVolume1: (an existing file name)
                Input volume 1
                flag: %s, position: -3
        inputVolume2: (an existing file name)
                Input volume 2
                flag: %s, position: -2
        order: ('0' or '1' or '2' or '3')
                Interpolation order if two images are in different coordinate frames
                or have different sampling.
                flag: --order %s
        outputVolume: (a boolean or a file name)
                Volume1 * Volume2
                flag: %s, position: -1

Outputs::

        outputVolume: (an existing file name)
                Volume1 * Volume2

.. _nipype.interfaces.slicer.filtering.arithmetic.SubtractScalarVolumes:


.. index:: SubtractScalarVolumes

SubtractScalarVolumes
---------------------

`Link to code <http://github.com/nipy/nipype/tree/e63e055194d62d2bdc4665688261c03a42fd0025/nipype/interfaces/slicer/filtering/arithmetic.py#L89>`__

Wraps command **SubtractScalarVolumes **

title: Subtract Scalar Volumes

category: Filtering.Arithmetic

description: Subtracts two images. Although all image types are supported on input, only signed types are produced. The two images do not have to have the same dimensions.

version: 0.1.0.$Revision: 19608 $(alpha)

documentation-url: http://wiki.slicer.org/slicerWiki/index.php/Documentation/4.1/Modules/Subtract

contributor: Bill Lorensen (GE)

acknowledgements: This work is part of the National Alliance for Medical Image Computing (NAMIC), funded by the National Institutes of Health through the NIH Roadmap for Medical Research, Grant U54 EB005149.

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
        environ: (a dictionary with keys which are a value of type 'str' and
                 with values which are a value of type 'str', nipype default value:
                 {})
                Environment variables
        ignore_exception: (a boolean, nipype default value: False)
                Print an error message instead of throwing an exception in case the
                interface fails to run
        inputVolume1: (an existing file name)
                Input volume 1
                flag: %s, position: -3
        inputVolume2: (an existing file name)
                Input volume 2
                flag: %s, position: -2
        order: ('0' or '1' or '2' or '3')
                Interpolation order if two images are in different coordinate frames
                or have different sampling.
                flag: --order %s
        outputVolume: (a boolean or a file name)
                Volume1 - Volume2
                flag: %s, position: -1

Outputs::

        outputVolume: (an existing file name)
                Volume1 - Volume2
