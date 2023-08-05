.. AUTO-GENERATED FILE -- DO NOT EDIT!

interfaces.freesurfer.model
===========================


.. _nipype.interfaces.freesurfer.model.Binarize:


.. index:: Binarize

Binarize
--------

`Link to code <http://github.com/nipy/nipype/tree/e63e055194d62d2bdc4665688261c03a42fd0025/nipype/interfaces/freesurfer/model.py#L403>`__

Wraps command **mri_binarize**

Use FreeSurfer mri_binarize to threshold an input volume

Examples
~~~~~~~~

>>> binvol = Binarize(in_file='structural.nii', min=10, binary_file='foo_out.nii')
>>> binvol.cmdline
'mri_binarize --o foo_out.nii --i structural.nii --min 10.000000'

Inputs::

        [Mandatory]
        in_file: (an existing file name)
                input volume
                flag: --i %s
        terminal_output: ('stream' or 'allatonce' or 'file' or 'none')
                Control terminal output: `stream` - displays to terminal
                immediately, `allatonce` - waits till command is finished to display
                output, `file` - writes output to file, `none` - output is ignored

        [Optional]
        abs: (a boolean)
                take abs of invol first (ie, make unsigned)
                flag: --abs
        args: (a string)
                Additional parameters to the command
                flag: %s
        bin_col_num: (a boolean)
                set binarized voxel value to its column number
                flag: --bincol
        bin_val: (an integer)
                set vox within thresh to val (default is 1)
                flag: --binval %d
        bin_val_not: (an integer)
                set vox outside range to val (default is 0)
                flag: --binvalnot %d
        binary_file: (a file name)
                binary output volume
                flag: --o %s
        count_file: (a boolean or a file name)
                save number of hits in ascii file (hits, ntotvox, pct)
                flag: --count %s
        dilate: (an integer)
                niters: dilate binarization in 3D
                flag: --dilate %d
        environ: (a dictionary with keys which are a value of type 'str' and
                 with values which are a value of type 'str', nipype default value:
                 {})
                Environment variables
        erode: (an integer)
                nerode: erode binarization in 3D (after any dilation)
                flag: --erode  %d
        erode2d: (an integer)
                nerode2d: erode binarization in 2D (after any 3D erosion)
                flag: --erode2d %d
        frame_no: (an integer)
                use 0-based frame of input (default is 0)
                flag: --frame %s
        ignore_exception: (a boolean, nipype default value: False)
                Print an error message instead of throwing an exception in case the
                interface fails to run
        invert: (a boolean)
                set binval=0, binvalnot=1
                flag: --inv
        mask_file: (an existing file name)
                must be within mask
                flag: --mask maskvol
        mask_thresh: (a float)
                set thresh for mask
                flag: --mask-thresh %f
        match: (a list of items which are an integer)
                match instead of threshold
                flag: --match %d...
        max: (a float)
                max thresh
                flag: --max %f
                mutually_exclusive: wm_ven_csf
        merge_file: (an existing file name)
                merge with mergevol
                flag: --merge %s
        min: (a float)
                min thresh
                flag: --min %f
                mutually_exclusive: wm_ven_csf
        out_type: ('nii' or 'nii.gz' or 'mgz')
                output file type
        rmax: (a float)
                compute max based on rmax*globalmean
                flag: --rmax %f
        rmin: (a float)
                compute min based on rmin*globalmean
                flag: --rmin %f
        subjects_dir: (an existing directory name)
                subjects directory
        ventricles: (a boolean)
                set match vals those for aseg ventricles+choroid (not 4th)
                flag: --ventricles
        wm: (a boolean)
                set match vals to 2 and 41 (aseg for cerebral WM)
                flag: --wm
        wm_ven_csf: (a boolean)
                WM and ventricular CSF, including choroid (not 4th)
                flag: --wm+vcsf
                mutually_exclusive: min, max
        zero_edges: (a boolean)
                zero the edge voxels
                flag: --zero-edges
        zero_slice_edge: (a boolean)
                zero the edge slice voxels
                flag: --zero-slice-edges

Outputs::

        binary_file: (an existing file name)
                binarized output volume
        count_file: (a file name)
                ascii file containing number of hits

.. _nipype.interfaces.freesurfer.model.Concatenate:


.. index:: Concatenate

Concatenate
-----------

`Link to code <http://github.com/nipy/nipype/tree/e63e055194d62d2bdc4665688261c03a42fd0025/nipype/interfaces/freesurfer/model.py#L506>`__

Wraps command **mri_concat**

Use Freesurfer mri_concat to combine several input volumes
into one output volume.  Can concatenate by frames, or compute
a variety of statistics on the input volumes.

Examples
~~~~~~~~

Combine two input volumes into one volume with two frames

>>> concat = Concatenate()
>>> concat.inputs.in_files = ['cont1.nii', 'cont2.nii']
>>> concat.inputs.concatenated_file = 'bar.nii'
>>> concat.cmdline
'mri_concat --o bar.nii --i cont1.nii --i cont2.nii'

Inputs::

        [Mandatory]
        in_files: (an existing file name)
                Individual volumes to be concatenated
                flag: --i %s...
        terminal_output: ('stream' or 'allatonce' or 'file' or 'none')
                Control terminal output: `stream` - displays to terminal
                immediately, `allatonce` - waits till command is finished to display
                output, `file` - writes output to file, `none` - output is ignored

        [Optional]
        add_val: (a float)
                Add some amount to the input volume
                flag: --add %f
        args: (a string)
                Additional parameters to the command
                flag: %s
        combine: (a boolean)
                Combine non-zero values into single frame volume
                flag: --combine
        concatenated_file: (a file name)
                Output volume
                flag: --o %s
        environ: (a dictionary with keys which are a value of type 'str' and
                 with values which are a value of type 'str', nipype default value:
                 {})
                Environment variables
        gmean: (an integer)
                create matrix to average Ng groups, Nper=Ntot/Ng
                flag: --gmean %d
        ignore_exception: (a boolean, nipype default value: False)
                Print an error message instead of throwing an exception in case the
                interface fails to run
        keep_dtype: (a boolean)
                Keep voxelwise precision type (default is float
                flag: --keep-datatype
        mask_file: (an existing file name)
                Mask input with a volume
                flag: --mask %s
        max_bonfcor: (a boolean)
                Compute max and bonferroni correct (assumes -log10(ps))
                flag: --max-bonfcor
        max_index: (a boolean)
                Compute the index of max voxel in concatenated volumes
                flag: --max-index
        mean_div_n: (a boolean)
                compute mean/nframes (good for var)
                flag: --mean-div-n
        multiply_by: (a float)
                Multiply input volume by some amount
                flag: --mul %f
        multiply_matrix_file: (an existing file name)
                Multiply input by an ascii matrix in file
                flag: --mtx %s
        paired_stats: ('sum' or 'avg' or 'diff' or 'diff-norm' or 'diff-
                 norm1' or 'diff-norm2')
                Compute paired sum, avg, or diff
                flag: --paired-%s
        sign: ('abs' or 'pos' or 'neg')
                Take only pos or neg voxles from input, or take abs
                flag: --%s
        sort: (a boolean)
                Sort each voxel by ascending frame value
                flag: --sort
        stats: ('sum' or 'var' or 'std' or 'max' or 'min' or 'mean')
                Compute the sum, var, std, max, min or mean of the input volumes
                flag: --%s
        subjects_dir: (an existing directory name)
                subjects directory
        vote: (a boolean)
                Most frequent value at each voxel and fraction of occurances
                flag: --vote

Outputs::

        concatenated_file: (an existing file name)
                Path/name of the output volume

.. _nipype.interfaces.freesurfer.model.GLMFit:


.. index:: GLMFit

GLMFit
------

`Link to code <http://github.com/nipy/nipype/tree/e63e055194d62d2bdc4665688261c03a42fd0025/nipype/interfaces/freesurfer/model.py#L256>`__

Wraps command **mri_glmfit**

Use FreeSurfer's mri_glmfit to specify and estimate a general linear model.

Examples
~~~~~~~~

>>> glmfit = GLMFit()
>>> glmfit.inputs.in_file = 'functional.nii'
>>> glmfit.inputs.one_sample = True
>>> glmfit.cmdline == 'mri_glmfit --glmdir %s --y functional.nii --osgm'%os.getcwd()
True

Inputs::

        [Mandatory]
        in_file: (a file name)
                input 4D file
                flag: --y %s
        terminal_output: ('stream' or 'allatonce' or 'file' or 'none')
                Control terminal output: `stream` - displays to terminal
                immediately, `allatonce` - waits till command is finished to display
                output, `file` - writes output to file, `none` - output is ignored

        [Optional]
        allow_ill_cond: (a boolean)
                allow ill-conditioned design matrices
                flag: --illcond
        allow_repeated_subjects: (a boolean)
                allow subject names to repeat in the fsgd file (must appear before
                --fsgd
                flag: --allowsubjrep
        args: (a string)
                Additional parameters to the command
                flag: %s
        calc_AR1: (a boolean)
                compute and save temporal AR1 of residual
                flag: --tar1
        check_opts: (a boolean)
                don't run anything, just check options and exit
                flag: --checkopts
        compute_log_y: (a boolean)
                compute natural log of y prior to analysis
                flag: --logy
        contrast: (an existing file name)
                contrast file
                flag: --C %s...
        cortex: (a boolean)
                use subjects ?h.cortex.label as label
                flag: --cortex
                mutually_exclusive: label_file
        debug: (a boolean)
                turn on debugging
                flag: --debug
        design: (an existing file name)
                design matrix file
                flag: --X %s
                mutually_exclusive: fsgd, design, one_sample
        diag: (an integer)
                Gdiag_no : set diagnositc level
        diag_cluster: (a boolean)
                save sig volume and exit from first sim loop
                flag: --diag-cluster
        environ: (a dictionary with keys which are a value of type 'str' and
                 with values which are a value of type 'str', nipype default value:
                 {})
                Environment variables
        fixed_fx_dof: (an integer)
                dof for fixed effects analysis
                flag: --ffxdof %d
                mutually_exclusive: fixed_fx_dof_file
        fixed_fx_dof_file: (a file name)
                text file with dof for fixed effects analysis
                flag: --ffxdofdat %d
                mutually_exclusive: fixed_fx_dof
        fixed_fx_var: (an existing file name)
                for fixed effects analysis
                flag: --yffxvar %s
        force_perm: (a boolean)
                force perumtation test, even when design matrix is not orthog
                flag: --perm-force
        fsgd: (a tuple of the form: (an existing file name, 'doss' or
                 'dods'))
                freesurfer descriptor file
                flag: --fsgd %s %s
                mutually_exclusive: fsgd, design, one_sample
        fwhm: (a floating point number >= 0.0)
                smooth input by fwhm
                flag: --fwhm %f
        glm_dir: (a string)
                save outputs to dir
                flag: --glmdir %s
        hemi: ('lh' or 'rh')
                surface hemisphere
        ignore_exception: (a boolean, nipype default value: False)
                Print an error message instead of throwing an exception in case the
                interface fails to run
        invert_mask: (a boolean)
                invert mask
                flag: --mask-inv
        label_file: (an existing file name)
                use label as mask, surfaces only
                flag: --label %s
                mutually_exclusive: cortex
        mask_file: (an existing file name)
                binary mask
                flag: --mask %s
        no_contrast_sok: (a boolean)
                do not fail if no contrasts specified
                flag: --no-contrasts-ok
        no_est_fwhm: (a boolean)
                turn off FWHM output estimation
                flag: --no-est-fwhm
        no_mask_smooth: (a boolean)
                do not mask when smoothing
                flag: --no-mask-smooth
        no_prune: (a boolean)
                do not prune
                flag: --no-prune
                mutually_exclusive: prunethresh
        one_sample: (a boolean)
                construct X and C as a one-sample group mean
                flag: --osgm
                mutually_exclusive: one_sample, fsgd, design, contrast
        pca: (a boolean)
                perform pca/svd analysis on residual
                flag: --pca
        per_voxel_reg: (an existing file name)
                per-voxel regressors
                flag: --pvr %s...
        profile: (an integer)
                niters : test speed
                flag: --profile %d
        prune: (a boolean)
                remove voxels that do not have a non-zero value at each frame (def)
                flag: --prune
        prune_thresh: (a float)
                prune threshold. Default is FLT_MIN
                flag: --prune_thr %f
                mutually_exclusive: noprune
        resynth_test: (an integer)
                test GLM by resynthsis
                flag: --resynthtest %d
        save_cond: (a boolean)
                flag to save design matrix condition at each voxel
                flag: --save-cond
        save_estimate: (a boolean)
                save signal estimate (yhat)
                flag: --yhat-save
        save_res_corr_mtx: (a boolean)
                save residual error spatial correlation matrix (eres.scm). Big!
                flag: --eres-scm
        save_residual: (a boolean)
                save residual error (eres)
                flag: --eres-save
        seed: (an integer)
                used for synthesizing noise
                flag: --seed %d
        self_reg: (a tuple of the form: (an integer, an integer, an integer))
                self-regressor from index col row slice
                flag: --selfreg %d %d %d
        sim_done_file: (a file name)
                create file when simulation finished
                flag: --sim-done %s
        sim_sign: ('abs' or 'pos' or 'neg')
                abs, pos, or neg
                flag: --sim-sign %s
        simulation: (a tuple of the form: ('perm' or 'mc-full' or 'mc-z', an
                 integer, a float, a string))
                nulltype nsim thresh csdbasename
                flag: --sim %s %d %f %s
        subject_id: (a string)
                subject id for surface geometry
        subjects_dir: (an existing directory name)
                subjects directory
        surf: (a boolean)
                analysis is on a surface mesh
                flag: --surf %s %s %s
                requires: subject_id, hemi
        surf_geo: (a string, nipype default value: white)
                surface geometry name (e.g. white, pial)
        synth: (a boolean)
                replace input with gaussian
                flag: --synth
        uniform: (a tuple of the form: (a float, a float))
                use uniform distribution instead of gaussian
                flag: --uniform %f %f
        var_fwhm: (a floating point number >= 0.0)
                smooth variance by fwhm
                flag: --var-fwhm %f
        vox_dump: (a tuple of the form: (an integer, an integer, an integer))
                dump voxel GLM and exit
                flag: --voxdump %d %d %d
        weight_file: (an existing file name)
                weight for each input at each voxel
                mutually_exclusive: weighted_ls
        weight_inv: (a boolean)
                invert weights
                flag: --w-inv
                mutually_exclusive: weighted_ls
        weight_sqrt: (a boolean)
                sqrt of weights
                flag: --w-sqrt
                mutually_exclusive: weighted_ls
        weighted_ls: (an existing file name)
                weighted least squares
                flag: --wls %s
                mutually_exclusive: weight_file, weight_inv, weight_sqrt

Outputs::

        beta_file: (an existing file name)
                map of regression coefficients
        dof_file: (a file name)
                text file with effective degrees-of-freedom for the analysis
        error_file: (a file name)
                map of residual error
        error_stddev_file: (a file name)
                map of residual error standard deviation
        error_var_file: (a file name)
                map of residual error variance
        estimate_file: (a file name)
                map of the estimated Y values
        frame_eigenvectors: (a file name)
                matrix of frame eigenvectors from residual PCA
        ftest_file
                map of test statistic values
        fwhm_file: (a file name)
                text file with estimated smoothness
        gamma_file
                map of contrast of regression coefficients
        gamma_var_file
                map of regression contrast variance
        glm_dir: (an existing directory name)
                output directory
        mask_file: (a file name)
                map of the mask used in the analysis
        sig_file
                map of F-test significance (in -log10p)
        singular_values: (a file name)
                matrix singular values from residual PCA
        spatial_eigenvectors: (a file name)
                map of spatial eigenvectors from residual PCA
        svd_stats_file: (a file name)
                text file summarizing the residual PCA

.. _nipype.interfaces.freesurfer.model.Label2Vol:


.. index:: Label2Vol

Label2Vol
---------

`Link to code <http://github.com/nipy/nipype/tree/e63e055194d62d2bdc4665688261c03a42fd0025/nipype/interfaces/freesurfer/model.py#L738>`__

Wraps command **mri_label2vol**

Make a binary volume from a Freesurfer label

Examples
~~~~~~~~

>>> binvol = Label2Vol(label_file='cortex.label', template_file='structural.nii', reg_file='register.dat', fill_thresh=0.5, vol_label_file='foo_out.nii')
>>> binvol.cmdline
'mri_label2vol --fillthresh 0 --label cortex.label --reg register.dat --temp structural.nii --o foo_out.nii'

Inputs::

        [Mandatory]
        annot_file: (an existing file name)
                surface annotation file
                flag: --annot %s
                mutually_exclusive: label_file, annot_file, seg_file, aparc_aseg
                requires: subject_id, hemi
        aparc_aseg: (a boolean)
                use aparc+aseg.mgz in subjectdir as seg
                flag: --aparc+aseg
                mutually_exclusive: label_file, annot_file, seg_file, aparc_aseg
        label_file: (an existing file name)
                list of label files
                flag: --label %s...
                mutually_exclusive: label_file, annot_file, seg_file, aparc_aseg
        seg_file: (an existing file name)
                segmentation file
                flag: --seg %s
                mutually_exclusive: label_file, annot_file, seg_file, aparc_aseg
        template_file: (an existing file name)
                output template volume
                flag: --temp %s
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
        fill_thresh: (0.0 <= a floating point number <= 1.0)
                thresh : between 0 and 1
                flag: --fillthresh %.f
        hemi: ('lh' or 'rh')
                hemisphere to use lh or rh
                flag: --hemi %s
        identity: (a boolean)
                set R=I
                flag: --identity
                mutually_exclusive: reg_file, reg_header, identity
        ignore_exception: (a boolean, nipype default value: False)
                Print an error message instead of throwing an exception in case the
                interface fails to run
        invert_mtx: (a boolean)
                Invert the registration matrix
                flag: --invertmtx
        label_hit_file: (a file name)
                file with each frame is nhits for a label
                flag: --hits %s
        label_voxel_volume: (a float)
                volume of each label point (def 1mm3)
                flag: --labvoxvol %f
        map_label_stat: (a file name)
                map the label stats field into the vol
                flag: --label-stat %s
        native_vox2ras: (a boolean)
                use native vox2ras xform instead of tkregister-style
                flag: --native-vox2ras
        proj: (a tuple of the form: ('abs' or 'frac', a float, a float, a
                 float))
                project along surface normal
                flag: --proj %s %f %f %f
                requires: subject_id, hemi
        reg_file: (an existing file name)
                tkregister style matrix VolXYZ = R*LabelXYZ
                flag: --reg %s
                mutually_exclusive: reg_file, reg_header, identity
        reg_header: (an existing file name)
                label template volume
                flag: --regheader %s
                mutually_exclusive: reg_file, reg_header, identity
        subject_id: (a string)
                subject id
                flag: --subject %s
        subjects_dir: (an existing directory name)
                subjects directory
        surface: (a string)
                use surface instead of white
                flag: --surf %s
        vol_label_file: (a file name)
                output volume
                flag: --o %s

Outputs::

        vol_label_file: (an existing file name)
                output volume

.. _nipype.interfaces.freesurfer.model.MRISPreproc:


.. index:: MRISPreproc

MRISPreproc
-----------

`Link to code <http://github.com/nipy/nipype/tree/e63e055194d62d2bdc4665688261c03a42fd0025/nipype/interfaces/freesurfer/model.py#L78>`__

Wraps command **mris_preproc**

Use FreeSurfer mris_preproc to prepare a group of contrasts for
a second level analysis

Examples
~~~~~~~~

>>> preproc = MRISPreproc()
>>> preproc.inputs.target = 'fsaverage'
>>> preproc.inputs.hemi = 'lh'
>>> preproc.inputs.vol_measure_file = [('cont1.nii', 'register.dat'),                                            ('cont1a.nii', 'register.dat')]
>>> preproc.inputs.out_file = 'concatenated_file.mgz'
>>> preproc.cmdline
'mris_preproc --hemi lh --out concatenated_file.mgz --target fsaverage --iv cont1.nii register.dat --iv cont1a.nii register.dat'

Inputs::

        [Mandatory]
        hemi: ('lh' or 'rh')
                hemisphere for source and target
                flag: --hemi %s
        target: (a string)
                target subject name
                flag: --target %s
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
        fsgd_file: (an existing file name)
                specify subjects using fsgd file
                flag: --fsgd %s
                mutually_exclusive: subjects, fsgd_file, subject_file
        fwhm: (a float)
                smooth by fwhm mm on the target surface
                flag: --fwhm %f
                mutually_exclusive: num_iters
        fwhm_source: (a float)
                smooth by fwhm mm on the source surface
                flag: --fwhm-src %f
                mutually_exclusive: num_iters_source
        ignore_exception: (a boolean, nipype default value: False)
                Print an error message instead of throwing an exception in case the
                interface fails to run
        num_iters: (an integer)
                niters : smooth by niters on the target surface
                flag: --niters %d
                mutually_exclusive: fwhm
        num_iters_source: (an integer)
                niters : smooth by niters on the source surface
                flag: --niterssrc %d
                mutually_exclusive: fwhm_source
        out_file: (a file name)
                output filename
                flag: --out %s
        proj_frac: (a float)
                projection fraction for vol2surf
                flag: --projfrac %s
        smooth_cortex_only: (a boolean)
                only smooth cortex (ie, exclude medial wall)
                flag: --smooth-cortex-only
        source_format: (a string)
                source format
                flag: --srcfmt %s
        subject_file: (an existing file name)
                file specifying subjects separated by white space
                flag: --f %s
                mutually_exclusive: subjects, fsgd_file, subject_file
        subjects: (a list of items which are any value)
                subjects from who measures are calculated
                flag: --s %s...
                mutually_exclusive: subjects, fsgd_file, subject_file
        subjects_dir: (an existing directory name)
                subjects directory
        surf_area: (a string)
                Extract vertex area from subject/surf/hemi.surfname to use as input.
                flag: --area %s
                mutually_exclusive: surf_measure, surf_measure_file, surf_area
        surf_dir: (a string)
                alternative directory (instead of surf)
                flag: --surfdir %s
        surf_measure: (a string)
                Use subject/surf/hemi.surf_measure as input
                flag: --meas %s
                mutually_exclusive: surf_measure, surf_measure_file, surf_area
        surf_measure_file: (an existing file name)
                file alternative to surfmeas, still requires list of subjects
                flag: --is %s...
                mutually_exclusive: surf_measure, surf_measure_file, surf_area
        vol_measure_file: (a tuple of the form: (an existing file name, an
                 existing file name))
                list of volume measure and reg file tuples
                flag: --iv %s %s...

Outputs::

        out_file: (an existing file name)
                preprocessed output file

.. _nipype.interfaces.freesurfer.model.MS_LDA:


.. index:: MS_LDA

MS_LDA
------

`Link to code <http://github.com/nipy/nipype/tree/e63e055194d62d2bdc4665688261c03a42fd0025/nipype/interfaces/freesurfer/model.py#L810>`__

Wraps command **mri_ms_LDA**

Perform LDA reduction on the intensity space of an arbitrary # of FLASH images

Examples
~~~~~~~~

>>> grey_label = 2
>>> white_label = 3
>>> zero_value = 1
>>> optimalWeights = MS_LDA(lda_labels=[grey_label, white_label],                                 label_file='label.mgz', weight_file='weights.txt',                                 shift=zero_value, vol_synth_file='synth_out.mgz',                                 conform=True, use_weights=True,                                 images=['FLASH1.mgz', 'FLASH2.mgz', 'FLASH3.mgz'])
>>> optimalWeights.cmdline
'mri_ms_LDA -conform -label label.mgz -lda 2 3 -shift 1 -W -synth synth_out.mgz -weight weights.txt FLASH1.mgz FLASH2.mgz FLASH3.mgz'

Inputs::

        [Mandatory]
        images: (an existing file name)
                list of input FLASH images
                flag: %s, position: -1
        lda_labels: (a list of from 2 to 2 items which are an integer)
                pair of class labels to optimize
                flag: -lda %s
        terminal_output: ('stream' or 'allatonce' or 'file' or 'none')
                Control terminal output: `stream` - displays to terminal
                immediately, `allatonce` - waits till command is finished to display
                output, `file` - writes output to file, `none` - output is ignored
        vol_synth_file: (a file name)
                filename for the synthesized output volume
                flag: -synth %s
        weight_file: (a file name)
                filename for the LDA weights (input or output)
                flag: -weight %s

        [Optional]
        args: (a string)
                Additional parameters to the command
                flag: %s
        conform: (a boolean)
                Conform the input volumes (brain mask typically already conformed)
                flag: -conform
        environ: (a dictionary with keys which are a value of type 'str' and
                 with values which are a value of type 'str', nipype default value:
                 {})
                Environment variables
        ignore_exception: (a boolean, nipype default value: False)
                Print an error message instead of throwing an exception in case the
                interface fails to run
        label_file: (a file name)
                filename of the label volume
                flag: -label %s
        mask_file: (a file name)
                filename of the brain mask volume
                flag: -mask %s
        shift: (an integer)
                shift all values equal to the given value to zero
                flag: -shift %d
        subjects_dir: (an existing directory name)
                subjects directory
        use_weights: (a boolean)
                Use the weights from a previously generated weight file
                flag: -W

Outputs::

        vol_synth_file: (an existing file name)
        weight_file: (an existing file name)

.. _nipype.interfaces.freesurfer.model.OneSampleTTest:


.. index:: OneSampleTTest

OneSampleTTest
--------------

`Link to code <http://github.com/nipy/nipype/tree/e63e055194d62d2bdc4665688261c03a42fd0025/nipype/interfaces/freesurfer/model.py#L335>`__

Wraps command **mri_glmfit**


Inputs::

        [Mandatory]
        in_file: (a file name)
                input 4D file
                flag: --y %s
        terminal_output: ('stream' or 'allatonce' or 'file' or 'none')
                Control terminal output: `stream` - displays to terminal
                immediately, `allatonce` - waits till command is finished to display
                output, `file` - writes output to file, `none` - output is ignored

        [Optional]
        allow_ill_cond: (a boolean)
                allow ill-conditioned design matrices
                flag: --illcond
        allow_repeated_subjects: (a boolean)
                allow subject names to repeat in the fsgd file (must appear before
                --fsgd
                flag: --allowsubjrep
        args: (a string)
                Additional parameters to the command
                flag: %s
        calc_AR1: (a boolean)
                compute and save temporal AR1 of residual
                flag: --tar1
        check_opts: (a boolean)
                don't run anything, just check options and exit
                flag: --checkopts
        compute_log_y: (a boolean)
                compute natural log of y prior to analysis
                flag: --logy
        contrast: (an existing file name)
                contrast file
                flag: --C %s...
        cortex: (a boolean)
                use subjects ?h.cortex.label as label
                flag: --cortex
                mutually_exclusive: label_file
        debug: (a boolean)
                turn on debugging
                flag: --debug
        design: (an existing file name)
                design matrix file
                flag: --X %s
                mutually_exclusive: fsgd, design, one_sample
        diag: (an integer)
                Gdiag_no : set diagnositc level
        diag_cluster: (a boolean)
                save sig volume and exit from first sim loop
                flag: --diag-cluster
        environ: (a dictionary with keys which are a value of type 'str' and
                 with values which are a value of type 'str', nipype default value:
                 {})
                Environment variables
        fixed_fx_dof: (an integer)
                dof for fixed effects analysis
                flag: --ffxdof %d
                mutually_exclusive: fixed_fx_dof_file
        fixed_fx_dof_file: (a file name)
                text file with dof for fixed effects analysis
                flag: --ffxdofdat %d
                mutually_exclusive: fixed_fx_dof
        fixed_fx_var: (an existing file name)
                for fixed effects analysis
                flag: --yffxvar %s
        force_perm: (a boolean)
                force perumtation test, even when design matrix is not orthog
                flag: --perm-force
        fsgd: (a tuple of the form: (an existing file name, 'doss' or
                 'dods'))
                freesurfer descriptor file
                flag: --fsgd %s %s
                mutually_exclusive: fsgd, design, one_sample
        fwhm: (a floating point number >= 0.0)
                smooth input by fwhm
                flag: --fwhm %f
        glm_dir: (a string)
                save outputs to dir
                flag: --glmdir %s
        hemi: ('lh' or 'rh')
                surface hemisphere
        ignore_exception: (a boolean, nipype default value: False)
                Print an error message instead of throwing an exception in case the
                interface fails to run
        invert_mask: (a boolean)
                invert mask
                flag: --mask-inv
        label_file: (an existing file name)
                use label as mask, surfaces only
                flag: --label %s
                mutually_exclusive: cortex
        mask_file: (an existing file name)
                binary mask
                flag: --mask %s
        no_contrast_sok: (a boolean)
                do not fail if no contrasts specified
                flag: --no-contrasts-ok
        no_est_fwhm: (a boolean)
                turn off FWHM output estimation
                flag: --no-est-fwhm
        no_mask_smooth: (a boolean)
                do not mask when smoothing
                flag: --no-mask-smooth
        no_prune: (a boolean)
                do not prune
                flag: --no-prune
                mutually_exclusive: prunethresh
        one_sample: (a boolean)
                construct X and C as a one-sample group mean
                flag: --osgm
                mutually_exclusive: one_sample, fsgd, design, contrast
        pca: (a boolean)
                perform pca/svd analysis on residual
                flag: --pca
        per_voxel_reg: (an existing file name)
                per-voxel regressors
                flag: --pvr %s...
        profile: (an integer)
                niters : test speed
                flag: --profile %d
        prune: (a boolean)
                remove voxels that do not have a non-zero value at each frame (def)
                flag: --prune
        prune_thresh: (a float)
                prune threshold. Default is FLT_MIN
                flag: --prune_thr %f
                mutually_exclusive: noprune
        resynth_test: (an integer)
                test GLM by resynthsis
                flag: --resynthtest %d
        save_cond: (a boolean)
                flag to save design matrix condition at each voxel
                flag: --save-cond
        save_estimate: (a boolean)
                save signal estimate (yhat)
                flag: --yhat-save
        save_res_corr_mtx: (a boolean)
                save residual error spatial correlation matrix (eres.scm). Big!
                flag: --eres-scm
        save_residual: (a boolean)
                save residual error (eres)
                flag: --eres-save
        seed: (an integer)
                used for synthesizing noise
                flag: --seed %d
        self_reg: (a tuple of the form: (an integer, an integer, an integer))
                self-regressor from index col row slice
                flag: --selfreg %d %d %d
        sim_done_file: (a file name)
                create file when simulation finished
                flag: --sim-done %s
        sim_sign: ('abs' or 'pos' or 'neg')
                abs, pos, or neg
                flag: --sim-sign %s
        simulation: (a tuple of the form: ('perm' or 'mc-full' or 'mc-z', an
                 integer, a float, a string))
                nulltype nsim thresh csdbasename
                flag: --sim %s %d %f %s
        subject_id: (a string)
                subject id for surface geometry
        subjects_dir: (an existing directory name)
                subjects directory
        surf: (a boolean)
                analysis is on a surface mesh
                flag: --surf %s %s %s
                requires: subject_id, hemi
        surf_geo: (a string, nipype default value: white)
                surface geometry name (e.g. white, pial)
        synth: (a boolean)
                replace input with gaussian
                flag: --synth
        uniform: (a tuple of the form: (a float, a float))
                use uniform distribution instead of gaussian
                flag: --uniform %f %f
        var_fwhm: (a floating point number >= 0.0)
                smooth variance by fwhm
                flag: --var-fwhm %f
        vox_dump: (a tuple of the form: (an integer, an integer, an integer))
                dump voxel GLM and exit
                flag: --voxdump %d %d %d
        weight_file: (an existing file name)
                weight for each input at each voxel
                mutually_exclusive: weighted_ls
        weight_inv: (a boolean)
                invert weights
                flag: --w-inv
                mutually_exclusive: weighted_ls
        weight_sqrt: (a boolean)
                sqrt of weights
                flag: --w-sqrt
                mutually_exclusive: weighted_ls
        weighted_ls: (an existing file name)
                weighted least squares
                flag: --wls %s
                mutually_exclusive: weight_file, weight_inv, weight_sqrt

Outputs::

        beta_file: (an existing file name)
                map of regression coefficients
        dof_file: (a file name)
                text file with effective degrees-of-freedom for the analysis
        error_file: (a file name)
                map of residual error
        error_stddev_file: (a file name)
                map of residual error standard deviation
        error_var_file: (a file name)
                map of residual error variance
        estimate_file: (a file name)
                map of the estimated Y values
        frame_eigenvectors: (a file name)
                matrix of frame eigenvectors from residual PCA
        ftest_file
                map of test statistic values
        fwhm_file: (a file name)
                text file with estimated smoothness
        gamma_file
                map of contrast of regression coefficients
        gamma_var_file
                map of regression contrast variance
        glm_dir: (an existing directory name)
                output directory
        mask_file: (a file name)
                map of the mask used in the analysis
        sig_file
                map of F-test significance (in -log10p)
        singular_values: (a file name)
                matrix singular values from residual PCA
        spatial_eigenvectors: (a file name)
                map of spatial eigenvectors from residual PCA
        svd_stats_file: (a file name)
                text file summarizing the residual PCA

.. _nipype.interfaces.freesurfer.model.SegStats:


.. index:: SegStats

SegStats
--------

`Link to code <http://github.com/nipy/nipype/tree/e63e055194d62d2bdc4665688261c03a42fd0025/nipype/interfaces/freesurfer/model.py#L614>`__

Wraps command **mri_segstats**

Use FreeSurfer mri_segstats for ROI analysis

Examples
~~~~~~~~

>>> import nipype.interfaces.freesurfer as fs
>>> ss = fs.SegStats()
>>> ss.inputs.annot = ('PWS04', 'lh', 'aparc')
>>> ss.inputs.in_file = 'functional.nii'
>>> ss.inputs.subjects_dir = '.'
>>> ss.inputs.avgwf_txt_file = './avgwf.txt'
>>> ss.inputs.summary_file = './summary.stats'
>>> ss.cmdline
'mri_segstats --annot PWS04 lh aparc --avgwf ./avgwf.txt --i functional.nii --sum ./summary.stats'

Inputs::

        [Mandatory]
        annot: (a tuple of the form: (a string, 'lh' or 'rh', a string))
                subject hemi parc : use surface parcellation
                flag: --annot %s %s %s
                mutually_exclusive: segmentation_file, annot, surf_label
        segmentation_file: (an existing file name)
                segmentation volume path
                flag: --seg %s
                mutually_exclusive: segmentation_file, annot, surf_label
        surf_label: (a tuple of the form: (a string, 'lh' or 'rh', a string))
                subject hemi label : use surface label
                flag: --slabel %s %s %s
                mutually_exclusive: segmentation_file, annot, surf_label
        terminal_output: ('stream' or 'allatonce' or 'file' or 'none')
                Control terminal output: `stream` - displays to terminal
                immediately, `allatonce` - waits till command is finished to display
                output, `file` - writes output to file, `none` - output is ignored

        [Optional]
        args: (a string)
                Additional parameters to the command
                flag: %s
        avgwf_file: (a boolean or a file name)
                Save as binary volume (bool or filename)
                flag: --avgwfvol %s
        avgwf_txt_file: (a boolean or a file name)
                Save average waveform into file (bool or filename)
                flag: --avgwf %s
        brain_vol: ('brain-vol-from-seg' or 'brainmask' or '--%s')
                Compute brain volume either with ``brainmask`` or ``brain-vol-from-
                seg``
        calc_power: ('sqr' or 'sqrt')
                Compute either the sqr or the sqrt of the input
                flag: --%s
        calc_snr: (a boolean)
                save mean/std as extra column in output table
                flag: --snr
        color_table_file: (an existing file name)
                color table file with seg id names
                flag: --ctab %s
                mutually_exclusive: color_table_file, default_color_table,
                 gca_color_table
        cortex_vol_from_surf: (a boolean)
                Compute cortex volume from surf
                flag: --surf-ctx-vol
        default_color_table: (a boolean)
                use $FREESURFER_HOME/FreeSurferColorLUT.txt
                flag: --ctab-default
                mutually_exclusive: color_table_file, default_color_table,
                 gca_color_table
        environ: (a dictionary with keys which are a value of type 'str' and
                 with values which are a value of type 'str', nipype default value:
                 {})
                Environment variables
        etiv: (a boolean)
                Compute ICV from talairach transform
                flag: --etiv
        etiv_only: ('etiv' or 'old-etiv' or '--%s-only')
                Compute etiv and exit. Use ``etiv`` or ``old-etiv``
        exclude_ctx_gm_wm: (a boolean)
                exclude cortical gray and white matter
                flag: --excl-ctxgmwm
        exclude_id: (an integer)
                Exclude seg id from report
                flag: --excludeid %d
        frame: (an integer)
                Report stats on nth frame of input volume
                flag: --frame %d
        gca_color_table: (an existing file name)
                get color table from GCA (CMA)
                flag: --ctab-gca %s
                mutually_exclusive: color_table_file, default_color_table,
                 gca_color_table
        ignore_exception: (a boolean, nipype default value: False)
                Print an error message instead of throwing an exception in case the
                interface fails to run
        in_file: (an existing file name)
                Use the segmentation to report stats on this volume
                flag: --i %s
        mask_erode: (an integer)
                Erode mask by some amount
                flag: --maskerode %d
        mask_file: (an existing file name)
                Mask volume (same size as seg
                flag: --mask %s
        mask_frame: (an integer)
                Mask with this (0 based) frame of the mask volume
                requires: mask_file
        mask_invert: (a boolean)
                Invert binarized mask volume
                flag: --maskinvert
        mask_sign: ('abs' or 'pos' or 'neg' or '--masksign %s')
                Sign for mask threshold: pos, neg, or abs
        mask_thresh: (a float)
                binarize mask with this threshold <0.5>
                flag: --maskthresh %f
        multiply: (a float)
                multiply input by val
                flag: --mul %f
        non_empty_only: (a boolean)
                Only report nonempty segmentations
                flag: --nonempty
        partial_volume_file: (an existing file name)
                Compensate for partial voluming
                flag: --pv %f
        segment_id: (a list of items which are any value)
                Manually specify segmentation ids
                flag: --id %s...
        sf_avg_file: (a boolean or a file name)
                Save mean across space and time
                flag: --sfavg %s
        subjects_dir: (an existing directory name)
                subjects directory
        summary_file: (a file name)
                Segmentation stats summary table file
                flag: --sum %s
        vox: (a list of items which are an integer)
                Replace seg with all 0s except at C R S (three int inputs)
                flag: --vox %s
        wm_vol_from_surf: (a boolean)
                Compute wm volume from surf
                flag: --surf-wm-vol

Outputs::

        avgwf_file: (a file name)
                Volume with functional statistics averaged over segs
        avgwf_txt_file: (a file name)
                Text file with functional statistics averaged over segs
        sf_avg_file: (a file name)
                Text file with func statistics averaged over segs and framss
        summary_file: (an existing file name)
                Segmentation summary statistics table
