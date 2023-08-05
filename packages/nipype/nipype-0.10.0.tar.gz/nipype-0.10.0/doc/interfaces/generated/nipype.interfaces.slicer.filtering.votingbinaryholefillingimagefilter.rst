.. AUTO-GENERATED FILE -- DO NOT EDIT!

interfaces.slicer.filtering.votingbinaryholefillingimagefilter
==============================================================


.. _nipype.interfaces.slicer.filtering.votingbinaryholefillingimagefilter.VotingBinaryHoleFillingImageFilter:


.. index:: VotingBinaryHoleFillingImageFilter

VotingBinaryHoleFillingImageFilter
----------------------------------

`Link to code <http://github.com/nipy/nipype/tree/e63e055194d62d2bdc4665688261c03a42fd0025/nipype/interfaces/slicer/filtering/votingbinaryholefillingimagefilter.py#L22>`__

Wraps command **VotingBinaryHoleFillingImageFilter **

title: Voting Binary Hole Filling Image Filter

category: Filtering

description: Applies a voting operation in order to fill-in cavities. This can be used for smoothing contours and for filling holes in binary images. This technique is used frequently when segmenting complete organs that may have ducts or vasculature that may not have been included in the initial segmentation, e.g. lungs, kidneys, liver.

version: 0.1.0.$Revision: 19608 $(alpha)

documentation-url: http://wiki.slicer.org/slicerWiki/index.php/Documentation/4.1/Modules/VotingBinaryHoleFillingImageFilter

contributor: Bill Lorensen (GE)

acknowledgements: This command module was derived from Insight/Examples/Filtering/VotingBinaryHoleFillingImageFilter (copyright) Insight Software Consortium

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
        background: (an integer)
                The value associated with the background (not object)
                flag: --background %d
        environ: (a dictionary with keys which are a value of type 'str' and
                 with values which are a value of type 'str', nipype default value:
                 {})
                Environment variables
        foreground: (an integer)
                The value associated with the foreground (object)
                flag: --foreground %d
        ignore_exception: (a boolean, nipype default value: False)
                Print an error message instead of throwing an exception in case the
                interface fails to run
        inputVolume: (an existing file name)
                Input volume to be filtered
                flag: %s, position: -2
        majorityThreshold: (an integer)
                The number of pixels over 50% that will decide whether an OFF pixel
                will become ON or not. For example, if the neighborhood of a pixel
                has 124 pixels (excluding itself), the 50% will be 62, and if you
                set a Majority threshold of 5, that means that the filter will
                require 67 or more neighbor pixels to be ON in order to switch the
                current OFF pixel to ON.
                flag: --majorityThreshold %d
        outputVolume: (a boolean or a file name)
                Output filtered
                flag: %s, position: -1
        radius: (an integer)
                The radius of a hole to be filled
                flag: --radius %s

Outputs::

        outputVolume: (an existing file name)
                Output filtered
