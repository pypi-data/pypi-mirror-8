.. AUTO-GENERATED FILE -- DO NOT EDIT!

interfaces.freesurfer.preprocess
================================


.. _nipype.interfaces.freesurfer.preprocess.ApplyVolTransform:


.. index:: ApplyVolTransform

ApplyVolTransform
-----------------

`Link to code <http://github.com/nipy/nipype/tree/e63e055194d62d2bdc4665688261c03a42fd0025/nipype/interfaces/freesurfer/preprocess.py#L976>`__

Wraps command **mri_vol2vol**

Use FreeSurfer mri_vol2vol to apply a transform.

Examples
~~~~~~~~

>>> from nipype.interfaces.freesurfer import ApplyVolTransform
>>> applyreg = ApplyVolTransform()
>>> applyreg.inputs.source_file = 'structural.nii'
>>> applyreg.inputs.reg_file = 'register.dat'
>>> applyreg.inputs.transformed_file = 'struct_warped.nii'
>>> applyreg.inputs.fs_target = True
>>> applyreg.cmdline
'mri_vol2vol --fstarg --reg register.dat --mov structural.nii --o struct_warped.nii'

Inputs::

        [Mandatory]
        fs_target: (a boolean)
                use orig.mgz from subject in regfile as target
                flag: --fstarg
                mutually_exclusive: target_file, tal, fs_target
                requires: reg_file
        fsl_reg_file: (an existing file name)
                fslRAS-to-fslRAS matrix (FSL format)
                flag: --fsl %s
                mutually_exclusive: reg_file, fsl_reg_file, xfm_reg_file,
                 reg_header, subject
        reg_file: (an existing file name)
                tkRAS-to-tkRAS matrix (tkregister2 format)
                flag: --reg %s
                mutually_exclusive: reg_file, fsl_reg_file, xfm_reg_file,
                 reg_header, subject
        reg_header: (a boolean)
                ScannerRAS-to-ScannerRAS matrix = identity
                flag: --regheader
                mutually_exclusive: reg_file, fsl_reg_file, xfm_reg_file,
                 reg_header, subject
        source_file: (an existing file name)
                Input volume you wish to transform
                flag: --mov %s
        subject: (a string)
                set matrix = identity and use subject for any templates
                flag: --s %s
                mutually_exclusive: reg_file, fsl_reg_file, xfm_reg_file,
                 reg_header, subject
        tal: (a boolean)
                map to a sub FOV of MNI305 (with --reg only)
                flag: --tal
                mutually_exclusive: target_file, tal, fs_target
        target_file: (an existing file name)
                Output template volume
                flag: --targ %s
                mutually_exclusive: target_file, tal, fs_target
        terminal_output: ('stream' or 'allatonce' or 'file' or 'none')
                Control terminal output: `stream` - displays to terminal
                immediately, `allatonce` - waits till command is finished to display
                output, `file` - writes output to file, `none` - output is ignored
        xfm_reg_file: (an existing file name)
                ScannerRAS-to-ScannerRAS matrix (MNI format)
                flag: --xfm %s
                mutually_exclusive: reg_file, fsl_reg_file, xfm_reg_file,
                 reg_header, subject

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
        interp: ('trilin' or 'nearest' or 'cubic')
                Interpolation method (<trilin> or nearest)
                flag: --interp %s
        inverse: (a boolean)
                sample from target to source
                flag: --inv
        invert_morph: (a boolean)
                Compute and use the inverse of the non-linear morph to resample the
                input volume. To be used by --m3z.
                flag: --inv-morph
                requires: m3z_file
        m3z_file: (a file name)
                This is the morph to be applied to the volume. Unless the morph is
                in mri/transforms (eg.: for talairach.m3z computed by reconall), you
                will need to specify the full path to this morph and use the
                --noDefM3zPath flag.
                flag: --m3z %s
        no_ded_m3z_path: (a boolean)
                To be used with the m3z flag. Instructs the code not to look for
                them3z morph in the default location
                (SUBJECTS_DIR/subj/mri/transforms), but instead just use the path
                indicated in --m3z.
                flag: --noDefM3zPath
                requires: m3z_file
        no_resample: (a boolean)
                Do not resample; just change vox2ras matrix
                flag: --no-resample
        subjects_dir: (an existing directory name)
                subjects directory
        tal_resolution: (a float)
                Resolution to sample when using tal
                flag: --talres %.10f
        transformed_file: (a file name)
                Output volume
                flag: --o %s

Outputs::

        transformed_file: (an existing file name)
                Path to output file if used normally

.. _nipype.interfaces.freesurfer.preprocess.BBRegister:


.. index:: BBRegister

BBRegister
----------

`Link to code <http://github.com/nipy/nipype/tree/e63e055194d62d2bdc4665688261c03a42fd0025/nipype/interfaces/freesurfer/preprocess.py#L842>`__

Wraps command **bbregister**

Use FreeSurfer bbregister to register a volume to the Freesurfer anatomical.

This program performs within-subject, cross-modal registration using a
boundary-based cost function. The registration is constrained to be 6
DOF (rigid). It is required that you have an anatomical scan of the
subject that has already been recon-all-ed using freesurfer.

Examples
~~~~~~~~

>>> from nipype.interfaces.freesurfer import BBRegister
>>> bbreg = BBRegister(subject_id='me', source_file='structural.nii', init='header', contrast_type='t2')
>>> bbreg.cmdline
'bbregister --t2 --init-header --reg structural_bbreg_me.dat --mov structural.nii --s me'

Inputs::

        [Mandatory]
        contrast_type: ('t1' or 't2')
                contrast type of image
                flag: --%s
        init: ('spm' or 'fsl' or 'header')
                initialize registration spm, fsl, header
                flag: --init-%s
                mutually_exclusive: init_reg_file
        init_reg_file: (an existing file name)
                existing registration file
                flag: --init-reg %s
                mutually_exclusive: init
        source_file: (a file name)
                source file to be registered
                flag: --mov %s
        subject_id: (a string)
                freesurfer subject id
                flag: --s %s
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
        epi_mask: (a boolean)
                mask out B0 regions in stages 1 and 2
                flag: --epi-mask
        ignore_exception: (a boolean, nipype default value: False)
                Print an error message instead of throwing an exception in case the
                interface fails to run
        intermediate_file: (an existing file name)
                Intermediate image, e.g. in case of partial FOV
                flag: --int %s
        out_fsl_file: (a boolean or a file name)
                write the transformation matrix in FSL FLIRT format
                flag: --fslmat %s
        out_reg_file: (a file name)
                output registration file
                flag: --reg %s
        reg_frame: (an integer)
                0-based frame index for 4D source file
                flag: --frame %d
                mutually_exclusive: reg_middle_frame
        reg_middle_frame: (a boolean)
                Register middle frame of 4D source file
                flag: --mid-frame
                mutually_exclusive: reg_frame
        registered_file: (a boolean or a file name)
                output warped sourcefile either True or filename
                flag: --o %s
        spm_nifti: (a boolean)
                force use of nifti rather than analyze with SPM
                flag: --spm-nii
        subjects_dir: (an existing directory name)
                subjects directory

Outputs::

        min_cost_file: (an existing file name)
                Output registration minimum cost file
        out_fsl_file: (a file name)
                Output FLIRT-style registration file
        out_reg_file: (an existing file name)
                Output registration file
        registered_file: (a file name)
                Registered and resampled source file

.. _nipype.interfaces.freesurfer.preprocess.DICOMConvert:


.. index:: DICOMConvert

DICOMConvert
------------

`Link to code <http://github.com/nipy/nipype/tree/e63e055194d62d2bdc4665688261c03a42fd0025/nipype/interfaces/freesurfer/preprocess.py#L439>`__

Wraps command **mri_convert**

use fs mri_convert to convert dicom files

Examples
~~~~~~~~

>>> from nipype.interfaces.freesurfer import DICOMConvert
>>> cvt = DICOMConvert()
>>> cvt.inputs.dicom_dir = 'dicomdir'
>>> cvt.inputs.file_mapping = [('nifti', '*.nii'), ('info', 'dicom*.txt'), ('dti', '*dti.bv*')]

Inputs::

        [Mandatory]
        base_output_dir: (a directory name)
                directory in which subject directories are created
        dicom_dir: (an existing directory name)
                dicom directory from which to convert dicom files
        terminal_output: ('stream' or 'allatonce' or 'file' or 'none')
                Control terminal output: `stream` - displays to terminal
                immediately, `allatonce` - waits till command is finished to display
                output, `file` - writes output to file, `none` - output is ignored

        [Optional]
        args: (a string)
                Additional parameters to the command
                flag: %s
        dicom_info: (an existing file name)
                File containing summary information from mri_parse_sdcmdir
        environ: (a dictionary with keys which are a value of type 'str' and
                 with values which are a value of type 'str', nipype default value:
                 {})
                Environment variables
        file_mapping: (a list of items which are a tuple of the form: (a
                 string, a string))
                defines the output fields of interface
        ignore_exception: (a boolean, nipype default value: False)
                Print an error message instead of throwing an exception in case the
                interface fails to run
        ignore_single_slice: (a boolean)
                ignore volumes containing a single slice
                requires: dicom_info
        out_type: ('cor' or 'mgh' or 'mgz' or 'minc' or 'analyze' or
                 'analyze4d' or 'spm' or 'afni' or 'brik' or 'bshort' or 'bfloat' or
                 'sdt' or 'outline' or 'otl' or 'gdf' or 'nifti1' or 'nii' or
                 'niigz', nipype default value: niigz)
                defines the type of output file produced
        seq_list: (a list of items which are a string)
                list of pulse sequence names to be converted.
                requires: dicom_info
        subject_dir_template: (a string, nipype default value: S.%04d)
                template for subject directory name
        subject_id
                subject identifier to insert into template
        subjects_dir: (an existing directory name)
                subjects directory

Outputs::

        None

.. _nipype.interfaces.freesurfer.preprocess.FitMSParams:


.. index:: FitMSParams

FitMSParams
-----------

`Link to code <http://github.com/nipy/nipype/tree/e63e055194d62d2bdc4665688261c03a42fd0025/nipype/interfaces/freesurfer/preprocess.py#L1249>`__

Wraps command **mri_ms_fitparms**

Estimate tissue paramaters from a set of FLASH images.

Examples
~~~~~~~~
>>> from nipype.interfaces.freesurfer import FitMSParams
>>> msfit = FitMSParams()
>>> msfit.inputs.in_files = ['flash_05.mgz', 'flash_30.mgz']
>>> msfit.inputs.out_dir = 'flash_parameters'
>>> msfit.cmdline
'mri_ms_fitparms  flash_05.mgz flash_30.mgz flash_parameters'

Inputs::

        [Mandatory]
        in_files: (a list of items which are an existing file name)
                list of FLASH images (must be in mgh format)
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
        flip_list: (a list of items which are an integer)
                list of flip angles of the input files
        ignore_exception: (a boolean, nipype default value: False)
                Print an error message instead of throwing an exception in case the
                interface fails to run
        out_dir: (a directory name)
                directory to store output in
                flag: %s, position: -1
        subjects_dir: (an existing directory name)
                subjects directory
        te_list: (a list of items which are a float)
                list of TEs of the input files (in msec)
        tr_list: (a list of items which are an integer)
                list of TRs of the input files (in msec)
        xfm_list: (a list of items which are an existing file name)
                list of transform files to apply to each FLASH image

Outputs::

        pd_image: (an existing file name)
                image of estimated proton density values
        t1_image: (an existing file name)
                image of estimated T1 relaxation values
        t2star_image: (an existing file name)
                image of estimated T2* values

.. _nipype.interfaces.freesurfer.preprocess.MRIConvert:


.. index:: MRIConvert

MRIConvert
----------

`Link to code <http://github.com/nipy/nipype/tree/e63e055194d62d2bdc4665688261c03a42fd0025/nipype/interfaces/freesurfer/preprocess.py#L325>`__

Wraps command **mri_convert**

use fs mri_convert to manipulate files

.. note::
   Adds niigz as an output type option

Examples
~~~~~~~~

>>> mc = MRIConvert()
>>> mc.inputs.in_file = 'structural.nii'
>>> mc.inputs.out_file = 'outfile.mgz'
>>> mc.inputs.out_type = 'mgz'
>>> mc.cmdline
'mri_convert --out_type mgz --input_volume structural.nii --output_volume outfile.mgz'

Inputs::

        [Mandatory]
        in_file: (an existing file name)
                File to read/convert
                flag: --input_volume %s, position: -2
        terminal_output: ('stream' or 'allatonce' or 'file' or 'none')
                Control terminal output: `stream` - displays to terminal
                immediately, `allatonce` - waits till command is finished to display
                output, `file` - writes output to file, `none` - output is ignored

        [Optional]
        apply_inv_transform: (an existing file name)
                apply inverse transformation xfm file
                flag: --apply_inverse_transform %s
        apply_transform: (an existing file name)
                apply xfm file
                flag: --apply_transform %s
        args: (a string)
                Additional parameters to the command
                flag: %s
        ascii: (a boolean)
                save output as ascii col>row>slice>frame
                flag: --ascii
        autoalign_matrix: (an existing file name)
                text file with autoalign matrix
                flag: --autoalign %s
        color_file: (an existing file name)
                color file
                flag: --color_file %s
        conform: (a boolean)
                conform to 256^3
                flag: --conform
        conform_min: (a boolean)
                conform to smallest size
                flag: --conform_min
        conform_size: (a float)
                conform to size_in_mm
                flag: --conform_size %s
        crop_center: (a tuple of the form: (an integer, an integer, an
                 integer))
                <x> <y> <z> crop to 256 around center (x, y, z)
                flag: --crop %d %d %d
        crop_gdf: (a boolean)
                apply GDF cropping
                flag: --crop_gdf
        crop_size: (a tuple of the form: (an integer, an integer, an
                 integer))
                <dx> <dy> <dz> crop to size <dx, dy, dz>
                flag: --cropsize %d %d %d
        cut_ends: (an integer)
                remove ncut slices from the ends
                flag: --cutends %d
        devolve_transform: (a string)
                subject id
                flag: --devolvexfm %s
        drop_n: (an integer)
                drop the last n frames
                flag: --ndrop %d
        environ: (a dictionary with keys which are a value of type 'str' and
                 with values which are a value of type 'str', nipype default value:
                 {})
                Environment variables
        fill_parcellation: (a boolean)
                fill parcellation
                flag: --fill_parcellation
        force_ras: (a boolean)
                use default when orientation info absent
                flag: --force_ras_good
        frame: (an integer)
                keep only 0-based frame number
                flag: --frame %d
        frame_subsample: (a tuple of the form: (an integer, an integer, an
                 integer))
                start delta end : frame subsampling (end = -1 for end)
                flag: --fsubsample %d %d %d
        fwhm: (a float)
                smooth input volume by fwhm mm
                flag: --fwhm %f
        ignore_exception: (a boolean, nipype default value: False)
                Print an error message instead of throwing an exception in case the
                interface fails to run
        in_center: (a list of at most 3 items which are a float)
                <R coordinate> <A coordinate> <S coordinate>
                flag: --in_center %s
        in_i_dir: (a tuple of the form: (a float, a float, a float))
                <R direction> <A direction> <S direction>
                flag: --in_i_direction %f %f %f
        in_i_size: (an integer)
                input i size
                flag: --in_i_size %d
        in_info: (a boolean)
                display input info
                flag: --in_info
        in_j_dir: (a tuple of the form: (a float, a float, a float))
                <R direction> <A direction> <S direction>
                flag: --in_j_direction %f %f %f
        in_j_size: (an integer)
                input j size
                flag: --in_j_size %d
        in_k_dir: (a tuple of the form: (a float, a float, a float))
                <R direction> <A direction> <S direction>
                flag: --in_k_direction %f %f %f
        in_k_size: (an integer)
                input k size
                flag: --in_k_size %d
        in_like: (an existing file name)
                input looks like
                flag: --in_like %s
        in_matrix: (a boolean)
                display input matrix
                flag: --in_matrix
        in_orientation: ('LAI' or 'LIA' or 'ALI' or 'AIL' or 'ILA' or 'IAL'
                 or 'LAS' or 'LSA' or 'ALS' or 'ASL' or 'SLA' or 'SAL' or 'LPI' or
                 'LIP' or 'PLI' or 'PIL' or 'ILP' or 'IPL' or 'LPS' or 'LSP' or
                 'PLS' or 'PSL' or 'SLP' or 'SPL' or 'RAI' or 'RIA' or 'ARI' or
                 'AIR' or 'IRA' or 'IAR' or 'RAS' or 'RSA' or 'ARS' or 'ASR' or
                 'SRA' or 'SAR' or 'RPI' or 'RIP' or 'PRI' or 'PIR' or 'IRP' or
                 'IPR' or 'RPS' or 'RSP' or 'PRS' or 'PSR' or 'SRP' or 'SPR')
                specify the input orientation
                flag: --in_orientation %s
        in_scale: (a float)
                input intensity scale factor
                flag: --scale %f
        in_stats: (a boolean)
                display input stats
                flag: --in_stats
        in_type: ('cor' or 'mgh' or 'mgz' or 'minc' or 'analyze' or
                 'analyze4d' or 'spm' or 'afni' or 'brik' or 'bshort' or 'bfloat' or
                 'sdt' or 'outline' or 'otl' or 'gdf' or 'nifti1' or 'nii' or
                 'niigz' or 'ge' or 'gelx' or 'lx' or 'ximg' or 'siemens' or 'dicom'
                 or 'siemens_dicom')
                input file type
                flag: --in_type %s
        invert_contrast: (a float)
                threshold for inversting contrast
                flag: --invert_contrast %f
        midframe: (a boolean)
                keep only the middle frame
                flag: --mid-frame
        no_change: (a boolean)
                don't change type of input to that of template
                flag: --nochange
        no_scale: (a boolean)
                dont rescale values for COR
                flag: --no_scale 1
        no_translate: (a boolean)
                ~~~
                flag: --no_translate
        no_write: (a boolean)
                do not write output
                flag: --no_write
        out_center: (a tuple of the form: (a float, a float, a float))
                <R coordinate> <A coordinate> <S coordinate>
                flag: --out_center %f %f %f
        out_datatype: ('uchar' or 'short' or 'int' or 'float')
                output data type <uchar|short|int|float>
                flag: --out_data_type %s
        out_file: (a file name)
                output filename or True to generate one
                flag: --output_volume %s, position: -1
        out_i_count: (an integer)
                some count ?? in i direction
                flag: --out_i_count %d
        out_i_dir: (a tuple of the form: (a float, a float, a float))
                <R direction> <A direction> <S direction>
                flag: --out_i_direction %f %f %f
        out_i_size: (an integer)
                output i size
                flag: --out_i_size %d
        out_info: (a boolean)
                display output info
                flag: --out_info
        out_j_count: (an integer)
                some count ?? in j direction
                flag: --out_j_count %d
        out_j_dir: (a tuple of the form: (a float, a float, a float))
                <R direction> <A direction> <S direction>
                flag: --out_j_direction %f %f %f
        out_j_size: (an integer)
                output j size
                flag: --out_j_size %d
        out_k_count: (an integer)
                some count ?? in k direction
                flag: --out_k_count %d
        out_k_dir: (a tuple of the form: (a float, a float, a float))
                <R direction> <A direction> <S direction>
                flag: --out_k_direction %f %f %f
        out_k_size: (an integer)
                output k size
                flag: --out_k_size %d
        out_matrix: (a boolean)
                display output matrix
                flag: --out_matrix
        out_orientation: ('LAI' or 'LIA' or 'ALI' or 'AIL' or 'ILA' or 'IAL'
                 or 'LAS' or 'LSA' or 'ALS' or 'ASL' or 'SLA' or 'SAL' or 'LPI' or
                 'LIP' or 'PLI' or 'PIL' or 'ILP' or 'IPL' or 'LPS' or 'LSP' or
                 'PLS' or 'PSL' or 'SLP' or 'SPL' or 'RAI' or 'RIA' or 'ARI' or
                 'AIR' or 'IRA' or 'IAR' or 'RAS' or 'RSA' or 'ARS' or 'ASR' or
                 'SRA' or 'SAR' or 'RPI' or 'RIP' or 'PRI' or 'PIR' or 'IRP' or
                 'IPR' or 'RPS' or 'RSP' or 'PRS' or 'PSR' or 'SRP' or 'SPR')
                specify the output orientation
                flag: --out_orientation %s
        out_scale: (a float)
                output intensity scale factor
                flag: --out-scale %d
        out_stats: (a boolean)
                display output stats
                flag: --out_stats
        out_type: ('cor' or 'mgh' or 'mgz' or 'minc' or 'analyze' or
                 'analyze4d' or 'spm' or 'afni' or 'brik' or 'bshort' or 'bfloat' or
                 'sdt' or 'outline' or 'otl' or 'gdf' or 'nifti1' or 'nii' or
                 'niigz')
                output file type
                flag: --out_type %s
        parse_only: (a boolean)
                parse input only
                flag: --parse_only
        read_only: (a boolean)
                read the input volume
                flag: --read_only
        reorder: (a tuple of the form: (an integer, an integer, an integer))
                olddim1 olddim2 olddim3
                flag: --reorder %d %d %d
        resample_type: ('interpolate' or 'weighted' or 'nearest' or 'sinc' or
                 'cubic')
                <interpolate|weighted|nearest|sinc|cubic> (default is interpolate)
                flag: --resample_type %s
        reslice_like: (an existing file name)
                reslice output to match file
                flag: --reslice_like %s
        sdcm_list: (an existing file name)
                list of DICOM files for conversion
                flag: --sdcmlist %s
        skip_n: (an integer)
                skip the first n frames
                flag: --nskip %d
        slice_bias: (a float)
                apply half-cosine bias field
                flag: --slice-bias %f
        slice_crop: (a tuple of the form: (an integer, an integer))
                s_start s_end : keep slices s_start to s_end
                flag: --slice-crop %d %d
        slice_reverse: (a boolean)
                reverse order of slices, update vox2ras
                flag: --slice-reverse
        smooth_parcellation: (a boolean)
                smooth parcellation
                flag: --smooth_parcellation
        sphinx: (a boolean)
                change orientation info to sphinx
                flag: --sphinx
        split: (a boolean)
                split output frames into separate output files.
                flag: --split
        status_file: (a file name)
                status file for DICOM conversion
                flag: --status %s
        subject_name: (a string)
                subject name ???
                flag: --subject_name %s
        subjects_dir: (an existing directory name)
                subjects directory
        template_info: (a boolean)
                dump info about template
        template_type: ('cor' or 'mgh' or 'mgz' or 'minc' or 'analyze' or
                 'analyze4d' or 'spm' or 'afni' or 'brik' or 'bshort' or 'bfloat' or
                 'sdt' or 'outline' or 'otl' or 'gdf' or 'nifti1' or 'nii' or
                 'niigz' or 'ge' or 'gelx' or 'lx' or 'ximg' or 'siemens' or 'dicom'
                 or 'siemens_dicom')
                template file type
                flag: --template_type %s
        unwarp_gradient: (a boolean)
                unwarp gradient nonlinearity
                flag: --unwarp_gradient_nonlinearity
        vox_size: (a tuple of the form: (a float, a float, a float))
                <size_x> <size_y> <size_z> specify the size (mm) - useful for
                upsampling or downsampling
                flag: -voxsize %f %f %f
        zero_ge_z_offset: (a boolean)
                zero ge z offset ???
                flag: --zero_ge_z_offset
        zero_outlines: (a boolean)
                zero outlines
                flag: --zero_outlines

Outputs::

        out_file: (an existing file name)
                converted output file

.. _nipype.interfaces.freesurfer.preprocess.ParseDICOMDir:


.. index:: ParseDICOMDir

ParseDICOMDir
-------------

`Link to code <http://github.com/nipy/nipype/tree/e63e055194d62d2bdc4665688261c03a42fd0025/nipype/interfaces/freesurfer/preprocess.py#L49>`__

Wraps command **mri_parse_sdcmdir**

Uses mri_parse_sdcmdir to get information from dicom directories

Examples
~~~~~~~~

>>> from nipype.interfaces.freesurfer import ParseDICOMDir
>>> dcminfo = ParseDICOMDir()
>>> dcminfo.inputs.dicom_dir = '.'
>>> dcminfo.inputs.sortbyrun = True
>>> dcminfo.inputs.summarize = True
>>> dcminfo.cmdline
'mri_parse_sdcmdir --d . --o dicominfo.txt --sortbyrun --summarize'

Inputs::

        [Mandatory]
        dicom_dir: (an existing directory name)
                path to siemens dicom directory
                flag: --d %s
        terminal_output: ('stream' or 'allatonce' or 'file' or 'none')
                Control terminal output: `stream` - displays to terminal
                immediately, `allatonce` - waits till command is finished to display
                output, `file` - writes output to file, `none` - output is ignored

        [Optional]
        args: (a string)
                Additional parameters to the command
                flag: %s
        dicom_info_file: (a file name, nipype default value: dicominfo.txt)
                file to which results are written
                flag: --o %s
        environ: (a dictionary with keys which are a value of type 'str' and
                 with values which are a value of type 'str', nipype default value:
                 {})
                Environment variables
        ignore_exception: (a boolean, nipype default value: False)
                Print an error message instead of throwing an exception in case the
                interface fails to run
        sortbyrun: (a boolean)
                assign run numbers
                flag: --sortbyrun
        subjects_dir: (an existing directory name)
                subjects directory
        summarize: (a boolean)
                only print out info for run leaders
                flag: --summarize

Outputs::

        dicom_info_file: (an existing file name)
                text file containing dicom information

.. _nipype.interfaces.freesurfer.preprocess.ReconAll:


.. index:: ReconAll

ReconAll
--------

`Link to code <http://github.com/nipy/nipype/tree/e63e055194d62d2bdc4665688261c03a42fd0025/nipype/interfaces/freesurfer/preprocess.py#L619>`__

Wraps command **recon-all**

Uses recon-all to generate surfaces and parcellations of structural data
from anatomical images of a subject.

Examples
~~~~~~~~

>>> from nipype.interfaces.freesurfer import ReconAll
>>> reconall = ReconAll()
>>> reconall.inputs.subject_id = 'foo'
>>> reconall.inputs.directive = 'all'
>>> reconall.inputs.subjects_dir = '.'
>>> reconall.inputs.T1_files = 'structural.nii'
>>> reconall.cmdline
'recon-all -all -i structural.nii -subjid foo -sd .'

Inputs::

        [Mandatory]
        terminal_output: ('stream' or 'allatonce' or 'file' or 'none')
                Control terminal output: `stream` - displays to terminal
                immediately, `allatonce` - waits till command is finished to display
                output, `file` - writes output to file, `none` - output is ignored

        [Optional]
        T1_files: (an existing file name)
                name of T1 file to process
                flag: -i %s...
        T2_file: (an existing file name)
                Use a T2 image to refine the cortical surface
                flag: -T2 %s
        args: (a string)
                Additional parameters to the command
                flag: %s
        directive: ('all' or 'autorecon1' or 'autorecon2' or 'autorecon2-cp'
                 or 'autorecon2-wm' or 'autorecon2-inflate1' or 'autorecon2-perhemi'
                 or 'autorecon3' or 'localGI' or 'qcache', nipype default value:
                 all)
                process directive
                flag: -%s, position: 0
        environ: (a dictionary with keys which are a value of type 'str' and
                 with values which are a value of type 'str', nipype default value:
                 {})
                Environment variables
        flags: (a string)
                additional parameters
                flag: %s
        hemi: ('lh' or 'rh')
                hemisphere to process
                flag: -hemi %s
        ignore_exception: (a boolean, nipype default value: False)
                Print an error message instead of throwing an exception in case the
                interface fails to run
        openmp: (an integer)
                Number of processors to use in parallel
                flag: -openmp %d
        subject_id: (a string, nipype default value: recon_all)
                subject name
                flag: -subjid %s
        subjects_dir: (an existing directory name)
                path to subjects directory
                flag: -sd %s

Outputs::

        BA_stats: (an existing file name)
                Brodmann Area statistics files
        T1: (an existing file name)
                Intensity normalized whole-head volume
        annot: (an existing file name)
                Surface annotation files
        aparc_a2009s_stats: (an existing file name)
                Aparc a2009s parcellation statistics files
        aparc_aseg: (an existing file name)
                Aparc parcellation projected into aseg volume
        aparc_stats: (an existing file name)
                Aparc parcellation statistics files
        aseg: (an existing file name)
                Volumetric map of regions from automatic segmentation
        aseg_stats: (an existing file name)
                Automated segmentation statistics file
        brain: (an existing file name)
                Intensity normalized brain-only volume
        brainmask: (an existing file name)
                Skull-stripped (brain-only) volume
        curv: (an existing file name)
                Maps of surface curvature
        curv_stats: (an existing file name)
                Curvature statistics files
        entorhinal_exvivo_stats: (an existing file name)
                Entorhinal exvivo statistics files
        filled: (an existing file name)
                Subcortical mass volume
        inflated: (an existing file name)
                Inflated surface meshes
        label: (an existing file name)
                Volume and surface label files
        norm: (an existing file name)
                Normalized skull-stripped volume
        nu: (an existing file name)
                Non-uniformity corrected whole-head volume
        orig: (an existing file name)
                Base image conformed to Freesurfer space
        pial: (an existing file name)
                Gray matter/pia mater surface meshes
        rawavg: (an existing file name)
                Volume formed by averaging input images
        ribbon: (an existing file name)
                Volumetric maps of cortical ribbons
        smoothwm: (an existing file name)
                Smoothed original surface meshes
        sphere: (an existing file name)
                Spherical surface meshes
        sphere_reg: (an existing file name)
                Spherical registration file
        subject_id: (a string)
                Subject name for whom to retrieve data
        subjects_dir: (an existing directory name)
                Freesurfer subjects directory.
        sulc: (an existing file name)
                Surface maps of sulcal depth
        thickness: (an existing file name)
                Surface maps of cortical thickness
        volume: (an existing file name)
                Surface maps of cortical volume
        white: (an existing file name)
                White/gray matter surface meshes
        wm: (an existing file name)
                Segmented white-matter volume
        wmparc: (an existing file name)
                Aparc parcellation projected into subcortical white matter
        wmparc_stats: (an existing file name)
                White matter parcellation statistics file

.. _nipype.interfaces.freesurfer.preprocess.Resample:


.. index:: Resample

Resample
--------

`Link to code <http://github.com/nipy/nipype/tree/e63e055194d62d2bdc4665688261c03a42fd0025/nipype/interfaces/freesurfer/preprocess.py#L553>`__

Wraps command **mri_convert**

Use FreeSurfer mri_convert to up or down-sample image files

Examples
~~~~~~~~

>>> from nipype.interfaces import freesurfer
>>> resampler = freesurfer.Resample()
>>> resampler.inputs.in_file = 'structural.nii'
>>> resampler.inputs.resampled_file = 'resampled.nii'
>>> resampler.inputs.voxel_size = (2.1, 2.1, 2.1)
>>> resampler.cmdline
'mri_convert -vs 2.10 2.10 2.10 -i structural.nii -o resampled.nii'

Inputs::

        [Mandatory]
        in_file: (an existing file name)
                file to resample
                flag: -i %s, position: -2
        terminal_output: ('stream' or 'allatonce' or 'file' or 'none')
                Control terminal output: `stream` - displays to terminal
                immediately, `allatonce` - waits till command is finished to display
                output, `file` - writes output to file, `none` - output is ignored
        voxel_size: (a tuple of the form: (a float, a float, a float))
                triplet of output voxel sizes
                flag: -vs %.2f %.2f %.2f

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
        resampled_file: (a file name)
                output filename
                flag: -o %s, position: -1
        subjects_dir: (an existing directory name)
                subjects directory

Outputs::

        resampled_file: (an existing file name)
                output filename

.. _nipype.interfaces.freesurfer.preprocess.RobustRegister:


.. index:: RobustRegister

RobustRegister
--------------

`Link to code <http://github.com/nipy/nipype/tree/e63e055194d62d2bdc4665688261c03a42fd0025/nipype/interfaces/freesurfer/preprocess.py#L1161>`__

Wraps command **mri_robust_register**

Perform intramodal linear registration (translation and rotation) using robust statistics.

Examples
~~~~~~~~
>>> from nipype.interfaces.freesurfer import RobustRegister
>>> reg = RobustRegister()
>>> reg.inputs.source_file = 'structural.nii'
>>> reg.inputs.target_file = 'T1.nii'
>>> reg.inputs.auto_sens = True
>>> reg.inputs.init_orient = True
>>> reg.cmdline
'mri_robust_register --satit --initorient --lta structural_robustreg.lta --mov structural.nii --dst T1.nii'

References
~~~~~~~~~~
Reuter, M, Rosas, HD, and Fischl, B, (2010). Highly Accurate Inverse Consistent Registration:
A Robust Approach.  Neuroimage 53(4) 1181-96.

Inputs::

        [Mandatory]
        auto_sens: (a boolean)
                auto-detect good sensitivity
                flag: --satit
                mutually_exclusive: outlier_sens
        outlier_sens: (a float)
                set outlier sensitivity explicitly
                flag: --sat %.4f
                mutually_exclusive: auto_sens
        source_file: (a file name)
                volume to be registered
                flag: --mov %s
        target_file: (a file name)
                target volume for the registration
                flag: --dst %s
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
        est_int_scale: (a boolean)
                estimate intensity scale (recommended for unnormalized images)
                flag: --iscale
        force_double: (a boolean)
                use double-precision intensities
                flag: --doubleprec
        force_float: (a boolean)
                use float intensities
                flag: --floattype
        half_source: (a boolean or a file name)
                write source volume mapped to halfway space
                flag: --halfmov %s
        half_source_xfm: (a boolean or a file name)
                write transform from source to halfway space
                flag: --halfmovlta %s
        half_targ: (a boolean or a file name)
                write target volume mapped to halfway space
                flag: --halfdst %s
        half_targ_xfm: (a boolean or a file name)
                write transform from target to halfway space
                flag: --halfdstlta %s
        half_weights: (a boolean or a file name)
                write weights volume mapped to halfway space
                flag: --halfweights %s
        high_iterations: (an integer)
                max # of times on highest resolution
                flag: --highit %d
        ignore_exception: (a boolean, nipype default value: False)
                Print an error message instead of throwing an exception in case the
                interface fails to run
        in_xfm_file: (an existing file name)
                use initial transform on source
                flag: --transform
        init_orient: (a boolean)
                use moments for initial orient (recommended for stripped brains)
                flag: --initorient
        iteration_thresh: (a float)
                stop iterations when below threshold
                flag: --epsit %.3f
        least_squares: (a boolean)
                use least squares instead of robust estimator
                flag: --leastsquares
        mask_source: (an existing file name)
                image to mask source volume with
                flag: --maskmov %s
        mask_target: (an existing file name)
                image to mask target volume with
                flag: --maskdst %s
        max_iterations: (an integer)
                maximum # of times on each resolution
                flag: --maxit %d
        no_init: (a boolean)
                skip transform init
                flag: --noinit
        no_multi: (a boolean)
                work on highest resolution
                flag: --nomulti
        out_reg_file: (a file name)
                registration file to write
                flag: --lta %s
        outlier_limit: (a float)
                set maximal outlier limit in satit
                flag: --wlimit %.3f
        registered_file: (a boolean or a file name)
                registered image; either True or filename
                flag: --warp %s
        subjects_dir: (an existing directory name)
                subjects directory
        subsample_thresh: (an integer)
                subsample if dimension is above threshold size
                flag: --subsample %d
        trans_only: (a boolean)
                find 3 parameter translation only
                flag: --transonly
        weights_file: (a boolean or a file name)
                weights image to write; either True or filename
                flag: --weights %s
        write_vo2vox: (a boolean)
                output vox2vox matrix (default is RAS2RAS)
                flag: --vox2vox

Outputs::

        half_source: (a file name)
                source image mapped to halfway space
        half_source_xfm: (a file name)
                transform file to map source image to halfway space
        half_targ: (a file name)
                target image mapped to halfway space
        half_targ_xfm: (a file name)
                transform file to map target image to halfway space
        half_weights: (a file name)
                weights image mapped to halfway space
        out_reg_file: (an existing file name)
                output registration file
        registered_file: (a file name)
                output image with registration applied
        weights_file: (a file name)
                image of weights used

.. _nipype.interfaces.freesurfer.preprocess.Smooth:


.. index:: Smooth

Smooth
------

`Link to code <http://github.com/nipy/nipype/tree/e63e055194d62d2bdc4665688261c03a42fd0025/nipype/interfaces/freesurfer/preprocess.py#L1050>`__

Wraps command **mris_volsmooth**

Use FreeSurfer mris_volsmooth to smooth a volume

This function smoothes cortical regions on a surface and non-cortical
regions in volume.

.. note::
   Cortical voxels are mapped to the surface (3D->2D) and then the
   smoothed values from the surface are put back into the volume to fill
   the cortical ribbon. If data is smoothed with this algorithm, one has to
   be careful about how further processing is interpreted.

Examples
~~~~~~~~

>>> from nipype.interfaces.freesurfer import Smooth
>>> smoothvol = Smooth(in_file='functional.nii', smoothed_file = 'foo_out.nii', reg_file='register.dat', surface_fwhm=10, vol_fwhm=6)
>>> smoothvol.cmdline
'mris_volsmooth --i functional.nii --reg register.dat --o foo_out.nii --fwhm 10.000000 --vol-fwhm 6.000000'

Inputs::

        [Mandatory]
        in_file: (an existing file name)
                source volume
                flag: --i %s
        num_iters: (an integer >= 1)
                number of iterations instead of fwhm
                flag: --niters %d
                mutually_exclusive: surface_fwhm
        reg_file: (an existing file name)
                registers volume to surface anatomical
                flag: --reg %s
        surface_fwhm: (a floating point number >= 0.0)
                surface FWHM in mm
                flag: --fwhm %f
                mutually_exclusive: num_iters
                requires: reg_file
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
        proj_frac: (a float)
                project frac of thickness a long surface normal
                flag: --projfrac %s
                mutually_exclusive: proj_frac_avg
        proj_frac_avg: (a tuple of the form: (a float, a float, a float))
                average a long normal min max delta
                flag: --projfrac-avg %.2f %.2f %.2f
                mutually_exclusive: proj_frac
        smoothed_file: (a file name)
                output volume
                flag: --o %s
        subjects_dir: (an existing directory name)
                subjects directory
        vol_fwhm: (a floating point number >= 0.0)
                volume smoothing outside of surface
                flag: --vol-fwhm %f

Outputs::

        smoothed_file: (an existing file name)
                smoothed input volume

.. _nipype.interfaces.freesurfer.preprocess.SynthesizeFLASH:


.. index:: SynthesizeFLASH

SynthesizeFLASH
---------------

`Link to code <http://github.com/nipy/nipype/tree/e63e055194d62d2bdc4665688261c03a42fd0025/nipype/interfaces/freesurfer/preprocess.py#L1321>`__

Wraps command **mri_synthesize**

Synthesize a FLASH acquisition from T1 and proton density maps.

Examples
~~~~~~~~
>>> from nipype.interfaces.freesurfer import SynthesizeFLASH
>>> syn = SynthesizeFLASH(tr=20, te=3, flip_angle=30)
>>> syn.inputs.t1_image = 'T1.mgz'
>>> syn.inputs.pd_image = 'PD.mgz'
>>> syn.inputs.out_file = 'flash_30syn.mgz'
>>> syn.cmdline
'mri_synthesize 20.00 30.00 3.000 T1.mgz PD.mgz flash_30syn.mgz'

Inputs::

        [Mandatory]
        flip_angle: (a float)
                flip angle (in degrees)
                flag: %.2f, position: 3
        pd_image: (an existing file name)
                image of proton density values
                flag: %s, position: 6
        t1_image: (an existing file name)
                image of T1 values
                flag: %s, position: 5
        te: (a float)
                echo time (in msec)
                flag: %.3f, position: 4
        terminal_output: ('stream' or 'allatonce' or 'file' or 'none')
                Control terminal output: `stream` - displays to terminal
                immediately, `allatonce` - waits till command is finished to display
                output, `file` - writes output to file, `none` - output is ignored
        tr: (a float)
                repetition time (in msec)
                flag: %.2f, position: 2

        [Optional]
        args: (a string)
                Additional parameters to the command
                flag: %s
        environ: (a dictionary with keys which are a value of type 'str' and
                 with values which are a value of type 'str', nipype default value:
                 {})
                Environment variables
        fixed_weighting: (a boolean)
                use a fixed weighting to generate optimal gray/white contrast
                flag: -w, position: 1
        ignore_exception: (a boolean, nipype default value: False)
                Print an error message instead of throwing an exception in case the
                interface fails to run
        out_file: (a file name)
                image to write
                flag: %s
        subjects_dir: (an existing directory name)
                subjects directory

Outputs::

        out_file: (an existing file name)
                synthesized FLASH acquisition

.. _nipype.interfaces.freesurfer.preprocess.UnpackSDICOMDir:


.. index:: UnpackSDICOMDir

UnpackSDICOMDir
---------------

`Link to code <http://github.com/nipy/nipype/tree/e63e055194d62d2bdc4665688261c03a42fd0025/nipype/interfaces/freesurfer/preprocess.py#L109>`__

Wraps command **unpacksdcmdir**

Use unpacksdcmdir to convert dicom files

Call unpacksdcmdir -help from the command line to see more information on
using this command.

Examples
~~~~~~~~

>>> from nipype.interfaces.freesurfer import UnpackSDICOMDir
>>> unpack = UnpackSDICOMDir()
>>> unpack.inputs.source_dir = '.'
>>> unpack.inputs.output_dir = '.'
>>> unpack.inputs.run_info = (5, 'mprage', 'nii', 'struct')
>>> unpack.inputs.dir_structure = 'generic'
>>> unpack.cmdline
'unpacksdcmdir -generic -targ . -run 5 mprage nii struct -src .'

Inputs::

        [Mandatory]
        config: (an existing file name)
                specify unpacking rules in file
                flag: -cfg %s
                mutually_exclusive: run_info, config, seq_config
        run_info: (a tuple of the form: (an integer, a string, a string, a
                 string))
                runno subdir format name : spec unpacking rules on cmdline
                flag: -run %d %s %s %s
                mutually_exclusive: run_info, config, seq_config
        seq_config: (an existing file name)
                specify unpacking rules based on sequence
                flag: -seqcfg %s
                mutually_exclusive: run_info, config, seq_config
        source_dir: (an existing directory name)
                directory with the DICOM files
                flag: -src %s
        terminal_output: ('stream' or 'allatonce' or 'file' or 'none')
                Control terminal output: `stream` - displays to terminal
                immediately, `allatonce` - waits till command is finished to display
                output, `file` - writes output to file, `none` - output is ignored

        [Optional]
        args: (a string)
                Additional parameters to the command
                flag: %s
        dir_structure: ('fsfast' or 'generic')
                unpack to specified directory structures
                flag: -%s
        environ: (a dictionary with keys which are a value of type 'str' and
                 with values which are a value of type 'str', nipype default value:
                 {})
                Environment variables
        ignore_exception: (a boolean, nipype default value: False)
                Print an error message instead of throwing an exception in case the
                interface fails to run
        log_file: (an existing file name)
                explicilty set log file
                flag: -log %s
        no_info_dump: (a boolean)
                do not create infodump file
                flag: -noinfodump
        no_unpack_err: (a boolean)
                do not try to unpack runs with errors
                flag: -no-unpackerr
        output_dir: (a directory name)
                top directory into which the files will be unpacked
                flag: -targ %s
        scan_only: (an existing file name)
                only scan the directory and put result in file
                flag: -scanonly %s
        spm_zeropad: (an integer)
                set frame number zero padding width for SPM
                flag: -nspmzeropad %d
        subjects_dir: (an existing directory name)
                subjects directory

Outputs::

        None
