.. AUTO-GENERATED FILE -- DO NOT EDIT!

interfaces.fsl.preprocess
=========================


.. _nipype.interfaces.fsl.preprocess.ApplyWarp:


.. index:: ApplyWarp

ApplyWarp
---------

`Link to code <http://github.com/nipy/nipype/tree/e63e055194d62d2bdc4665688261c03a42fd0025/nipype/interfaces/fsl/preprocess.py#L983>`__

Wraps command **applywarp**

Use FSL's applywarp to apply the results of a FNIRT registration

Examples
~~~~~~~~
>>> from nipype.interfaces import fsl
>>> from nipype.testing import example_data
>>> aw = fsl.ApplyWarp()
>>> aw.inputs.in_file = example_data('structural.nii')
>>> aw.inputs.ref_file = example_data('mni.nii')
>>> aw.inputs.field_file = 'my_coefficients_filed.nii' #doctest: +SKIP
>>> res = aw.run() #doctest: +SKIP

Inputs::

        [Mandatory]
        in_file: (an existing file name)
                image to be warped
                flag: --in=%s, position: 0
        ref_file: (an existing file name)
                reference image
                flag: --ref=%s, position: 1
        terminal_output: ('stream' or 'allatonce' or 'file' or 'none')
                Control terminal output: `stream` - displays to terminal
                immediately, `allatonce` - waits till command is finished to display
                output, `file` - writes output to file, `none` - output is ignored

        [Optional]
        abswarp: (a boolean)
                treat warp field as absolute: x' = w(x)
                flag: --abs
                mutually_exclusive: relwarp
        args: (a string)
                Additional parameters to the command
                flag: %s
        datatype: ('char' or 'short' or 'int' or 'float' or 'double')
                Force output data type [char short int float double].
                flag: --datatype=%s
        environ: (a dictionary with keys which are a value of type 'str' and
                 with values which are a value of type 'str', nipype default value:
                 {})
                Environment variables
        field_file: (an existing file name)
                file containing warp field
                flag: --warp=%s
        ignore_exception: (a boolean, nipype default value: False)
                Print an error message instead of throwing an exception in case the
                interface fails to run
        interp: ('nn' or 'trilinear' or 'sinc' or 'spline')
                interpolation method
                flag: --interp=%s, position: -2
        mask_file: (an existing file name)
                filename for mask image (in reference space)
                flag: --mask=%s
        out_file: (a file name)
                output filename
                flag: --out=%s, position: 2
        output_type: ('NIFTI_PAIR' or 'NIFTI_PAIR_GZ' or 'NIFTI_GZ' or
                 'NIFTI')
                FSL output type
        postmat: (an existing file name)
                filename for post-transform (affine matrix)
                flag: --postmat=%s
        premat: (an existing file name)
                filename for pre-transform (affine matrix)
                flag: --premat=%s
        relwarp: (a boolean)
                treat warp field as relative: x' = x + w(x)
                flag: --rel, position: -1
                mutually_exclusive: abswarp
        superlevel: ('a' or an integer)
                level of intermediary supersampling, a for 'automatic' or integer
                level. Default = 2
                flag: --superlevel=%s
        supersample: (a boolean)
                intermediary supersampling of output, default is off
                flag: --super

Outputs::

        out_file: (an existing file name)
                Warped output file

.. _nipype.interfaces.fsl.preprocess.ApplyXfm:


.. index:: ApplyXfm

ApplyXfm
--------

`Link to code <http://github.com/nipy/nipype/tree/e63e055194d62d2bdc4665688261c03a42fd0025/nipype/interfaces/fsl/preprocess.py#L570>`__

Wraps command **flirt**

Currently just a light wrapper around FLIRT,
with no modifications

ApplyXfm is used to apply an existing tranform to an image


Examples
~~~~~~~~

>>> import nipype.interfaces.fsl as fsl
>>> from nipype.testing import example_data
>>> applyxfm = fsl.ApplyXfm()
>>> applyxfm.inputs.in_file = example_data('structural.nii')
>>> applyxfm.inputs.in_matrix_file = example_data('trans.mat')
>>> applyxfm.inputs.out_file = 'newfile.nii'
>>> applyxfm.inputs.reference = example_data('mni.nii')
>>> applyxfm.inputs.apply_xfm = True
>>> result = applyxfm.run() # doctest: +SKIP

Inputs::

        [Mandatory]
        in_file: (an existing file name)
                input file
                flag: -in %s, position: 0
        reference: (an existing file name)
                reference file
                flag: -ref %s, position: 1
        terminal_output: ('stream' or 'allatonce' or 'file' or 'none')
                Control terminal output: `stream` - displays to terminal
                immediately, `allatonce` - waits till command is finished to display
                output, `file` - writes output to file, `none` - output is ignored

        [Optional]
        angle_rep: ('quaternion' or 'euler')
                representation of rotation angles
                flag: -anglerep %s
        apply_isoxfm: (a float)
                as applyxfm but forces isotropic resampling
                flag: -applyisoxfm %f
                mutually_exclusive: apply_xfm
        apply_xfm: (a boolean, nipype default value: True)
                apply transformation supplied by in_matrix_file
                flag: -applyxfm
                requires: in_matrix_file
        args: (a string)
                Additional parameters to the command
                flag: %s
        bbrslope: (a float)
                value of bbr slope
                flag: -bbrslope %f
        bbrtype: ('signed' or 'global_abs' or 'local_abs')
                type of bbr cost function: signed [default], global_abs, local_abs
                flag: -bbrtype %s
        bgvalue: (a float)
                use specified background value for points outside FOV
                flag: -setbackground %f
        bins: (an integer)
                number of histogram bins
                flag: -bins %d
        coarse_search: (an integer)
                coarse search delta angle
                flag: -coarsesearch %d
        cost: ('mutualinfo' or 'corratio' or 'normcorr' or 'normmi' or
                 'leastsq' or 'labeldiff' or 'bbr')
                cost function
                flag: -cost %s
        cost_func: ('mutualinfo' or 'corratio' or 'normcorr' or 'normmi' or
                 'leastsq' or 'labeldiff' or 'bbr')
                cost function
                flag: -searchcost %s
        datatype: ('char' or 'short' or 'int' or 'float' or 'double')
                force output data type
                flag: -datatype %s
        display_init: (a boolean)
                display initial matrix
                flag: -displayinit
        dof: (an integer)
                number of transform degrees of freedom
                flag: -dof %d
        echospacing: (a float)
                value of EPI echo spacing - units of seconds
                flag: -echospacing %f
        environ: (a dictionary with keys which are a value of type 'str' and
                 with values which are a value of type 'str', nipype default value:
                 {})
                Environment variables
        fieldmap: (a file name)
                fieldmap image in rads/s - must be already registered to the
                reference image
                flag: -fieldmap %s
        fieldmapmask: (a file name)
                mask for fieldmap image
                flag: -fieldmapmask %s
        fine_search: (an integer)
                fine search delta angle
                flag: -finesearch %d
        force_scaling: (a boolean)
                force rescaling even for low-res images
                flag: -forcescaling
        ignore_exception: (a boolean, nipype default value: False)
                Print an error message instead of throwing an exception in case the
                interface fails to run
        in_matrix_file: (a file name)
                input 4x4 affine matrix
                flag: -init %s
        in_weight: (an existing file name)
                File for input weighting volume
                flag: -inweight %s
        interp: ('trilinear' or 'nearestneighbour' or 'sinc' or 'spline')
                final interpolation method used in reslicing
                flag: -interp %s
        min_sampling: (a float)
                set minimum voxel dimension for sampling
                flag: -minsampling %f
        no_clamp: (a boolean)
                do not use intensity clamping
                flag: -noclamp
        no_resample: (a boolean)
                do not change input sampling
                flag: -noresample
        no_resample_blur: (a boolean)
                do not use blurring on downsampling
                flag: -noresampblur
        no_search: (a boolean)
                set all angular searches to ranges 0 to 0
                flag: -nosearch
        out_file: (a file name)
                registered output file
                flag: -out %s, position: 2
        out_log: (a file name)
                output log
                requires: save_log
        out_matrix_file: (a file name)
                output affine matrix in 4x4 asciii format
                flag: -omat %s, position: 3
        output_type: ('NIFTI_PAIR' or 'NIFTI_PAIR_GZ' or 'NIFTI_GZ' or
                 'NIFTI')
                FSL output type
        padding_size: (an integer)
                for applyxfm: interpolates outside image by size
                flag: -paddingsize %d
        pedir: (an integer)
                phase encode direction of EPI - 1/2/3=x/y/z & -1/-2/-3=-x/-y/-z
                flag: -pedir %d
        ref_weight: (an existing file name)
                File for reference weighting volume
                flag: -refweight %s
        rigid2D: (a boolean)
                use 2D rigid body mode - ignores dof
                flag: -2D
        save_log: (a boolean)
                save to log file
        schedule: (an existing file name)
                replaces default schedule
                flag: -schedule %s
        searchr_x: (a list of from 2 to 2 items which are an integer)
                search angles along x-axis, in degrees
                flag: -searchrx %s
        searchr_y: (a list of from 2 to 2 items which are an integer)
                search angles along y-axis, in degrees
                flag: -searchry %s
        searchr_z: (a list of from 2 to 2 items which are an integer)
                search angles along z-axis, in degrees
                flag: -searchrz %s
        sinc_width: (an integer)
                full-width in voxels
                flag: -sincwidth %d
        sinc_window: ('rectangular' or 'hanning' or 'blackman')
                sinc window
                flag: -sincwindow %s
        uses_qform: (a boolean)
                initialize using sform or qform
                flag: -usesqform
        verbose: (an integer)
                verbose mode, 0 is least
                flag: -verbose %d
        wm_seg: (a file name)
                white matter segmentation volume needed by BBR cost function
                flag: -wmseg %s
        wmcoords: (a file name)
                white matter boundary coordinates for BBR cost function
                flag: -wmcoords %s
        wmnorms: (a file name)
                white matter boundary normals for BBR cost function
                flag: -wmnorms %s

Outputs::

        out_file: (an existing file name)
                path/name of registered file (if generated)
        out_log: (a file name)
                path/name of output log (if generated)
        out_matrix_file: (an existing file name)
                path/name of calculated affine transform (if generated)

.. _nipype.interfaces.fsl.preprocess.BET:


.. index:: BET

BET
---

`Link to code <http://github.com/nipy/nipype/tree/e63e055194d62d2bdc4665688261c03a42fd0025/nipype/interfaces/fsl/preprocess.py#L117>`__

Wraps command **bet**

Use FSL BET command for skull stripping.

For complete details, see the `BET Documentation.
<http://www.fmrib.ox.ac.uk/fsl/bet2/index.html>`_

Examples
~~~~~~~~
>>> from nipype.interfaces import fsl
>>> from nipype.testing import  example_data
>>> btr = fsl.BET()
>>> btr.inputs.in_file = example_data('structural.nii')
>>> btr.inputs.frac = 0.7
>>> res = btr.run() # doctest: +SKIP

Inputs::

        [Mandatory]
        in_file: (an existing file name)
                input file to skull strip
                flag: %s, position: 0
        terminal_output: ('stream' or 'allatonce' or 'file' or 'none')
                Control terminal output: `stream` - displays to terminal
                immediately, `allatonce` - waits till command is finished to display
                output, `file` - writes output to file, `none` - output is ignored

        [Optional]
        args: (a string)
                Additional parameters to the command
                flag: %s
        center: (a list of at most 3 items which are an integer)
                center of gravity in voxels
                flag: -c %s
        environ: (a dictionary with keys which are a value of type 'str' and
                 with values which are a value of type 'str', nipype default value:
                 {})
                Environment variables
        frac: (a float)
                fractional intensity threshold
                flag: -f %.2f
        functional: (a boolean)
                apply to 4D fMRI data
                flag: -F
                mutually_exclusive: functional, reduce_bias, robust, padding,
                 remove_eyes, surfaces, t2_guided
        ignore_exception: (a boolean, nipype default value: False)
                Print an error message instead of throwing an exception in case the
                interface fails to run
        mask: (a boolean)
                create binary mask image
                flag: -m
        mesh: (a boolean)
                generate a vtk mesh brain surface
                flag: -e
        no_output: (a boolean)
                Don't generate segmented output
                flag: -n
        out_file: (a file name)
                name of output skull stripped image
                flag: %s, position: 1
        outline: (a boolean)
                create surface outline image
                flag: -o
        output_type: ('NIFTI_PAIR' or 'NIFTI_PAIR_GZ' or 'NIFTI_GZ' or
                 'NIFTI')
                FSL output type
        padding: (a boolean)
                improve BET if FOV is very small in Z (by temporarily padding end
                slices)
                flag: -Z
                mutually_exclusive: functional, reduce_bias, robust, padding,
                 remove_eyes, surfaces, t2_guided
        radius: (an integer)
                head radius
                flag: -r %d
        reduce_bias: (a boolean)
                bias field and neck cleanup
                flag: -B
                mutually_exclusive: functional, reduce_bias, robust, padding,
                 remove_eyes, surfaces, t2_guided
        remove_eyes: (a boolean)
                eye & optic nerve cleanup (can be useful in SIENA)
                flag: -S
                mutually_exclusive: functional, reduce_bias, robust, padding,
                 remove_eyes, surfaces, t2_guided
        robust: (a boolean)
                robust brain centre estimation (iterates BET several times)
                flag: -R
                mutually_exclusive: functional, reduce_bias, robust, padding,
                 remove_eyes, surfaces, t2_guided
        skull: (a boolean)
                create skull image
                flag: -s
        surfaces: (a boolean)
                run bet2 and then betsurf to get additional skull and scalp surfaces
                (includes registrations)
                flag: -A
                mutually_exclusive: functional, reduce_bias, robust, padding,
                 remove_eyes, surfaces, t2_guided
        t2_guided: (a file name)
                as with creating surfaces, when also feeding in non-brain-extracted
                T2 (includes registrations)
                flag: -A2 %s
                mutually_exclusive: functional, reduce_bias, robust, padding,
                 remove_eyes, surfaces, t2_guided
        threshold: (a boolean)
                apply thresholding to segmented brain image and mask
                flag: -t
        vertical_gradient: (a float)
                vertical gradient in fractional intensity threshold (-1, 1)
                flag: -g %.2f

Outputs::

        inskull_mask_file: (a file name)
                path/name of inskull mask (if generated)
        inskull_mesh_file: (a file name)
                path/name of inskull mesh outline (if generated)
        mask_file: (a file name)
                path/name of binary brain mask (if generated)
        meshfile: (a file name)
                path/name of vtk mesh file (if generated)
        out_file: (a file name)
                path/name of skullstripped file (if generated)
        outline_file: (a file name)
                path/name of outline file (if generated)
        outskin_mask_file: (a file name)
                path/name of outskin mask (if generated)
        outskin_mesh_file: (a file name)
                path/name of outskin mesh outline (if generated)
        outskull_mask_file: (a file name)
                path/name of outskull mask (if generated)
        outskull_mesh_file: (a file name)
                path/name of outskull mesh outline (if generated)
        skull_mask_file: (a file name)
                path/name of skull mask (if generated)

.. _nipype.interfaces.fsl.preprocess.FAST:


.. index:: FAST

FAST
----

`Link to code <http://github.com/nipy/nipype/tree/e63e055194d62d2bdc4665688261c03a42fd0025/nipype/interfaces/fsl/preprocess.py#L290>`__

Wraps command **fast**

Use FSL FAST for segmenting and bias correction.

For complete details, see the `FAST Documentation.
<http://www.fmrib.ox.ac.uk/fsl/fast4/index.html>`_

Examples
~~~~~~~~
>>> from nipype.interfaces import fsl
>>> from nipype.testing import example_data

Assign options through the ``inputs`` attribute:

>>> fastr = fsl.FAST()
>>> fastr.inputs.in_files = example_data('structural.nii')
>>> out = fastr.run() #doctest: +SKIP

Inputs::

        [Mandatory]
        in_files: (an existing file name)
                image, or multi-channel set of images, to be segmented
                flag: %s, position: -1
        terminal_output: ('stream' or 'allatonce' or 'file' or 'none')
                Control terminal output: `stream` - displays to terminal
                immediately, `allatonce` - waits till command is finished to display
                output, `file` - writes output to file, `none` - output is ignored

        [Optional]
        args: (a string)
                Additional parameters to the command
                flag: %s
        bias_iters: (1 <= an integer <= 10)
                number of main-loop iterations during bias-field removal
                flag: -I %d
        bias_lowpass: (4 <= an integer <= 40)
                bias field smoothing extent (FWHM) in mm
                flag: -l %d
        environ: (a dictionary with keys which are a value of type 'str' and
                 with values which are a value of type 'str', nipype default value:
                 {})
                Environment variables
        hyper: (0.0 <= a floating point number <= 1.0)
                segmentation spatial smoothness
                flag: -H %.2f
        ignore_exception: (a boolean, nipype default value: False)
                Print an error message instead of throwing an exception in case the
                interface fails to run
        img_type: (1 or 2 or 3)
                int specifying type of image: (1 = T1, 2 = T2, 3 = PD)
                flag: -t %d
        init_seg_smooth: (0.0001 <= a floating point number <= 0.1)
                initial segmentation spatial smoothness (during bias field
                estimation)
                flag: -f %.3f
        init_transform: (an existing file name)
                <standard2input.mat> initialise using priors
                flag: -a %s
        iters_afterbias: (1 <= an integer <= 20)
                number of main-loop iterations after bias-field removal
                flag: -O %d
        manual_seg: (an existing file name)
                Filename containing intensities
                flag: -s %s
        mixel_smooth: (0.0 <= a floating point number <= 1.0)
                spatial smoothness for mixeltype
                flag: -R %.2f
        no_bias: (a boolean)
                do not remove bias field
                flag: -N
        no_pve: (a boolean)
                turn off PVE (partial volume estimation)
                flag: --nopve
        number_classes: (1 <= an integer <= 10)
                number of tissue-type classes
                flag: -n %d
        other_priors: (a list of from 3 to 3 items which are a file name)
                alternative prior images
                flag: -A %s
        out_basename: (a file name)
                base name of output files
                flag: -o %s
        output_biascorrected: (a boolean)
                output restored image (bias-corrected image)
                flag: -B
        output_biasfield: (a boolean)
                output estimated bias field
                flag: -b
        output_type: ('NIFTI_PAIR' or 'NIFTI_PAIR_GZ' or 'NIFTI_GZ' or
                 'NIFTI')
                FSL output type
        probability_maps: (a boolean)
                outputs individual probability maps
                flag: -p
        segment_iters: (1 <= an integer <= 50)
                number of segmentation-initialisation iterations
                flag: -W %d
        segments: (a boolean)
                outputs a separate binary image for each tissue type
                flag: -g
        use_priors: (a boolean)
                use priors throughout
                flag: -P
        verbose: (a boolean)
                switch on diagnostic messages
                flag: -v

Outputs::

        bias_field: (a file name)
        mixeltype: (a file name)
                path/name of mixeltype volume file _mixeltype
        partial_volume_files: (a file name)
        partial_volume_map: (a file name)
                path/name of partial volume file _pveseg
        probability_maps: (a file name)
        restored_image: (a file name)
        tissue_class_files: (a file name)
        tissue_class_map: (an existing file name)
                path/name of binary segmented volume file one val for each class
                _seg

.. _nipype.interfaces.fsl.preprocess.FIRST:


.. index:: FIRST

FIRST
-----

`Link to code <http://github.com/nipy/nipype/tree/e63e055194d62d2bdc4665688261c03a42fd0025/nipype/interfaces/fsl/preprocess.py#L1522>`__

Wraps command **run_first_all**

Use FSL's run_first_all command to segment subcortical volumes

http://www.fmrib.ox.ac.uk/fsl/first/index.html

Examples
~~~~~~~~

>>> from nipype.interfaces import fsl
>>> first = fsl.FIRST()
>>> first.inputs.in_file = 'structural.nii'
>>> first.inputs.out_file = 'segmented.nii'
>>> res = first.run() #doctest: +SKIP

Inputs::

        [Mandatory]
        in_file: (an existing file name)
                input data file
                flag: -i %s, position: -2
        out_file: (a file name, nipype default value: segmented)
                output data file
                flag: -o %s, position: -1
        terminal_output: ('stream' or 'allatonce' or 'file' or 'none')
                Control terminal output: `stream` - displays to terminal
                immediately, `allatonce` - waits till command is finished to display
                output, `file` - writes output to file, `none` - output is ignored

        [Optional]
        affine_file: (an existing file name)
                Affine matrix to use (e.g. img2std.mat) (does not re-run
                registration)
                flag: -a %s, position: 6
        args: (a string)
                Additional parameters to the command
                flag: %s
        brain_extracted: (a boolean)
                Input structural image is already brain-extracted
                flag: -b, position: 2
        environ: (a dictionary with keys which are a value of type 'str' and
                 with values which are a value of type 'str', nipype default value:
                 {})
                Environment variables
        ignore_exception: (a boolean, nipype default value: False)
                Print an error message instead of throwing an exception in case the
                interface fails to run
        list_of_specific_structures: (a list of at least 1 items which are a
                 string)
                Runs only on the specified structures (e.g. L_Hipp, R_HippL_Accu,
                R_Accu, L_Amyg, R_AmygL_Caud, R_Caud, L_Pall, R_PallL_Puta, R_Puta,
                L_Thal, R_Thal, BrStem
                flag: -s %s, position: 5
        method: ('auto' or 'fast' or 'none')
                Method must be one of auto, fast, none, or it can be entered using
                the 'method_as_numerical_threshold' input
                flag: -m, position: 4
                mutually_exclusive: method_as_numerical_threshold
        method_as_numerical_threshold: (a float)
                Specify a numerical threshold value or use the 'method' input to
                choose auto, fast, or none
                flag: -m, position: 4
        no_cleanup: (a boolean)
                Input structural image is already brain-extracted
                flag: -d, position: 3
        output_type: ('NIFTI_PAIR' or 'NIFTI_PAIR_GZ' or 'NIFTI_GZ' or
                 'NIFTI')
                FSL output type
        verbose: (a boolean)
                Use verbose logging.
                flag: -v, position: 1

Outputs::

        bvars: (an existing file name)
                bvars for each subcortical region
        original_segmentations: (an existing file name)
                3D image file containing the segmented regions as integer values.
                Uses CMA labelling
        segmentation_file: (an existing file name)
                4D image file containing a single volume per segmented region
        vtk_surfaces: (an existing file name)
                VTK format meshes for each subcortical region

.. _nipype.interfaces.fsl.preprocess.FLIRT:


.. index:: FLIRT

FLIRT
-----

`Link to code <http://github.com/nipy/nipype/tree/e63e055194d62d2bdc4665688261c03a42fd0025/nipype/interfaces/fsl/preprocess.py#L521>`__

Wraps command **flirt**

Use FSL FLIRT for coregistration.

For complete details, see the `FLIRT Documentation.
<http://www.fmrib.ox.ac.uk/fsl/flirt/index.html>`_

To print out the command line help, use:
    fsl.FLIRT().inputs_help()

Examples
~~~~~~~~
>>> from nipype.interfaces import fsl
>>> from nipype.testing import example_data
>>> flt = fsl.FLIRT(bins=640, cost_func='mutualinfo')
>>> flt.inputs.in_file = 'structural.nii'
>>> flt.inputs.reference = 'mni.nii'
>>> flt.inputs.output_type = "NIFTI_GZ"
>>> flt.cmdline #doctest: +ELLIPSIS
'flirt -in structural.nii -ref mni.nii -out structural_flirt.nii.gz -omat structural_flirt.mat -bins 640 -searchcost mutualinfo'
>>> res = flt.run() #doctest: +SKIP

Inputs::

        [Mandatory]
        in_file: (an existing file name)
                input file
                flag: -in %s, position: 0
        reference: (an existing file name)
                reference file
                flag: -ref %s, position: 1
        terminal_output: ('stream' or 'allatonce' or 'file' or 'none')
                Control terminal output: `stream` - displays to terminal
                immediately, `allatonce` - waits till command is finished to display
                output, `file` - writes output to file, `none` - output is ignored

        [Optional]
        angle_rep: ('quaternion' or 'euler')
                representation of rotation angles
                flag: -anglerep %s
        apply_isoxfm: (a float)
                as applyxfm but forces isotropic resampling
                flag: -applyisoxfm %f
                mutually_exclusive: apply_xfm
        apply_xfm: (a boolean)
                apply transformation supplied by in_matrix_file
                flag: -applyxfm
                requires: in_matrix_file
        args: (a string)
                Additional parameters to the command
                flag: %s
        bbrslope: (a float)
                value of bbr slope
                flag: -bbrslope %f
        bbrtype: ('signed' or 'global_abs' or 'local_abs')
                type of bbr cost function: signed [default], global_abs, local_abs
                flag: -bbrtype %s
        bgvalue: (a float)
                use specified background value for points outside FOV
                flag: -setbackground %f
        bins: (an integer)
                number of histogram bins
                flag: -bins %d
        coarse_search: (an integer)
                coarse search delta angle
                flag: -coarsesearch %d
        cost: ('mutualinfo' or 'corratio' or 'normcorr' or 'normmi' or
                 'leastsq' or 'labeldiff' or 'bbr')
                cost function
                flag: -cost %s
        cost_func: ('mutualinfo' or 'corratio' or 'normcorr' or 'normmi' or
                 'leastsq' or 'labeldiff' or 'bbr')
                cost function
                flag: -searchcost %s
        datatype: ('char' or 'short' or 'int' or 'float' or 'double')
                force output data type
                flag: -datatype %s
        display_init: (a boolean)
                display initial matrix
                flag: -displayinit
        dof: (an integer)
                number of transform degrees of freedom
                flag: -dof %d
        echospacing: (a float)
                value of EPI echo spacing - units of seconds
                flag: -echospacing %f
        environ: (a dictionary with keys which are a value of type 'str' and
                 with values which are a value of type 'str', nipype default value:
                 {})
                Environment variables
        fieldmap: (a file name)
                fieldmap image in rads/s - must be already registered to the
                reference image
                flag: -fieldmap %s
        fieldmapmask: (a file name)
                mask for fieldmap image
                flag: -fieldmapmask %s
        fine_search: (an integer)
                fine search delta angle
                flag: -finesearch %d
        force_scaling: (a boolean)
                force rescaling even for low-res images
                flag: -forcescaling
        ignore_exception: (a boolean, nipype default value: False)
                Print an error message instead of throwing an exception in case the
                interface fails to run
        in_matrix_file: (a file name)
                input 4x4 affine matrix
                flag: -init %s
        in_weight: (an existing file name)
                File for input weighting volume
                flag: -inweight %s
        interp: ('trilinear' or 'nearestneighbour' or 'sinc' or 'spline')
                final interpolation method used in reslicing
                flag: -interp %s
        min_sampling: (a float)
                set minimum voxel dimension for sampling
                flag: -minsampling %f
        no_clamp: (a boolean)
                do not use intensity clamping
                flag: -noclamp
        no_resample: (a boolean)
                do not change input sampling
                flag: -noresample
        no_resample_blur: (a boolean)
                do not use blurring on downsampling
                flag: -noresampblur
        no_search: (a boolean)
                set all angular searches to ranges 0 to 0
                flag: -nosearch
        out_file: (a file name)
                registered output file
                flag: -out %s, position: 2
        out_log: (a file name)
                output log
                requires: save_log
        out_matrix_file: (a file name)
                output affine matrix in 4x4 asciii format
                flag: -omat %s, position: 3
        output_type: ('NIFTI_PAIR' or 'NIFTI_PAIR_GZ' or 'NIFTI_GZ' or
                 'NIFTI')
                FSL output type
        padding_size: (an integer)
                for applyxfm: interpolates outside image by size
                flag: -paddingsize %d
        pedir: (an integer)
                phase encode direction of EPI - 1/2/3=x/y/z & -1/-2/-3=-x/-y/-z
                flag: -pedir %d
        ref_weight: (an existing file name)
                File for reference weighting volume
                flag: -refweight %s
        rigid2D: (a boolean)
                use 2D rigid body mode - ignores dof
                flag: -2D
        save_log: (a boolean)
                save to log file
        schedule: (an existing file name)
                replaces default schedule
                flag: -schedule %s
        searchr_x: (a list of from 2 to 2 items which are an integer)
                search angles along x-axis, in degrees
                flag: -searchrx %s
        searchr_y: (a list of from 2 to 2 items which are an integer)
                search angles along y-axis, in degrees
                flag: -searchry %s
        searchr_z: (a list of from 2 to 2 items which are an integer)
                search angles along z-axis, in degrees
                flag: -searchrz %s
        sinc_width: (an integer)
                full-width in voxels
                flag: -sincwidth %d
        sinc_window: ('rectangular' or 'hanning' or 'blackman')
                sinc window
                flag: -sincwindow %s
        uses_qform: (a boolean)
                initialize using sform or qform
                flag: -usesqform
        verbose: (an integer)
                verbose mode, 0 is least
                flag: -verbose %d
        wm_seg: (a file name)
                white matter segmentation volume needed by BBR cost function
                flag: -wmseg %s
        wmcoords: (a file name)
                white matter boundary coordinates for BBR cost function
                flag: -wmcoords %s
        wmnorms: (a file name)
                white matter boundary normals for BBR cost function
                flag: -wmnorms %s

Outputs::

        out_file: (an existing file name)
                path/name of registered file (if generated)
        out_log: (a file name)
                path/name of output log (if generated)
        out_matrix_file: (an existing file name)
                path/name of calculated affine transform (if generated)

.. _nipype.interfaces.fsl.preprocess.FNIRT:


.. index:: FNIRT

FNIRT
-----

`Link to code <http://github.com/nipy/nipype/tree/e63e055194d62d2bdc4665688261c03a42fd0025/nipype/interfaces/fsl/preprocess.py#L851>`__

Wraps command **fnirt**

Use FSL FNIRT for non-linear registration.

Examples
~~~~~~~~
>>> from nipype.interfaces import fsl
>>> from nipype.testing import example_data
>>> fnt = fsl.FNIRT(affine_file=example_data('trans.mat'))
>>> res = fnt.run(ref_file=example_data('mni.nii', in_file=example_data('structural.nii')) #doctest: +SKIP

T1 -> Mni153

>>> from nipype.interfaces import fsl
>>> fnirt_mprage = fsl.FNIRT()
>>> fnirt_mprage.inputs.in_fwhm = [8, 4, 2, 2]
>>> fnirt_mprage.inputs.subsampling_scheme = [4, 2, 1, 1]

Specify the resolution of the warps

>>> fnirt_mprage.inputs.warp_resolution = (6, 6, 6)
>>> res = fnirt_mprage.run(in_file='structural.nii', ref_file='mni.nii', warped_file='warped.nii', fieldcoeff_file='fieldcoeff.nii')#doctest: +SKIP

We can check the command line and confirm that it's what we expect.

>>> fnirt_mprage.cmdline  #doctest: +SKIP
'fnirt --cout=fieldcoeff.nii --in=structural.nii --infwhm=8,4,2,2 --ref=mni.nii --subsamp=4,2,1,1 --warpres=6,6,6 --iout=warped.nii'

Inputs::

        [Mandatory]
        in_file: (an existing file name)
                name of input image
                flag: --in=%s
        ref_file: (an existing file name)
                name of reference image
                flag: --ref=%s
        terminal_output: ('stream' or 'allatonce' or 'file' or 'none')
                Control terminal output: `stream` - displays to terminal
                immediately, `allatonce` - waits till command is finished to display
                output, `file` - writes output to file, `none` - output is ignored

        [Optional]
        affine_file: (an existing file name)
                name of file containing affine transform
                flag: --aff=%s
        apply_inmask: (a list of items which are 0 or 1)
                list of iterations to use input mask on (1 to use, 0 to skip)
                flag: --applyinmask=%s
                mutually_exclusive: skip_inmask
        apply_intensity_mapping: (a list of items which are 0 or 1)
                List of subsampling levels to apply intensity mapping for (0 to
                skip, 1 to apply)
                flag: --estint=%s
                mutually_exclusive: skip_intensity_mapping
        apply_refmask: (a list of items which are 0 or 1)
                list of iterations to use reference mask on (1 to use, 0 to skip)
                flag: --applyrefmask=%s
                mutually_exclusive: skip_refmask
        args: (a string)
                Additional parameters to the command
                flag: %s
        bias_regularization_lambda: (a float)
                Weight of regularisation for bias-field, default 10000
                flag: --biaslambda=%f
        biasfield_resolution: (a tuple of the form: (an integer, an integer,
                 an integer))
                Resolution (in mm) of bias-field modelling local intensities,
                default 50, 50, 50
                flag: --biasres=%d,%d,%d
        config_file: ('T1_2_MNI152_2mm' or 'FA_2_FMRIB58_1mm' or an existing
                 file name)
                Name of config file specifying command line arguments
                flag: --config=%s
        derive_from_ref: (a boolean)
                If true, ref image is used to calculate derivatives. Default false
                flag: --refderiv
        environ: (a dictionary with keys which are a value of type 'str' and
                 with values which are a value of type 'str', nipype default value:
                 {})
                Environment variables
        field_file: (a boolean or a file name)
                name of output file with field or true
                flag: --fout=%s
        fieldcoeff_file: (a boolean or a file name)
                name of output file with field coefficients or true
                flag: --cout=%s
        hessian_precision: ('double' or 'float')
                Precision for representing Hessian, double or float. Default double
                flag: --numprec=%s
        ignore_exception: (a boolean, nipype default value: False)
                Print an error message instead of throwing an exception in case the
                interface fails to run
        in_fwhm: (a list of items which are an integer)
                FWHM (in mm) of gaussian smoothing kernel for input volume, default
                [6, 4, 2, 2]
                flag: --infwhm=%s
        in_intensitymap_file: (an existing file name)
                name of file/files containing initial intensity mapingusually
                generated by previos fnirt run
                flag: --intin=%s
        inmask_file: (an existing file name)
                name of file with mask in input image space
                flag: --inmask=%s
        inmask_val: (a float)
                Value to mask out in --in image. Default =0.0
                flag: --impinval=%f
        intensity_mapping_model: ('none' or 'global_linear' or
                 'global_non_linearlocal_linear' or 'global_non_linear_with_bias' or
                 'local_non_linear')
                Model for intensity-mapping
                flag: --intmod=%s
        intensity_mapping_order: (an integer)
                Order of poynomial for mapping intensities, default 5
                flag: --intorder=%d
        inwarp_file: (an existing file name)
                name of file containing initial non-linear warps
                flag: --inwarp=%s
        jacobian_file: (a boolean or a file name)
                name of file for writing out the Jacobianof the field (for
                diagnostic or VBM purposes)
                flag: --jout=%s
        jacobian_range: (a tuple of the form: (a float, a float))
                Allowed range of Jacobian determinants, default 0.01, 100.0
                flag: --jacrange=%f,%f
        log_file: (a file name)
                Name of log-file
                flag: --logout=%s
        max_nonlin_iter: (a list of items which are an integer)
                Max # of non-linear iterations list, default [5, 5, 5, 5]
                flag: --miter=%s
        modulatedref_file: (a boolean or a file name)
                name of file for writing out intensity modulated--ref (for
                diagnostic purposes)
                flag: --refout=%s
        out_intensitymap_file: (a boolean or a file name)
                name of files for writing information pertaining to intensity
                mapping
                flag: --intout=%s
        output_type: ('NIFTI_PAIR' or 'NIFTI_PAIR_GZ' or 'NIFTI_GZ' or
                 'NIFTI')
                FSL output type
        ref_fwhm: (a list of items which are an integer)
                FWHM (in mm) of gaussian smoothing kernel for ref volume, default
                [4, 2, 0, 0]
                flag: --reffwhm=%s
        refmask_file: (an existing file name)
                name of file with mask in reference space
                flag: --refmask=%s
        refmask_val: (a float)
                Value to mask out in --ref image. Default =0.0
                flag: --imprefval=%f
        regularization_lambda: (a list of items which are a float)
                Weight of regularisation, default depending on --ssqlambda and
                --regmod switches. See user documetation.
                flag: --lambda=%s
        regularization_model: ('membrane_energy' or 'bending_energy')
                Model for regularisation of warp-field [membrane_energy
                bending_energy], default bending_energy
                flag: --regmod=%s
        skip_implicit_in_masking: (a boolean)
                skip implicit masking based on valuein --in image. Default = 0
                flag: --impinm=0
        skip_implicit_ref_masking: (a boolean)
                skip implicit masking based on valuein --ref image. Default = 0
                flag: --imprefm=0
        skip_inmask: (a boolean)
                skip specified inmask if set, default false
                flag: --applyinmask=0
                mutually_exclusive: apply_inmask
        skip_intensity_mapping: (a boolean)
                Skip estimate intensity-mapping default false
                flag: --estint=0
                mutually_exclusive: apply_intensity_mapping
        skip_lambda_ssq: (a boolean)
                If true, lambda is not weighted by current ssq, default false
                flag: --ssqlambda=0
        skip_refmask: (a boolean)
                Skip specified refmask if set, default false
                flag: --applyrefmask=0
                mutually_exclusive: apply_refmask
        spline_order: (an integer)
                Order of spline, 2->Qadratic spline, 3->Cubic spline. Default=3
                flag: --splineorder=%d
        subsampling_scheme: (a list of items which are an integer)
                sub-sampling scheme, list, default [4, 2, 1, 1]
                flag: --subsamp=%s
        warp_resolution: (a tuple of the form: (an integer, an integer, an
                 integer))
                (approximate) resolution (in mm) of warp basis in x-, y- and
                z-direction, default 10, 10, 10
                flag: --warpres=%d,%d,%d
        warped_file: (a file name)
                name of output image
                flag: --iout=%s

Outputs::

        field_file: (a file name)
                file with warp field
        fieldcoeff_file: (an existing file name)
                file with field coefficients
        jacobian_file: (a file name)
                file containing Jacobian of the field
        log_file: (a file name)
                Name of log-file
        modulatedref_file: (a file name)
                file containing intensity modulated --ref
        out_intensitymap_file: (a file name)
                file containing info pertaining to intensity mapping
        warped_file: (an existing file name)
                warped image

.. _nipype.interfaces.fsl.preprocess.FUGUE:


.. index:: FUGUE

FUGUE
-----

`Link to code <http://github.com/nipy/nipype/tree/e63e055194d62d2bdc4665688261c03a42fd0025/nipype/interfaces/fsl/preprocess.py#L1242>`__

Wraps command **fugue**

`FUGUE <http://fsl.fmrib.ox.ac.uk/fsl/fslwiki/FUGUE>`_ is, most generally, a set of tools for
EPI distortion correction.

Distortions may be corrected for
    1. improving registration with non-distorted images (e.g. structurals), or
    2. dealing with motion-dependent changes.

FUGUE is designed to deal only with the first case - improving registration.


Examples
~~~~~~~~


Unwarping an input image (shift map is known) ::

>>> from nipype.interfaces.fsl.preprocess import FUGUE
>>> fugue = FUGUE()
>>> fugue.inputs.in_file = 'epi.nii'
>>> fugue.inputs.mask_file = 'epi_mask.nii'
>>> fugue.inputs.shift_in_file = 'vsm.nii'  # Previously computed with fugue as well
>>> fugue.inputs.unwarp_direction = 'y'
>>> fugue.inputs.output_type = "NIFTI_GZ"
>>> fugue.cmdline #doctest: +ELLIPSIS
'fugue --in=epi.nii --mask=epi_mask.nii --loadshift=vsm.nii --unwarpdir=y --unwarp=epi_unwarped.nii.gz'
>>> fugue.run() #doctest: +SKIP


Warping an input image (shift map is known) ::

>>> from nipype.interfaces.fsl.preprocess import FUGUE
>>> fugue = FUGUE()
>>> fugue.inputs.in_file = 'epi.nii'
>>> fugue.inputs.forward_warping = True
>>> fugue.inputs.mask_file = 'epi_mask.nii'
>>> fugue.inputs.shift_in_file = 'vsm.nii'  # Previously computed with fugue as well
>>> fugue.inputs.unwarp_direction = 'y'
>>> fugue.inputs.output_type = "NIFTI_GZ"
>>> fugue.cmdline #doctest: +ELLIPSIS
'fugue --in=epi.nii --mask=epi_mask.nii --loadshift=vsm.nii --unwarpdir=y --warp=epi_warped.nii.gz'
>>> fugue.run() #doctest: +SKIP


Computing the vsm (unwrapped phase map is known) ::

>>> from nipype.interfaces.fsl.preprocess import FUGUE
>>> fugue = FUGUE()
>>> fugue.inputs.phasemap_in_file = 'epi_phasediff.nii'
>>> fugue.inputs.mask_file = 'epi_mask.nii'
>>> fugue.inputs.dwell_to_asym_ratio = (0.77e-3 * 3) / 2.46e-3
>>> fugue.inputs.unwarp_direction = 'y'
>>> fugue.inputs.save_shift = True
>>> fugue.inputs.output_type = "NIFTI_GZ"
>>> fugue.cmdline #doctest: +ELLIPSIS
'fugue --dwelltoasym=0.9390243902 --mask=epi_mask.nii --phasemap=epi_phasediff.nii --saveshift=epi_phasediff_vsm.nii.gz --unwarpdir=y'
>>> fugue.run() #doctest: +SKIP

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
        asym_se_time: (a float)
                set the fieldmap asymmetric spin echo time (sec)
                flag: --asym=%.10f
        despike_2dfilter: (a boolean)
                apply a 2D de-spiking filter
                flag: --despike
        despike_threshold: (a float)
                specify the threshold for de-spiking (default=3.0)
                flag: --despikethreshold=%s
        dwell_time: (a float)
                set the EPI dwell time per phase-encode line - same as echo spacing
                - (sec)
                flag: --dwell=%.10f
        dwell_to_asym_ratio: (a float)
                set the dwell to asym time ratio
                flag: --dwelltoasym=%.10f
        environ: (a dictionary with keys which are a value of type 'str' and
                 with values which are a value of type 'str', nipype default value:
                 {})
                Environment variables
        fmap_in_file: (an existing file name)
                filename for loading fieldmap (rad/s)
                flag: --loadfmap=%s
        fmap_out_file: (a file name)
                filename for saving fieldmap (rad/s)
                flag: --savefmap=%s
        forward_warping: (a boolean, nipype default value: False)
                apply forward warping instead of unwarping
        fourier_order: (an integer)
                apply Fourier (sinusoidal) fitting of order N
                flag: --fourier=%d
        icorr: (a boolean)
                apply intensity correction to unwarping (pixel shift method only)
                flag: --icorr
                requires: shift_in_file
        icorr_only: (a boolean)
                apply intensity correction only
                flag: --icorronly
                requires: unwarped_file
        ignore_exception: (a boolean, nipype default value: False)
                Print an error message instead of throwing an exception in case the
                interface fails to run
        in_file: (an existing file name)
                filename of input volume
                flag: --in=%s
        mask_file: (an existing file name)
                filename for loading valid mask
                flag: --mask=%s
        median_2dfilter: (a boolean)
                apply 2D median filtering
                flag: --median
        no_extend: (a boolean)
                do not apply rigid-body extrapolation to the fieldmap
                flag: --noextend
        no_gap_fill: (a boolean)
                do not apply gap-filling measure to the fieldmap
                flag: --nofill
        nokspace: (a boolean)
                do not use k-space forward warping
                flag: --nokspace
        output_type: ('NIFTI_PAIR' or 'NIFTI_PAIR_GZ' or 'NIFTI_GZ' or
                 'NIFTI')
                FSL output type
        pava: (a boolean)
                apply monotonic enforcement via PAVA
                flag: --pava
        phase_conjugate: (a boolean)
                apply phase conjugate method of unwarping
                flag: --phaseconj
        phasemap_in_file: (an existing file name)
                filename for input phase image
                flag: --phasemap=%s
        poly_order: (an integer)
                apply polynomial fitting of order N
                flag: --poly=%d
        save_fmap: (a boolean)
                write field map volume
                mutually_exclusive: save_unmasked_fmap
        save_shift: (a boolean)
                write pixel shift volume
                mutually_exclusive: save_unmasked_shift
        save_unmasked_fmap: (a boolean)
                saves the unmasked fieldmap when using --savefmap
                flag: --unmaskfmap
                mutually_exclusive: save_fmap
        save_unmasked_shift: (a boolean)
                saves the unmasked shiftmap when using --saveshift
                flag: --unmaskshift
                mutually_exclusive: save_shift
        shift_in_file: (an existing file name)
                filename for reading pixel shift volume
                flag: --loadshift=%s
        shift_out_file: (a file name)
                filename for saving pixel shift volume
                flag: --saveshift=%s
        smooth2d: (a float)
                apply 2D Gaussian smoothing of sigma N (in mm)
                flag: --smooth2=%.2f
        smooth3d: (a float)
                apply 3D Gaussian smoothing of sigma N (in mm)
                flag: --smooth3=%.2f
        unwarp_direction: ('x' or 'y' or 'z' or 'x-' or 'y-' or 'z-')
                specifies direction of warping (default y)
                flag: --unwarpdir=%s
        unwarped_file: (a file name)
                apply unwarping and save as filename
                flag: --unwarp=%s
                mutually_exclusive: warped_file
                requires: in_file
        warped_file: (a file name)
                apply forward warping and save as filename
                flag: --warp=%s
                mutually_exclusive: unwarped_file
                requires: in_file

Outputs::

        fmap_out_file: (a file name)
                fieldmap file
        shift_out_file: (a file name)
                voxel shift map file
        unwarped_file: (a file name)
                unwarped file
        warped_file: (a file name)
                forward warped file

.. _nipype.interfaces.fsl.preprocess.MCFLIRT:


.. index:: MCFLIRT

MCFLIRT
-------

`Link to code <http://github.com/nipy/nipype/tree/e63e055194d62d2bdc4665688261c03a42fd0025/nipype/interfaces/fsl/preprocess.py#L647>`__

Wraps command **mcflirt**

Use FSL MCFLIRT to do within-modality motion correction.

For complete details, see the `MCFLIRT Documentation.
<http://www.fmrib.ox.ac.uk/fsl/mcflirt/index.html>`_

Examples
~~~~~~~~
>>> from nipype.interfaces import fsl
>>> from nipype.testing import example_data
>>> mcflt = fsl.MCFLIRT(in_file=example_data('functional.nii'), cost='mutualinfo')
>>> res = mcflt.run() # doctest: +SKIP

Inputs::

        [Mandatory]
        in_file: (an existing file name)
                timeseries to motion-correct
                flag: -in %s, position: 0
        terminal_output: ('stream' or 'allatonce' or 'file' or 'none')
                Control terminal output: `stream` - displays to terminal
                immediately, `allatonce` - waits till command is finished to display
                output, `file` - writes output to file, `none` - output is ignored

        [Optional]
        args: (a string)
                Additional parameters to the command
                flag: %s
        bins: (an integer)
                number of histogram bins
                flag: -bins %d
        cost: ('mutualinfo' or 'woods' or 'corratio' or 'normcorr' or
                 'normmi' or 'leastsquares')
                cost function to optimize
                flag: -cost %s
        dof: (an integer)
                degrees of freedom for the transformation
                flag: -dof %d
        environ: (a dictionary with keys which are a value of type 'str' and
                 with values which are a value of type 'str', nipype default value:
                 {})
                Environment variables
        ignore_exception: (a boolean, nipype default value: False)
                Print an error message instead of throwing an exception in case the
                interface fails to run
        init: (an existing file name)
                inital transformation matrix
                flag: -init %s
        interpolation: ('spline' or 'nn' or 'sinc')
                interpolation method for transformation
                flag: -%s_final
        mean_vol: (a boolean)
                register to mean volume
                flag: -meanvol
        out_file: (a file name)
                file to write
                flag: -out %s
        output_type: ('NIFTI_PAIR' or 'NIFTI_PAIR_GZ' or 'NIFTI_GZ' or
                 'NIFTI')
                FSL output type
        ref_file: (an existing file name)
                target image for motion correction
                flag: -reffile %s
        ref_vol: (an integer)
                volume to align frames to
                flag: -refvol %d
        rotation: (an integer)
                scaling factor for rotation tolerances
                flag: -rotation %d
        save_mats: (a boolean)
                save transformation matrices
                flag: -mats
        save_plots: (a boolean)
                save transformation parameters
                flag: -plots
        save_rms: (a boolean)
                save rms displacement parameters
                flag: -rmsabs -rmsrel
        scaling: (a float)
                scaling factor to use
                flag: -scaling %.2f
        smooth: (a float)
                smoothing factor for the cost function
                flag: -smooth %.2f
        stages: (an integer)
                stages (if 4, perform final search with sinc interpolation
                flag: -stages %d
        stats_imgs: (a boolean)
                produce variance and std. dev. images
                flag: -stats
        use_contour: (a boolean)
                run search on contour images
                flag: -edge
        use_gradient: (a boolean)
                run search on gradient images
                flag: -gdt

Outputs::

        mat_file: (an existing file name)
                transformation matrices
        mean_img: (an existing file name)
                mean timeseries image
        out_file: (an existing file name)
                motion-corrected timeseries
        par_file: (an existing file name)
                text-file with motion parameters
        rms_files: (an existing file name)
                absolute and relative displacement parameters
        std_img: (an existing file name)
                standard deviation image
        variance_img: (an existing file name)
                variance image

.. _nipype.interfaces.fsl.preprocess.PRELUDE:


.. index:: PRELUDE

PRELUDE
-------

`Link to code <http://github.com/nipy/nipype/tree/e63e055194d62d2bdc4665688261c03a42fd0025/nipype/interfaces/fsl/preprocess.py#L1441>`__

Wraps command **prelude**

Use FSL prelude to do phase unwrapping

Examples
~~~~~~~~

Please insert examples for use of this command

Inputs::

        [Mandatory]
        complex_phase_file: (an existing file name)
                complex phase input volume
                flag: --complex=%s
                mutually_exclusive: magnitude_file, phase_file
        magnitude_file: (an existing file name)
                file containing magnitude image
                flag: --abs=%s
                mutually_exclusive: complex_phase_file
        phase_file: (an existing file name)
                raw phase file
                flag: --phase=%s
                mutually_exclusive: complex_phase_file
        terminal_output: ('stream' or 'allatonce' or 'file' or 'none')
                Control terminal output: `stream` - displays to terminal
                immediately, `allatonce` - waits till command is finished to display
                output, `file` - writes output to file, `none` - output is ignored

        [Optional]
        args: (a string)
                Additional parameters to the command
                flag: %s
        end: (an integer)
                final image number to process (default Inf)
                flag: --end=%d
        environ: (a dictionary with keys which are a value of type 'str' and
                 with values which are a value of type 'str', nipype default value:
                 {})
                Environment variables
        ignore_exception: (a boolean, nipype default value: False)
                Print an error message instead of throwing an exception in case the
                interface fails to run
        label_file: (a file name)
                saving the area labels output
                flag: --labels=%s
        labelprocess2d: (a boolean)
                does label processing in 2D (slice at a time)
                flag: --labelslices
        mask_file: (an existing file name)
                filename of mask input volume
                flag: --mask=%s
        num_partitions: (an integer)
                number of phase partitions to use
                flag: --numphasesplit=%d
        output_type: ('NIFTI_PAIR' or 'NIFTI_PAIR_GZ' or 'NIFTI_GZ' or
                 'NIFTI')
                FSL output type
        process2d: (a boolean)
                does all processing in 2D (slice at a time)
                flag: --slices
                mutually_exclusive: labelprocess2d
        process3d: (a boolean)
                forces all processing to be full 3D
                flag: --force3D
                mutually_exclusive: labelprocess2d, process2d
        rawphase_file: (a file name)
                saving the raw phase output
                flag: --rawphase=%s
        removeramps: (a boolean)
                remove phase ramps during unwrapping
                flag: --removeramps
        savemask_file: (a file name)
                saving the mask volume
                flag: --savemask=%s
        start: (an integer)
                first image number to process (default 0)
                flag: --start=%d
        threshold: (a float)
                intensity threshold for masking
                flag: --thresh=%.10f
        unwrapped_phase_file: (a file name)
                file containing unwrapepd phase
                flag: --unwrap=%s

Outputs::

        unwrapped_phase_file: (an existing file name)
                unwrapped phase file

.. _nipype.interfaces.fsl.preprocess.SUSAN:


.. index:: SUSAN

SUSAN
-----

`Link to code <http://github.com/nipy/nipype/tree/e63e055194d62d2bdc4665688261c03a42fd0025/nipype/interfaces/fsl/preprocess.py#L1114>`__

Wraps command **susan**

use FSL SUSAN to perform smoothing

Examples
~~~~~~~~

>>> from nipype.interfaces import fsl
>>> from nipype.testing import example_data
>>> print anatfile #doctest: +SKIP
anatomical.nii #doctest: +SKIP
>>> sus = fsl.SUSAN()
>>> sus.inputs.in_file = example_data('structural.nii')
>>> sus.inputs.brightness_threshold = 2000.0
>>> sus.inputs.fwhm = 8.0
>>> result = sus.run() #doctest: +SKIP

Inputs::

        [Mandatory]
        brightness_threshold: (a float)
                brightness threshold and should be greater than noise level and less
                than contrast of edges to be preserved.
                flag: %.10f, position: 2
        fwhm: (a float)
                fwhm of smoothing, in mm, gets converted using sqrt(8*log(2))
                flag: %.10f, position: 3
        in_file: (an existing file name)
                filename of input timeseries
                flag: %s, position: 1
        terminal_output: ('stream' or 'allatonce' or 'file' or 'none')
                Control terminal output: `stream` - displays to terminal
                immediately, `allatonce` - waits till command is finished to display
                output, `file` - writes output to file, `none` - output is ignored

        [Optional]
        args: (a string)
                Additional parameters to the command
                flag: %s
        dimension: (3 or 2, nipype default value: 3)
                within-plane (2) or fully 3D (3)
                flag: %d, position: 4
        environ: (a dictionary with keys which are a value of type 'str' and
                 with values which are a value of type 'str', nipype default value:
                 {})
                Environment variables
        ignore_exception: (a boolean, nipype default value: False)
                Print an error message instead of throwing an exception in case the
                interface fails to run
        out_file: (a file name)
                output file name
                flag: %s, position: -1
        output_type: ('NIFTI_PAIR' or 'NIFTI_PAIR_GZ' or 'NIFTI_GZ' or
                 'NIFTI')
                FSL output type
        usans: (a list of at most 2 items which are a tuple of the form: (an
                 existing file name, a float), nipype default value: [])
                determines whether the smoothing area (USAN) is to be found from
                secondary images (0, 1 or 2). A negative value for any brightness
                threshold will auto-set the threshold at 10% of the robust range
        use_median: (1 or 0, nipype default value: 1)
                whether to use a local median filter in the cases where single-point
                noise is detected
                flag: %d, position: 5

Outputs::

        smoothed_file: (an existing file name)
                smoothed output file

.. _nipype.interfaces.fsl.preprocess.SliceTimer:


.. index:: SliceTimer

SliceTimer
----------

`Link to code <http://github.com/nipy/nipype/tree/e63e055194d62d2bdc4665688261c03a42fd0025/nipype/interfaces/fsl/preprocess.py#L1050>`__

Wraps command **slicetimer**

use FSL slicetimer to perform slice timing correction.

Examples
~~~~~~~~
>>> from nipype.interfaces import fsl
>>> from nipype.testing import example_data
>>> st = fsl.SliceTimer()
>>> st.inputs.in_file = example_data('functional.nii')
>>> st.inputs.interleaved = True
>>> result = st.run() #doctest: +SKIP

Inputs::

        [Mandatory]
        in_file: (an existing file name)
                filename of input timeseries
                flag: --in=%s, position: 0
        terminal_output: ('stream' or 'allatonce' or 'file' or 'none')
                Control terminal output: `stream` - displays to terminal
                immediately, `allatonce` - waits till command is finished to display
                output, `file` - writes output to file, `none` - output is ignored

        [Optional]
        args: (a string)
                Additional parameters to the command
                flag: %s
        custom_order: (an existing file name)
                filename of single-column custom interleave order file (first slice
                is referred to as 1 not 0)
                flag: --ocustom=%s
        custom_timings: (an existing file name)
                slice timings, in fractions of TR, range 0:1 (default is 0.5 = no
                shift)
                flag: --tcustom=%s
        environ: (a dictionary with keys which are a value of type 'str' and
                 with values which are a value of type 'str', nipype default value:
                 {})
                Environment variables
        global_shift: (a float)
                shift in fraction of TR, range 0:1 (default is 0.5 = no shift)
                flag: --tglobal
        ignore_exception: (a boolean, nipype default value: False)
                Print an error message instead of throwing an exception in case the
                interface fails to run
        index_dir: (a boolean)
                slice indexing from top to bottom
                flag: --down
        interleaved: (a boolean)
                use interleaved acquisition
                flag: --odd
        out_file: (a file name)
                filename of output timeseries
                flag: --out=%s
        output_type: ('NIFTI_PAIR' or 'NIFTI_PAIR_GZ' or 'NIFTI_GZ' or
                 'NIFTI')
                FSL output type
        slice_direction: (1 or 2 or 3)
                direction of slice acquisition (x=1, y=2, z=3) - default is z
                flag: --direction=%d
        time_repetition: (a float)
                Specify TR of data - default is 3s
                flag: --repeat=%f

Outputs::

        slice_time_corrected_file: (an existing file name)
                slice time corrected file
