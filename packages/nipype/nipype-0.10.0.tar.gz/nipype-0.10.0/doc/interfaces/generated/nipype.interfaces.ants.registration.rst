.. AUTO-GENERATED FILE -- DO NOT EDIT!

interfaces.ants.registration
============================


.. _nipype.interfaces.ants.registration.Registration:


.. index:: Registration

Registration
------------

`Link to code <http://github.com/nipy/nipype/tree/e63e055194d62d2bdc4665688261c03a42fd0025/nipype/interfaces/ants/registration.py#L344>`__

Wraps command **antsRegistration**

Examples
~~~~~~~~
>>> import copy
>>> from nipype.interfaces.ants import Registration
>>> reg = Registration()
>>> reg.inputs.fixed_image = ['fixed1.nii', 'fixed2.nii']
>>> reg.inputs.moving_image = ['moving1.nii', 'moving2.nii']
>>> reg.inputs.output_transform_prefix = "output_"
>>> reg.inputs.initial_moving_transform = 'trans.mat'
>>> reg.inputs.invert_initial_moving_transform = True
>>> reg.inputs.transforms = ['Affine', 'SyN']
>>> reg.inputs.transform_parameters = [(2.0,), (0.25, 3.0, 0.0)]
>>> reg.inputs.number_of_iterations = [[1500, 200], [100, 50, 30]]
>>> reg.inputs.dimension = 3
>>> reg.inputs.write_composite_transform = True
>>> reg.inputs.collapse_output_transforms = False
>>> reg.inputs.metric = ['Mattes']*2
>>> reg.inputs.metric_weight = [1]*2 # Default (value ignored currently by ANTs)
>>> reg.inputs.radius_or_number_of_bins = [32]*2
>>> reg.inputs.sampling_strategy = ['Random', None]
>>> reg.inputs.sampling_percentage = [0.05, None]
>>> reg.inputs.convergence_threshold = [1.e-8, 1.e-9]
>>> reg.inputs.convergence_window_size = [20]*2
>>> reg.inputs.smoothing_sigmas = [[1,0], [2,1,0]]
>>> reg.inputs.sigma_units = ['vox'] * 2
>>> reg.inputs.shrink_factors = [[2,1], [3,2,1]]
>>> reg.inputs.use_estimate_learning_rate_once = [True, True]
>>> reg.inputs.use_histogram_matching = [True, True] # This is the default
>>> reg.inputs.output_warped_image = 'output_warped_image.nii.gz'

>>> reg1 = copy.deepcopy(reg)
>>> reg1.inputs.winsorize_lower_quantile = 0.025
>>> reg1.inputs.collapse_linear_transforms_to_fixed_image_header = False
>>> reg1.cmdline
'antsRegistration --collapse-linear-transforms-to-fixed-image-header 0 --collapse-output-transforms 0 --dimensionality 3 --initial-moving-transform [ trans.mat, 1 ] --interpolation Linear --output [ output_, output_warped_image.nii.gz ] --transform Affine[ 2.0 ] --metric Mattes[ fixed1.nii, moving1.nii, 1, 32, Random, 0.05 ] --convergence [ 1500x200, 1e-08, 20 ] --smoothing-sigmas 1.0x0.0vox --shrink-factors 2x1 --use-estimate-learning-rate-once 1 --use-histogram-matching 1 --transform SyN[ 0.25, 3.0, 0.0 ] --metric Mattes[ fixed1.nii, moving1.nii, 1, 32 ] --convergence [ 100x50x30, 1e-09, 20 ] --smoothing-sigmas 2.0x1.0x0.0vox --shrink-factors 3x2x1 --use-estimate-learning-rate-once 1 --use-histogram-matching 1 --winsorize-image-intensities [ 0.025, 1.0 ]  --write-composite-transform 1'
>>> reg1.run()  #doctest: +SKIP

>>> reg2 = copy.deepcopy(reg)
>>> reg2.inputs.winsorize_upper_quantile = 0.975
>>> reg2.cmdline
'antsRegistration --collapse-linear-transforms-to-fixed-image-header 0 --collapse-output-transforms 0 --dimensionality 3 --initial-moving-transform [ trans.mat, 1 ] --interpolation Linear --output [ output_, output_warped_image.nii.gz ] --transform Affine[ 2.0 ] --metric Mattes[ fixed1.nii, moving1.nii, 1, 32, Random, 0.05 ] --convergence [ 1500x200, 1e-08, 20 ] --smoothing-sigmas 1.0x0.0vox --shrink-factors 2x1 --use-estimate-learning-rate-once 1 --use-histogram-matching 1 --transform SyN[ 0.25, 3.0, 0.0 ] --metric Mattes[ fixed1.nii, moving1.nii, 1, 32 ] --convergence [ 100x50x30, 1e-09, 20 ] --smoothing-sigmas 2.0x1.0x0.0vox --shrink-factors 3x2x1 --use-estimate-learning-rate-once 1 --use-histogram-matching 1 --winsorize-image-intensities [ 0.0, 0.975 ]  --write-composite-transform 1'

>>> reg3 = copy.deepcopy(reg)
>>> reg3.inputs.winsorize_lower_quantile = 0.025
>>> reg3.inputs.winsorize_upper_quantile = 0.975
>>> reg3.cmdline
'antsRegistration --collapse-linear-transforms-to-fixed-image-header 0 --collapse-output-transforms 0 --dimensionality 3 --initial-moving-transform [ trans.mat, 1 ] --interpolation Linear --output [ output_, output_warped_image.nii.gz ] --transform Affine[ 2.0 ] --metric Mattes[ fixed1.nii, moving1.nii, 1, 32, Random, 0.05 ] --convergence [ 1500x200, 1e-08, 20 ] --smoothing-sigmas 1.0x0.0vox --shrink-factors 2x1 --use-estimate-learning-rate-once 1 --use-histogram-matching 1 --transform SyN[ 0.25, 3.0, 0.0 ] --metric Mattes[ fixed1.nii, moving1.nii, 1, 32 ] --convergence [ 100x50x30, 1e-09, 20 ] --smoothing-sigmas 2.0x1.0x0.0vox --shrink-factors 3x2x1 --use-estimate-learning-rate-once 1 --use-histogram-matching 1 --winsorize-image-intensities [ 0.025, 0.975 ]  --write-composite-transform 1'

>>> # Test collapse transforms flag
>>> reg4 = copy.deepcopy(reg)
>>> reg4.inputs.collapse_output_transforms = True
>>> outputs = reg4._list_outputs()
>>> print outputs #doctest: +ELLIPSIS
{'reverse_invert_flags': [True, False], 'inverse_composite_transform': ['.../nipype/testing/data/output_InverseComposite.h5'], 'warped_image': '.../nipype/testing/data/output_warped_image.nii.gz', 'inverse_warped_image': <undefined>, 'forward_invert_flags': [False, False], 'reverse_transforms': ['.../nipype/testing/data/output_0GenericAffine.mat', '.../nipype/testing/data/output_1InverseWarp.nii.gz'], 'composite_transform': ['.../nipype/testing/data/output_Composite.h5'], 'forward_transforms': ['.../nipype/testing/data/output_0GenericAffine.mat', '.../nipype/testing/data/output_1Warp.nii.gz']}
>>> reg4.aggregate_outputs() #doctest: +SKIP

>>> # Test multiple metrics per stage
>>> reg5 = copy.deepcopy(reg)
>>> reg5.inputs.metric = ['CC', ['CC', 'Mattes']]
>>> reg5.inputs.metric_weight = [1, [.5]*2]
>>> reg5.inputs.radius_or_number_of_bins = [4, [32]*2]
>>> reg5.inputs.sampling_strategy = ['Random', None] # use default strategy in second stage
>>> reg5.inputs.sampling_percentage = [0.05, [0.05, 0.10]]
>>> reg5.cmdline
'antsRegistration --collapse-linear-transforms-to-fixed-image-header 0 --collapse-output-transforms 0 --dimensionality 3 --initial-moving-transform [ trans.mat, 1 ] --interpolation Linear --output [ output_, output_warped_image.nii.gz ] --transform Affine[ 2.0 ] --metric CC[ fixed1.nii, moving1.nii, 1, 4, Random, 0.05 ] --convergence [ 1500x200, 1e-08, 20 ] --smoothing-sigmas 1.0x0.0vox --shrink-factors 2x1 --use-estimate-learning-rate-once 1 --use-histogram-matching 1 --transform SyN[ 0.25, 3.0, 0.0 ] --metric CC[ fixed1.nii, moving1.nii, 0.5, 32, None, 0.05 ] --metric Mattes[ fixed1.nii, moving1.nii, 0.5, 32, None, 0.1 ] --convergence [ 100x50x30, 1e-09, 20 ] --smoothing-sigmas 2.0x1.0x0.0vox --shrink-factors 3x2x1 --use-estimate-learning-rate-once 1 --use-histogram-matching 1 --winsorize-image-intensities [ 0.0, 1.0 ]  --write-composite-transform 1'

Inputs::

        [Mandatory]
        fixed_image: (an existing file name)
                image to apply transformation to (generally a coregistered
                functional)
        metric: (a list of items which are 'CC' or 'MeanSquares' or 'Demons'
                 or 'GC' or 'MI' or 'Mattes' or a list of items which are 'CC' or
                 'MeanSquares' or 'Demons' or 'GC' or 'MI' or 'Mattes')
                the metric(s) to use for each stage. Note that multiple metrics per
                stage are not supported in ANTS 1.9.1 and earlier.
        metric_weight: (a list of items which are a float or a list of items
                 which are a float, nipype default value: [1.0])
                the metric weight(s) for each stage. The weights must sum to 1 per
                stage.
                requires: metric
        moving_image: (an existing file name)
                image to apply transformation to (generally a coregistered
                functional)
        shrink_factors: (a list of items which are a list of items which are
                 an integer)
        smoothing_sigmas: (a list of items which are a list of items which
                 are a float)
        terminal_output: ('stream' or 'allatonce' or 'file' or 'none')
                Control terminal output: `stream` - displays to terminal
                immediately, `allatonce` - waits till command is finished to display
                output, `file` - writes output to file, `none` - output is ignored
        transforms: (a list of items which are 'Rigid' or 'Affine' or
                 'CompositeAffine' or 'Similarity' or 'Translation' or 'BSpline' or
                 'GaussianDisplacementField' or 'TimeVaryingVelocityField' or
                 'TimeVaryingBSplineVelocityField' or 'SyN' or 'BSplineSyN' or
                 'Exponential' or 'BSplineExponential')
                flag: %s

        [Optional]
        args: (a string)
                Additional parameters to the command
                flag: %s
        collapse_linear_transforms_to_fixed_image_header: (a boolean, nipype
                 default value: False)
                flag: %s
        collapse_output_transforms: (a boolean, nipype default value: False)
                Collapse output transforms. Specifically, enabling this option
                combines all adjacent linear transforms and composes all adjacent
                displacement field transforms before writing the results to disk.
                flag: --collapse-output-transforms %d
        convergence_threshold: (a list of at least 1 items which are a float,
                 nipype default value: [1e-06])
                requires: number_of_iterations
        convergence_window_size: (a list of at least 1 items which are an
                 integer, nipype default value: [10])
                requires: convergence_threshold
        dimension: (3 or 2, nipype default value: 3)
                image dimension (2 or 3)
                flag: --dimensionality %d
        environ: (a dictionary with keys which are a value of type 'str' and
                 with values which are a value of type 'str', nipype default value:
                 {})
                Environment variables
        fixed_image_mask: (an existing file name)
                mask used to limit registration region
                flag: %s
        ignore_exception: (a boolean, nipype default value: False)
                Print an error message instead of throwing an exception in case the
                interface fails to run
        initial_moving_transform: (an existing file name)
                flag: %s
                mutually_exclusive: initial_moving_transform_com
        initial_moving_transform_com: (0 or 1 or 2)
                Use center of mass for moving transform
                flag: %s
                mutually_exclusive: initial_moving_transform
        interpolation: ('Linear' or 'NearestNeighbor' or 'CosineWindowedSinc'
                 or 'WelchWindowedSinc' or 'HammingWindowedSinc' or
                 'LanczosWindowedSinc' or 'BSpline', nipype default value: Linear)
                flag: %s
        invert_initial_moving_transform: (a boolean)
                mutually_exclusive: initial_moving_transform_com
                requires: initial_moving_transform
        metric_item_trait: ('CC' or 'MeanSquares' or 'Demons' or 'GC' or 'MI'
                 or 'Mattes')
        metric_stage_trait: ('CC' or 'MeanSquares' or 'Demons' or 'GC' or
                 'MI' or 'Mattes' or a list of items which are 'CC' or 'MeanSquares'
                 or 'Demons' or 'GC' or 'MI' or 'Mattes')
        metric_weight_item_trait: (a float)
        metric_weight_stage_trait: (a float or a list of items which are a
                 float)
        moving_image_mask: (an existing file name)
                requires: fixed_image_mask
        num_threads: (an integer, nipype default value: 1)
                Number of ITK threads to use
        number_of_iterations: (a list of items which are a list of items
                 which are an integer)
        output_inverse_warped_image: (a boolean or a file name)
                requires: output_warped_image
        output_transform_prefix: (a string, nipype default value: transform)
                flag: %s
        output_warped_image: (a boolean or a file name)
        radius_bins_item_trait: (an integer)
        radius_bins_stage_trait: (an integer or a list of items which are an
                 integer)
        radius_or_number_of_bins: (a list of items which are an integer or a
                 list of items which are an integer, nipype default value: [5])
                the number of bins in each stage for the MI and Mattes metric, the
                radius for other metrics
                requires: metric_weight
        sampling_percentage: (a list of items which are 0.0 <= a floating
                 point number <= 1.0 or None or a list of items which are 0.0 <= a
                 floating point number <= 1.0 or None)
                the metric sampling percentage(s) to use for each stage
                requires: sampling_strategy
        sampling_percentage_item_trait
        sampling_percentage_stage_trait
        sampling_strategy: (a list of items which are 'None' or 'Regular' or
                 'Random' or None or a list of items which are 'None' or 'Regular'
                 or 'Random' or None)
                the metric sampling strategy (strategies) for each stage
                requires: metric_weight
        sampling_strategy_item_trait
        sampling_strategy_stage_trait
        sigma_units: (a list of items which are 'mm' or 'vox')
                units for smoothing sigmas
                requires: smoothing_sigmas
        transform_parameters: (a list of items which are a float or a tuple
                 of the form: (a float) or a tuple of the form: (a float, a float, a
                 float) or a tuple of the form: (a float, an integer, an integer, an
                 integer))
        use_estimate_learning_rate_once: (a list of items which are a
                 boolean)
        use_histogram_matching: (a boolean or a list of items which are a
                 boolean, nipype default value: True)
        winsorize_lower_quantile: (0.0 <= a floating point number <= 1.0,
                 nipype default value: 0.0)
                The Lower quantile to clip image ranges
                flag: %s
        winsorize_upper_quantile: (0.0 <= a floating point number <= 1.0,
                 nipype default value: 1.0)
                The Upper quantile to clip image ranges
                flag: %s
        write_composite_transform: (a boolean, nipype default value: False)
                flag: --write-composite-transform %d

Outputs::

        composite_transform: (a list of items which are an existing file
                 name)
                Composite transform file
        forward_invert_flags: (a list of items which are a boolean)
                List of flags corresponding to the forward transforms
        forward_transforms: (a list of items which are an existing file name)
                List of output transforms for forward registration
        inverse_composite_transform: (a list of items which are an existing
                 file name)
                Inverse composite transform file
        inverse_warped_image: (a file name)
                Outputs the inverse of the warped image
        reverse_invert_flags: (a list of items which are a boolean)
                List of flags corresponding to the reverse transforms
        reverse_transforms: (a list of items which are an existing file name)
                List of output transforms for reverse registration
        warped_image: (a file name)
                Outputs warped image
