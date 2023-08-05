.. AUTO-GENERATED FILE -- DO NOT EDIT!

interfaces.slicer.filtering.denoising
=====================================


.. _nipype.interfaces.slicer.filtering.denoising.CurvatureAnisotropicDiffusion:


.. index:: CurvatureAnisotropicDiffusion

CurvatureAnisotropicDiffusion
-----------------------------

`Link to code <http://github.com/nipy/nipype/tree/e63e055194d62d2bdc4665688261c03a42fd0025/nipype/interfaces/slicer/filtering/denoising.py#L58>`__

Wraps command **CurvatureAnisotropicDiffusion **

title: Curvature Anisotropic Diffusion

category: Filtering.Denoising

description: Performs anisotropic diffusion on an image using a modified curvature diffusion equation (MCDE).

MCDE does not exhibit the edge enhancing properties of classic anisotropic diffusion, which can under certain conditions undergo a 'negative' diffusion, which enhances the contrast of edges.  Equations of the form of MCDE always undergo positive diffusion, with the conductance term only varying the strength of that diffusion.

 Qualitatively, MCDE compares well with other non-linear diffusion techniques.  It is less sensitive to contrast than classic Perona-Malik style diffusion, and preserves finer detailed structures in images.  There is a potential speed trade-off for using this function in place of Gradient Anisotropic Diffusion.  Each iteration of the solution takes roughly twice as long.  Fewer iterations, however, may be required to reach an acceptable solution.

version: 0.1.0.$Revision: 19608 $(alpha)

documentation-url: http://wiki.slicer.org/slicerWiki/index.php/Documentation/4.1/Modules/CurvatureAnisotropicDiffusion

contributor: Bill Lorensen (GE)

acknowledgements: This command module was derived from Insight/Examples (copyright) Insight Software Consortium

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
        conductance: (a float)
                Conductance controls the sensitivity of the conductance term. As a
                general rule, the lower the value, the more strongly the filter
                preserves edges. A high value will cause diffusion (smoothing)
                across edges. Note that the number of iterations controls how much
                smoothing is done within regions bounded by edges.
                flag: --conductance %f
        environ: (a dictionary with keys which are a value of type 'str' and
                 with values which are a value of type 'str', nipype default value:
                 {})
                Environment variables
        ignore_exception: (a boolean, nipype default value: False)
                Print an error message instead of throwing an exception in case the
                interface fails to run
        inputVolume: (an existing file name)
                Input volume to be filtered
                flag: %s, position: -2
        iterations: (an integer)
                The more iterations, the more smoothing. Each iteration takes the
                same amount of time. If it takes 10 seconds for one iteration, then
                it will take 100 seconds for 10 iterations. Note that the
                conductance controls how much each iteration smooths across edges.
                flag: --iterations %d
        outputVolume: (a boolean or a file name)
                Output filtered
                flag: %s, position: -1
        timeStep: (a float)
                The time step depends on the dimensionality of the image. In Slicer
                the images are 3D and the default (.0625) time step will provide a
                stable solution.
                flag: --timeStep %f

Outputs::

        outputVolume: (an existing file name)
                Output filtered

.. _nipype.interfaces.slicer.filtering.denoising.GaussianBlurImageFilter:


.. index:: GaussianBlurImageFilter

GaussianBlurImageFilter
-----------------------

`Link to code <http://github.com/nipy/nipype/tree/e63e055194d62d2bdc4665688261c03a42fd0025/nipype/interfaces/slicer/filtering/denoising.py#L95>`__

Wraps command **GaussianBlurImageFilter **

title: Gaussian Blur Image Filter

category: Filtering.Denoising

description: Apply a gaussian blurr to an image

version: 0.1.0.$Revision: 1.1 $(alpha)

documentation-url: http://wiki.slicer.org/slicerWiki/index.php/Documentation/4.1/Modules/GaussianBlurImageFilter

contributor: Julien Jomier (Kitware), Stephen Aylward (Kitware)

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
        inputVolume: (an existing file name)
                Input volume
                flag: %s, position: -2
        outputVolume: (a boolean or a file name)
                Blurred Volume
                flag: %s, position: -1
        sigma: (a float)
                Sigma value in physical units (e.g., mm) of the Gaussian kernel
                flag: --sigma %f

Outputs::

        outputVolume: (an existing file name)
                Blurred Volume

.. _nipype.interfaces.slicer.filtering.denoising.GradientAnisotropicDiffusion:


.. index:: GradientAnisotropicDiffusion

GradientAnisotropicDiffusion
----------------------------

`Link to code <http://github.com/nipy/nipype/tree/e63e055194d62d2bdc4665688261c03a42fd0025/nipype/interfaces/slicer/filtering/denoising.py#L21>`__

Wraps command **GradientAnisotropicDiffusion **

title: Gradient Anisotropic Diffusion

category: Filtering.Denoising

description: Runs gradient anisotropic diffusion on a volume.

Anisotropic diffusion methods reduce noise (or unwanted detail) in images while preserving specific image features, like edges.  For many applications, there is an assumption that light-dark transitions (edges) are interesting.  Standard isotropic diffusion methods move and blur light-dark boundaries.  Anisotropic diffusion methods are formulated to specifically preserve edges. The conductance term for this implementation is a function of the gradient magnitude of the image at each point, reducing the strength of diffusion at edges. The numerical implementation of this equation is similar to that described in the Perona-Malik paper, but uses a more robust technique for gradient magnitude estimation and has been generalized to N-dimensions.

version: 0.1.0.$Revision: 19608 $(alpha)

documentation-url: http://wiki.slicer.org/slicerWiki/index.php/Documentation/4.1/Modules/GradientAnisotropicDiffusion

contributor: Bill Lorensen (GE)

acknowledgements: This command module was derived from Insight/Examples (copyright) Insight Software Consortium

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
        conductance: (a float)
                Conductance controls the sensitivity of the conductance term. As a
                general rule, the lower the value, the more strongly the filter
                preserves edges. A high value will cause diffusion (smoothing)
                across edges. Note that the number of iterations controls how much
                smoothing is done within regions bounded by edges.
                flag: --conductance %f
        environ: (a dictionary with keys which are a value of type 'str' and
                 with values which are a value of type 'str', nipype default value:
                 {})
                Environment variables
        ignore_exception: (a boolean, nipype default value: False)
                Print an error message instead of throwing an exception in case the
                interface fails to run
        inputVolume: (an existing file name)
                Input volume to be filtered
                flag: %s, position: -2
        iterations: (an integer)
                The more iterations, the more smoothing. Each iteration takes the
                same amount of time. If it takes 10 seconds for one iteration, then
                it will take 100 seconds for 10 iterations. Note that the
                conductance controls how much each iteration smooths across edges.
                flag: --iterations %d
        outputVolume: (a boolean or a file name)
                Output filtered
                flag: %s, position: -1
        timeStep: (a float)
                The time step depends on the dimensionality of the image. In Slicer
                the images are 3D and the default (.0625) time step will provide a
                stable solution.
                flag: --timeStep %f

Outputs::

        outputVolume: (an existing file name)
                Output filtered

.. _nipype.interfaces.slicer.filtering.denoising.MedianImageFilter:


.. index:: MedianImageFilter

MedianImageFilter
-----------------

`Link to code <http://github.com/nipy/nipype/tree/e63e055194d62d2bdc4665688261c03a42fd0025/nipype/interfaces/slicer/filtering/denoising.py#L128>`__

Wraps command **MedianImageFilter **

title: Median Image Filter

category: Filtering.Denoising

description: The MedianImageFilter is commonly used as a robust approach for noise reduction. This filter is particularly efficient against "salt-and-pepper" noise. In other words, it is robust to the presence of gray-level outliers. MedianImageFilter computes the value of each output pixel as the statistical median of the neighborhood of values around the corresponding input pixel.

version: 0.1.0.$Revision: 19608 $(alpha)

documentation-url: http://wiki.slicer.org/slicerWiki/index.php/Documentation/4.1/Modules/MedianImageFilter

contributor: Bill Lorensen (GE)

acknowledgements: This command module was derived from Insight/Examples/Filtering/MedianImageFilter (copyright) Insight Software Consortium

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
        inputVolume: (an existing file name)
                Input volume to be filtered
                flag: %s, position: -2
        neighborhood: (an integer)
                The size of the neighborhood in each dimension
                flag: --neighborhood %s
        outputVolume: (a boolean or a file name)
                Output filtered
                flag: %s, position: -1

Outputs::

        outputVolume: (an existing file name)
                Output filtered
