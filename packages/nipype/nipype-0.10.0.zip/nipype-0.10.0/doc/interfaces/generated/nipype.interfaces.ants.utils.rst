.. AUTO-GENERATED FILE -- DO NOT EDIT!

interfaces.ants.utils
=====================


.. _nipype.interfaces.ants.utils.AverageAffineTransform:


.. index:: AverageAffineTransform

AverageAffineTransform
----------------------

`Link to code <http://github.com/nipy/nipype/tree/e63e055194d62d2bdc4665688261c03a42fd0025/nipype/interfaces/ants/utils.py#L31>`__

Wraps command **AverageAffineTransform**

Examples
~~~~~~~~
>>> from nipype.interfaces.ants import AverageAffineTransform
>>> avg = AverageAffineTransform()
>>> avg.inputs.dimension = 3
>>> avg.inputs.transforms = ['trans.mat', 'func_to_struct.mat']
>>> avg.inputs.output_affine_transform = 'MYtemplatewarp.mat'
>>> avg.cmdline
'AverageAffineTransform 3 MYtemplatewarp.mat trans.mat func_to_struct.mat'

Inputs::

        [Mandatory]
        dimension: (3 or 2)
                image dimension (2 or 3)
                flag: %d, position: 0
        output_affine_transform: (a file name)
                Outputfname.txt: the name of the resulting transform.
                flag: %s, position: 1
        terminal_output: ('stream' or 'allatonce' or 'file' or 'none')
                Control terminal output: `stream` - displays to terminal
                immediately, `allatonce` - waits till command is finished to display
                output, `file` - writes output to file, `none` - output is ignored
        transforms: (an existing file name)
                transforms to average
                flag: %s, position: 3

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
        num_threads: (an integer, nipype default value: 1)
                Number of ITK threads to use

Outputs::

        affine_transform: (an existing file name)
                average transform file

.. _nipype.interfaces.ants.utils.AverageImages:


.. index:: AverageImages

AverageImages
-------------

`Link to code <http://github.com/nipy/nipype/tree/e63e055194d62d2bdc4665688261c03a42fd0025/nipype/interfaces/ants/utils.py#L70>`__

Wraps command **AverageImages**

Examples
~~~~~~~~
>>> from nipype.interfaces.ants import AverageImages
>>> avg = AverageImages()
>>> avg.inputs.dimension = 3
>>> avg.inputs.output_average_image = "average.nii.gz"
>>> avg.inputs.normalize = True
>>> avg.inputs.images = ['rc1s1.nii', 'rc1s1.nii']
>>> avg.cmdline
'AverageImages 3 average.nii.gz 1 rc1s1.nii rc1s1.nii'

Inputs::

        [Mandatory]
        dimension: (3 or 2)
                image dimension (2 or 3)
                flag: %d, position: 0
        images: (an existing file name)
                image to apply transformation to (generally a coregistered
                functional)
                flag: %s, position: 3
        normalize: (a boolean)
                Normalize: if true, the 2nd imageis divided by its mean. This will
                select the largest image to average into.
                flag: %d, position: 2
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
        num_threads: (an integer, nipype default value: 1)
                Number of ITK threads to use
        output_average_image: (a file name, nipype default value:
                 average.nii)
                the name of the resulting image.
                flag: %s, position: 1

Outputs::

        output_average_image: (an existing file name)
                average image file

.. _nipype.interfaces.ants.utils.JacobianDeterminant:


.. index:: JacobianDeterminant

JacobianDeterminant
-------------------

`Link to code <http://github.com/nipy/nipype/tree/e63e055194d62d2bdc4665688261c03a42fd0025/nipype/interfaces/ants/utils.py#L161>`__

Wraps command **ANTSJacobian**

Examples
~~~~~~~~
>>> from nipype.interfaces.ants import JacobianDeterminant
>>> jacobian = JacobianDeterminant()
>>> jacobian.inputs.dimension = 3
>>> jacobian.inputs.warp_file = 'ants_Warp.nii.gz'
>>> jacobian.inputs.output_prefix = 'Sub001_'
>>> jacobian.inputs.use_log = 1
>>> jacobian.cmdline
'ANTSJacobian 3 ants_Warp.nii.gz Sub001_ 1'

Inputs::

        [Mandatory]
        dimension: (3 or 2)
                image dimension (2 or 3)
                flag: %d, position: 0
        terminal_output: ('stream' or 'allatonce' or 'file' or 'none')
                Control terminal output: `stream` - displays to terminal
                immediately, `allatonce` - waits till command is finished to display
                output, `file` - writes output to file, `none` - output is ignored
        warp_file: (an existing file name)
                input warp file
                flag: %s, position: 1

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
        norm_by_total: (0 or 1)
                normalize jacobian by total in mask to adjust for head size
                flag: %d, position: 5
        num_threads: (an integer, nipype default value: 1)
                Number of ITK threads to use
        output_prefix: (a file name)
                prefix of the output image filename: PREFIX(log)jacobian.nii.gz
                flag: %s, position: 2
        projection_vector: (a list of items which are a float)
                vector to project warp against
                flag: %s, position: 6
        template_mask: (an existing file name)
                template mask to adjust for head size
                flag: %s, position: 4
        use_log: (0 or 1)
                log transform the jacobian determinant
                flag: %d, position: 3

Outputs::

        jacobian_image: (an existing file name)
                (log transformed) jacobian image

.. _nipype.interfaces.ants.utils.MultiplyImages:


.. index:: MultiplyImages

MultiplyImages
--------------

`Link to code <http://github.com/nipy/nipype/tree/e63e055194d62d2bdc4665688261c03a42fd0025/nipype/interfaces/ants/utils.py#L109>`__

Wraps command **MultiplyImages**

Examples
~~~~~~~~
>>> from nipype.interfaces.ants import MultiplyImages
>>> test = MultiplyImages()
>>> test.inputs.dimension = 3
>>> test.inputs.first_input = 'moving2.nii'
>>> test.inputs.second_input = 0.25
>>> test.inputs.output_product_image = "out.nii"
>>> test.cmdline
'MultiplyImages 3 moving2.nii 0.25 out.nii'

Inputs::

        [Mandatory]
        dimension: (3 or 2)
                image dimension (2 or 3)
                flag: %d, position: 0
        first_input: (an existing file name)
                image 1
                flag: %s, position: 1
        output_product_image: (a file name)
                Outputfname.nii.gz: the name of the resulting image.
                flag: %s, position: 3
        second_input: (an existing file name or a float)
                image 2 or multiplication weight
                flag: %s, position: 2
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
        num_threads: (an integer, nipype default value: 1)
                Number of ITK threads to use

Outputs::

        output_product_image: (an existing file name)
                average image file
