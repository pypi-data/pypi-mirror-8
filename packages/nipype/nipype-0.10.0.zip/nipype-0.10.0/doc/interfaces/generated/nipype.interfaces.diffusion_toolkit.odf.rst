.. AUTO-GENERATED FILE -- DO NOT EDIT!

interfaces.diffusion_toolkit.odf
================================


.. _nipype.interfaces.diffusion_toolkit.odf.HARDIMat:


.. index:: HARDIMat

HARDIMat
--------

`Link to code <http://github.com/nipy/nipype/tree/e63e055194d62d2bdc4665688261c03a42fd0025/nipype/interfaces/diffusion_toolkit/odf.py#L54>`__

Wraps command **hardi_mat**

Use hardi_mat to calculate a reconstruction matrix from a gradient table

Inputs::

        [Mandatory]
        bvals: (an existing file name)
                b values file
        bvecs: (an existing file name)
                b vectors file
                flag: %s, position: 1
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
        image_info: (an existing file name)
                specify image information file. the image info file is generated
                 from original dicom image by diff_unpack program and contains image
                 orientation and other information needed for reconstruction and
                 tracking. by default will look into the image folder for .info file
                flag: -info %s
        image_orientation_vectors: (a list of from 6 to 6 items which are a
                 float)
                specify image orientation vectors. if just one argument given,
                 will treat it as filename and read the orientation vectors from
                 the file. if 6 arguments are given, will treat them as 6 float
                 numbers and construct the 1st and 2nd vector and calculate the 3rd
                 one automatically.
                 this information will be used to determine image orientation,
                 as well as to adjust gradient vectors with oblique angle when
                flag: -iop %f
        oblique_correction: (a boolean)
                when oblique angle(s) applied, some SIEMENS dti protocols do not
                 adjust gradient accordingly, thus it requires adjustment for
                correct
                 diffusion tensor calculation
                flag: -oc
        odf_file: (an existing file name)
                filename that contains the reconstruction points on a HEMI-sphere.
                 use the pre-set 181 points by default
                flag: -odf %s
        order: (an integer)
                maximum order of spherical harmonics. must be even number. default
                 is 4
                flag: -order %s
        out_file: (a file name, nipype default value: recon_mat.dat)
                output matrix file
                flag: %s, position: 2
        reference_file: (an existing file name)
                provide a dicom or nifti image as the reference for the program to
                 figure out the image orientation information. if no such info was
                 found in the given image header, the next 5 options -info, etc.,
                 will be used if provided. if image orientation info can be found
                 in the given reference, all other 5 image orientation options will
                 be IGNORED
                flag: -ref %s

Outputs::

        out_file: (an existing file name)
                output matrix file

.. _nipype.interfaces.diffusion_toolkit.odf.ODFRecon:


.. index:: ODFRecon

ODFRecon
--------

`Link to code <http://github.com/nipy/nipype/tree/e63e055194d62d2bdc4665688261c03a42fd0025/nipype/interfaces/diffusion_toolkit/odf.py#L126>`__

Wraps command **odf_recon**

Use odf_recon to generate tensors and other maps

Inputs::

        [Mandatory]
        DWI: (an existing file name)
                Input raw data
                flag: %s, position: 1
        matrix: (an existing file name)
                use given file as reconstruction matrix.
                flag: -mat %s
        n_b0: (an integer)
                number of b0 scans. by default the program gets this information
                 from the number of directions and number of volumes in
                 the raw data. useful when dealing with incomplete raw
                 data set or only using part of raw data set to reconstruct
                flag: -b0 %s
        n_directions: (an integer)
                Number of directions
                flag: %s, position: 2
        n_output_directions: (an integer)
                Number of output directions
                flag: %s, position: 3
        terminal_output: ('stream' or 'allatonce' or 'file' or 'none')
                Control terminal output: `stream` - displays to terminal
                immediately, `allatonce` - waits till command is finished to display
                output, `file` - writes output to file, `none` - output is ignored

        [Optional]
        args: (a string)
                Additional parameters to the command
                flag: %s
        dsi: (a boolean)
                indicates that the data is dsi
                flag: -dsi
        environ: (a dictionary with keys which are a value of type 'str' and
                 with values which are a value of type 'str', nipype default value:
                 {})
                Environment variables
        filter: (a boolean)
                apply a filter (e.g. high pass) to the raw image
                flag: -f
        ignore_exception: (a boolean, nipype default value: False)
                Print an error message instead of throwing an exception in case the
                interface fails to run
        image_orientation_vectors: (a list of from 6 to 6 items which are a
                 float)
                specify image orientation vectors. if just one argument given,
                 will treat it as filename and read the orientation vectors from
                 the file. if 6 arguments are given, will treat them as 6 float
                 numbers and construct the 1st and 2nd vector and calculate the 3rd
                 one automatically.
                 this information will be used to determine image orientation,
                 as well as to adjust gradient vectors with oblique angle when
                flag: -iop %f
        oblique_correction: (a boolean)
                when oblique angle(s) applied, some SIEMENS dti protocols do not
                 adjust gradient accordingly, thus it requires adjustment for
                correct
                 diffusion tensor calculation
                flag: -oc
        out_prefix: (a string, nipype default value: odf)
                Output file prefix
                flag: %s, position: 4
        output_entropy: (a boolean)
                output entropy map
                flag: -oe
        output_type: ('nii' or 'analyze' or 'ni1' or 'nii.gz', nipype default
                 value: nii)
                output file type
                flag: -ot %s
        sharpness: (a float)
                smooth or sharpen the raw data. factor > 0 is smoothing.
                 factor < 0 is sharpening. default value is 0
                 NOTE: this option applies to DSI study only
                flag: -s %f
        subtract_background: (a boolean)
                subtract the background value before reconstruction
                flag: -bg

Outputs::

        B0: (an existing file name)
        DWI: (an existing file name)
        ODF: (an existing file name)
        entropy: (a file name)
        max: (an existing file name)

.. _nipype.interfaces.diffusion_toolkit.odf.ODFTracker:


.. index:: ODFTracker

ODFTracker
----------

`Link to code <http://github.com/nipy/nipype/tree/e63e055194d62d2bdc4665688261c03a42fd0025/nipype/interfaces/diffusion_toolkit/odf.py#L205>`__

Wraps command **odf_tracker**

Use odf_tracker to generate track file

Inputs::

        [Mandatory]
        ODF: (an existing file name)
        mask1_file: (a file name)
                first mask image
                flag: -m %s, position: 2
        max: (an existing file name)
        terminal_output: ('stream' or 'allatonce' or 'file' or 'none')
                Control terminal output: `stream` - displays to terminal
                immediately, `allatonce` - waits till command is finished to display
                output, `file` - writes output to file, `none` - output is ignored

        [Optional]
        angle_threshold: (a float)
                set angle threshold. default value is 35 degree for
                 default tracking method and 25 for rk2
                flag: -at %f
        args: (a string)
                Additional parameters to the command
                flag: %s
        disc: (a boolean)
                use disc tracking
                flag: -disc
        dsi: (a boolean)
                 specify the input odf data is dsi. because dsi recon uses fixed
                 pre-calculated matrix, some special orientation patch needs to
                 be applied to keep dti/dsi/q-ball consistent.
                flag: -dsi
        environ: (a dictionary with keys which are a value of type 'str' and
                 with values which are a value of type 'str', nipype default value:
                 {})
                Environment variables
        ignore_exception: (a boolean, nipype default value: False)
                Print an error message instead of throwing an exception in case the
                interface fails to run
        image_orientation_vectors: (a list of from 6 to 6 items which are a
                 float)
                specify image orientation vectors. if just one argument given,
                 will treat it as filename and read the orientation vectors from
                 the file. if 6 arguments are given, will treat them as 6 float
                 numbers and construct the 1st and 2nd vector and calculate the 3rd
                 one automatically.
                 this information will be used to determine image orientation,
                 as well as to adjust gradient vectors with oblique angle when
                flag: -iop %f
        input_data_prefix: (a string, nipype default value: odf)
                recon data prefix
                flag: %s, position: 0
        input_output_type: ('nii' or 'analyze' or 'ni1' or 'nii.gz', nipype
                 default value: nii)
                input and output file type
                flag: -it %s
        invert_x: (a boolean)
                invert x component of the vector
                flag: -ix
        invert_y: (a boolean)
                invert y component of the vector
                flag: -iy
        invert_z: (a boolean)
                invert z component of the vector
                flag: -iz
        limit: (an integer)
                in some special case, such as heart data, some track may go into
                 infinite circle and take long time to stop. this option allows
                 setting a limit for the longest tracking steps (voxels)
                flag: -limit %d
        mask1_threshold: (a float)
                threshold value for the first mask image, if not given, the program
                will try automatically find the threshold
        mask2_file: (a file name)
                second mask image
                flag: -m2 %s, position: 4
        mask2_threshold: (a float)
                threshold value for the second mask image, if not given, the program
                will try automatically find the threshold
        out_file: (a file name, nipype default value: tracks.trk)
                output track file
                flag: %s, position: 1
        random_seed: (an integer)
                use random location in a voxel instead of the center of the voxel
                 to seed. can also define number of seed per voxel. default is 1
                flag: -rseed %s
        runge_kutta2: (a boolean)
                use 2nd order runge-kutta method for tracking.
                 default tracking method is non-interpolate streamline
                flag: -rk2
        slice_order: (an integer)
                set the slice order. 1 means normal, -1 means reversed. default
                value is 1
                flag: -sorder %d
        step_length: (a float)
                set step length, in the unit of minimum voxel size.
                 default value is 0.1.
                flag: -l %f
        swap_xy: (a boolean)
                swap x and y vectors while tracking
                flag: -sxy
        swap_yz: (a boolean)
                swap y and z vectors while tracking
                flag: -syz
        swap_zx: (a boolean)
                swap x and z vectors while tracking
                flag: -szx
        voxel_order: ('RAS' or 'RPS' or 'RAI' or 'RPI' or 'LAI' or 'LAS' or
                 'LPS' or 'LPI')
                specify the voxel order in RL/AP/IS (human brain) reference. must be
                 3 letters with no space in between.
                 for example, RAS means the voxel row is from L->R, the column
                 is from P->A and the slice order is from I->S.
                 by default voxel order is determined by the image orientation
                 (but NOT guaranteed to be correct because of various standards).
                 for example, siemens axial image is LPS, coronal image is LIP and
                 sagittal image is PIL.
                 this information also is NOT needed for tracking but will be saved
                 in the track file and is essential for track display to map onto
                 the right coordinates
                flag: -vorder %s

Outputs::

        track_file: (an existing file name)
                output track file
