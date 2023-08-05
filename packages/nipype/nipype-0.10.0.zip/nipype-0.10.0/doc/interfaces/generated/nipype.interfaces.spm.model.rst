.. AUTO-GENERATED FILE -- DO NOT EDIT!

interfaces.spm.model
====================


.. _nipype.interfaces.spm.model.EstimateContrast:


.. index:: EstimateContrast

EstimateContrast
----------------

`Link to code <http://github.com/nipy/nipype/tree/e63e055194d62d2bdc4665688261c03a42fd0025/nipype/interfaces/spm/model.py#L301>`__

use spm_contrasts to estimate contrasts of interest

Examples
~~~~~~~~
>>> import nipype.interfaces.spm as spm
>>> est = spm.EstimateContrast()
>>> est.inputs.spm_mat_file = 'SPM.mat'
>>> cont1 = ('Task>Baseline','T', ['Task-Odd','Task-Even'],[0.5,0.5])
>>> cont2 = ('Task-Odd>Task-Even','T', ['Task-Odd','Task-Even'],[1,-1])
>>> contrasts = [cont1,cont2]
>>> est.inputs.contrasts = contrasts
>>> est.run() # doctest: +SKIP

Inputs::

        [Mandatory]
        beta_images: (an existing file name)
                Parameter estimates of the design matrix
        contrasts: (a list of items which are a tuple of the form: (a string,
                 'T', a list of items which are a string, a list of items which are
                 a float) or a tuple of the form: (a string, 'T', a list of items
                 which are a string, a list of items which are a float, a list of
                 items which are a float) or a tuple of the form: (a string, 'F', a
                 list of items which are a tuple of the form: (a string, 'T', a list
                 of items which are a string, a list of items which are a float) or
                 a tuple of the form: (a string, 'T', a list of items which are a
                 string, a list of items which are a float, a list of items which
                 are a float)))
                List of contrasts with each contrast being a list of the form:
                 [('name', 'stat', [condition list], [weight list], [session
                list])]. if
                 session list is None or not provided, all sessions are used. For F
                 contrasts, the condition list should contain previously defined
                 T-contrasts.
        residual_image: (an existing file name)
                Mean-squared image of the residuals
        spm_mat_file: (an existing file name)
                Absolute path to SPM.mat

        [Optional]
        group_contrast: (a boolean)
                higher level contrast
                mutually_exclusive: use_derivs
        ignore_exception: (a boolean, nipype default value: False)
                Print an error message instead of throwing an exception in case the
                interface fails to run
        matlab_cmd: (a string)
                matlab command to use
        mfile: (a boolean, nipype default value: True)
                Run m-code using m-file
        paths: (a directory name)
                Paths to add to matlabpath
        use_derivs: (a boolean)
                use derivatives for estimation
                mutually_exclusive: group_contrast
        use_mcr: (a boolean)
                Run m-code using SPM MCR
        use_v8struct: (a boolean, nipype default value: True)
                Generate SPM8 and higher compatible jobs

Outputs::

        con_images: (an existing file name)
                contrast images from a t-contrast
        ess_images: (an existing file name)
                contrast images from an F-contrast
        spmF_images: (an existing file name)
                stat images from an F-contrast
        spmT_images: (an existing file name)
                stat images from a t-contrast
        spm_mat_file: (an existing file name)
                Updated SPM mat file

.. _nipype.interfaces.spm.model.EstimateModel:


.. index:: EstimateModel

EstimateModel
-------------

`Link to code <http://github.com/nipy/nipype/tree/e63e055194d62d2bdc4665688261c03a42fd0025/nipype/interfaces/spm/model.py#L182>`__

Use spm_spm to estimate the parameters of a model

http://www.fil.ion.ucl.ac.uk/spm/doc/manual.pdf#page=71

Examples
~~~~~~~~
>>> est = EstimateModel()
>>> est.inputs.spm_mat_file = 'SPM.mat'
>>> est.run() # doctest: +SKIP

Inputs::

        [Mandatory]
        estimation_method: (a dictionary with keys which are 'Classical' or
                 'Bayesian2' or 'Bayesian' and with values which are any value)
                Classical, Bayesian2, Bayesian (dict)
        spm_mat_file: (an existing file name)
                absolute path to SPM.mat

        [Optional]
        flags: (a string)
                optional arguments (opt)
        ignore_exception: (a boolean, nipype default value: False)
                Print an error message instead of throwing an exception in case the
                interface fails to run
        matlab_cmd: (a string)
                matlab command to use
        mfile: (a boolean, nipype default value: True)
                Run m-code using m-file
        paths: (a directory name)
                Paths to add to matlabpath
        use_mcr: (a boolean)
                Run m-code using SPM MCR
        use_v8struct: (a boolean, nipype default value: True)
                Generate SPM8 and higher compatible jobs

Outputs::

        RPVimage: (an existing file name)
                Resels per voxel image
        beta_images: (an existing file name)
                design parameter estimates
        mask_image: (an existing file name)
                binary mask to constrain estimation
        residual_image: (an existing file name)
                Mean-squared image of the residuals
        spm_mat_file: (an existing file name)
                Updated SPM mat file

.. _nipype.interfaces.spm.model.FactorialDesign:


.. index:: FactorialDesign

FactorialDesign
---------------

`Link to code <http://github.com/nipy/nipype/tree/e63e055194d62d2bdc4665688261c03a42fd0025/nipype/interfaces/spm/model.py#L744>`__

Base class for factorial designs

http://www.fil.ion.ucl.ac.uk/spm/doc/manual.pdf#page=79

Inputs::

        [Mandatory]

        [Optional]
        covariates: (a dictionary with keys which are 'vector' or 'name' or
                 'interaction' or 'centering' and with values which are any value)
                covariate dictionary {vector, name, interaction, centering}
        explicit_mask_file: (a file name)
                use an implicit mask file to threshold
        global_calc_mean: (a boolean)
                use mean for global calculation
                mutually_exclusive: global_calc_omit, global_calc_values
        global_calc_omit: (a boolean)
                omit global calculation
                mutually_exclusive: global_calc_mean, global_calc_values
        global_calc_values: (a list of items which are a float)
                omit global calculation
                mutually_exclusive: global_calc_mean, global_calc_omit
        global_normalization: (1 or 2 or 3)
                global normalization None-1, Proportional-2, ANCOVA-3
        ignore_exception: (a boolean, nipype default value: False)
                Print an error message instead of throwing an exception in case the
                interface fails to run
        matlab_cmd: (a string)
                matlab command to use
        mfile: (a boolean, nipype default value: True)
                Run m-code using m-file
        no_grand_mean_scaling: (a boolean)
                do not perform grand mean scaling
        paths: (a directory name)
                Paths to add to matlabpath
        spm_mat_dir: (an existing directory name)
                directory to store SPM.mat file (opt)
        threshold_mask_absolute: (a float)
                use an absolute threshold
                mutually_exclusive: threshold_mask_none, threshold_mask_relative
        threshold_mask_none: (a boolean)
                do not use threshold masking
                mutually_exclusive: threshold_mask_absolute, threshold_mask_relative
        threshold_mask_relative: (a float)
                threshold using a proportion of the global value
                mutually_exclusive: threshold_mask_absolute, threshold_mask_none
        use_implicit_threshold: (a boolean)
                use implicit mask NaNs or zeros to threshold
        use_mcr: (a boolean)
                Run m-code using SPM MCR
        use_v8struct: (a boolean, nipype default value: True)
                Generate SPM8 and higher compatible jobs

Outputs::

        spm_mat_file: (an existing file name)
                SPM mat file

.. _nipype.interfaces.spm.model.Level1Design:


.. index:: Level1Design

Level1Design
------------

`Link to code <http://github.com/nipy/nipype/tree/e63e055194d62d2bdc4665688261c03a42fd0025/nipype/interfaces/spm/model.py#L92>`__

Generate an SPM design matrix

http://www.fil.ion.ucl.ac.uk/spm/doc/manual.pdf#page=61

Examples
~~~~~~~~

>>> level1design = Level1Design()
>>> level1design.inputs.timing_units = 'secs'
>>> level1design.inputs.interscan_interval = 2.5
>>> level1design.inputs.bases = {'hrf':{'derivs': [0,0]}}
>>> level1design.inputs.session_info = 'session_info.npz'
>>> level1design.run() # doctest: +SKIP

Inputs::

        [Mandatory]
        bases: (a dictionary with keys which are 'hrf' or 'fourier' or
                 'fourier_han' or 'gamma' or 'fir' and with values which are any
                 value)
                 dict {'name':{'basesparam1':val,...}}
                 name : string
                 Name of basis function (hrf, fourier, fourier_han,
                 gamma, fir)
                 hrf :
                 derivs : 2-element list
                 Model HRF Derivatives. No derivatives: [0,0],
                 Time derivatives : [1,0], Time and Dispersion
                 derivatives: [1,1]
                 fourier, fourier_han, gamma, fir:
                 length : int
                 Post-stimulus window length (in seconds)
                 order : int
                 Number of basis functions
        interscan_interval: (a float)
                Interscan interval in secs
        session_info
                Session specific information generated by ``modelgen.SpecifyModel``
        timing_units: ('secs' or 'scans')
                units for specification of onsets

        [Optional]
        factor_info: (a list of items which are a dictionary with keys which
                 are 'name' or 'levels' and with values which are any value)
                Factor specific information file (opt)
        global_intensity_normalization: ('none' or 'scaling')
                Global intensity normalization - scaling or none
        ignore_exception: (a boolean, nipype default value: False)
                Print an error message instead of throwing an exception in case the
                interface fails to run
        mask_image: (an existing file name)
                Image for explicitly masking the analysis
        mask_threshold: ('-Inf' or a float, nipype default value: -Inf)
                Thresholding for the mask
        matlab_cmd: (a string)
                matlab command to use
        mfile: (a boolean, nipype default value: True)
                Run m-code using m-file
        microtime_onset: (a float)
                The onset/time-bin in seconds for alignment (opt)
        microtime_resolution: (an integer)
                Number of time-bins per scan in secs (opt)
        model_serial_correlations: ('AR(1)' or 'FAST' or 'none')
                Model serial correlations AR(1), FAST or none. FAST is available in
                SPM12
        paths: (a directory name)
                Paths to add to matlabpath
        spm_mat_dir: (an existing directory name)
                directory to store SPM.mat file (opt)
        use_mcr: (a boolean)
                Run m-code using SPM MCR
        use_v8struct: (a boolean, nipype default value: True)
                Generate SPM8 and higher compatible jobs
        volterra_expansion_order: (1 or 2)
                Model interactions - yes:1, no:2

Outputs::

        spm_mat_file: (an existing file name)
                SPM mat file

.. _nipype.interfaces.spm.model.MultipleRegressionDesign:


.. index:: MultipleRegressionDesign

MultipleRegressionDesign
------------------------

`Link to code <http://github.com/nipy/nipype/tree/e63e055194d62d2bdc4665688261c03a42fd0025/nipype/interfaces/spm/model.py#L900>`__

Create SPM design for multiple regression

Examples
~~~~~~~~

>>> mreg = MultipleRegressionDesign()
>>> mreg.inputs.in_files = ['cont1.nii','cont2.nii']
>>> mreg.run() # doctest: +SKIP

Inputs::

        [Mandatory]
        in_files: (a list of at least 2 items which are an existing file
                 name)
                List of files

        [Optional]
        covariates: (a dictionary with keys which are 'vector' or 'name' or
                 'interaction' or 'centering' and with values which are any value)
                covariate dictionary {vector, name, interaction, centering}
        explicit_mask_file: (a file name)
                use an implicit mask file to threshold
        global_calc_mean: (a boolean)
                use mean for global calculation
                mutually_exclusive: global_calc_omit, global_calc_values
        global_calc_omit: (a boolean)
                omit global calculation
                mutually_exclusive: global_calc_mean, global_calc_values
        global_calc_values: (a list of items which are a float)
                omit global calculation
                mutually_exclusive: global_calc_mean, global_calc_omit
        global_normalization: (1 or 2 or 3)
                global normalization None-1, Proportional-2, ANCOVA-3
        ignore_exception: (a boolean, nipype default value: False)
                Print an error message instead of throwing an exception in case the
                interface fails to run
        include_intercept: (a boolean, nipype default value: True)
                Include intercept in design
        matlab_cmd: (a string)
                matlab command to use
        mfile: (a boolean, nipype default value: True)
                Run m-code using m-file
        no_grand_mean_scaling: (a boolean)
                do not perform grand mean scaling
        paths: (a directory name)
                Paths to add to matlabpath
        spm_mat_dir: (an existing directory name)
                directory to store SPM.mat file (opt)
        threshold_mask_absolute: (a float)
                use an absolute threshold
                mutually_exclusive: threshold_mask_none, threshold_mask_relative
        threshold_mask_none: (a boolean)
                do not use threshold masking
                mutually_exclusive: threshold_mask_absolute, threshold_mask_relative
        threshold_mask_relative: (a float)
                threshold using a proportion of the global value
                mutually_exclusive: threshold_mask_absolute, threshold_mask_none
        use_implicit_threshold: (a boolean)
                use implicit mask NaNs or zeros to threshold
        use_mcr: (a boolean)
                Run m-code using SPM MCR
        use_v8struct: (a boolean, nipype default value: True)
                Generate SPM8 and higher compatible jobs
        user_covariates: (a dictionary with keys which are 'vector' or 'name'
                 or 'centering' and with values which are any value)
                covariate dictionary {vector, name, centering}

Outputs::

        spm_mat_file: (an existing file name)
                SPM mat file

.. _nipype.interfaces.spm.model.OneSampleTTestDesign:


.. index:: OneSampleTTestDesign

OneSampleTTestDesign
--------------------

`Link to code <http://github.com/nipy/nipype/tree/e63e055194d62d2bdc4665688261c03a42fd0025/nipype/interfaces/spm/model.py#L795>`__

Create SPM design for one sample t-test

Examples
~~~~~~~~

>>> ttest = OneSampleTTestDesign()
>>> ttest.inputs.in_files = ['cont1.nii', 'cont2.nii']
>>> ttest.run() # doctest: +SKIP

Inputs::

        [Mandatory]
        in_files: (a list of at least 2 items which are an existing file
                 name)
                input files

        [Optional]
        covariates: (a dictionary with keys which are 'vector' or 'name' or
                 'interaction' or 'centering' and with values which are any value)
                covariate dictionary {vector, name, interaction, centering}
        explicit_mask_file: (a file name)
                use an implicit mask file to threshold
        global_calc_mean: (a boolean)
                use mean for global calculation
                mutually_exclusive: global_calc_omit, global_calc_values
        global_calc_omit: (a boolean)
                omit global calculation
                mutually_exclusive: global_calc_mean, global_calc_values
        global_calc_values: (a list of items which are a float)
                omit global calculation
                mutually_exclusive: global_calc_mean, global_calc_omit
        global_normalization: (1 or 2 or 3)
                global normalization None-1, Proportional-2, ANCOVA-3
        ignore_exception: (a boolean, nipype default value: False)
                Print an error message instead of throwing an exception in case the
                interface fails to run
        matlab_cmd: (a string)
                matlab command to use
        mfile: (a boolean, nipype default value: True)
                Run m-code using m-file
        no_grand_mean_scaling: (a boolean)
                do not perform grand mean scaling
        paths: (a directory name)
                Paths to add to matlabpath
        spm_mat_dir: (an existing directory name)
                directory to store SPM.mat file (opt)
        threshold_mask_absolute: (a float)
                use an absolute threshold
                mutually_exclusive: threshold_mask_none, threshold_mask_relative
        threshold_mask_none: (a boolean)
                do not use threshold masking
                mutually_exclusive: threshold_mask_absolute, threshold_mask_relative
        threshold_mask_relative: (a float)
                threshold using a proportion of the global value
                mutually_exclusive: threshold_mask_absolute, threshold_mask_none
        use_implicit_threshold: (a boolean)
                use implicit mask NaNs or zeros to threshold
        use_mcr: (a boolean)
                Run m-code using SPM MCR
        use_v8struct: (a boolean, nipype default value: True)
                Generate SPM8 and higher compatible jobs

Outputs::

        spm_mat_file: (an existing file name)
                SPM mat file

.. _nipype.interfaces.spm.model.PairedTTestDesign:


.. index:: PairedTTestDesign

PairedTTestDesign
-----------------

`Link to code <http://github.com/nipy/nipype/tree/e63e055194d62d2bdc4665688261c03a42fd0025/nipype/interfaces/spm/model.py#L864>`__

Create SPM design for paired t-test

Examples
~~~~~~~~

>>> pttest = PairedTTestDesign()
>>> pttest.inputs.paired_files = [['cont1.nii','cont1a.nii'],['cont2.nii','cont2a.nii']]
>>> pttest.run() # doctest: +SKIP

Inputs::

        [Mandatory]
        paired_files: (a list of at least 2 items which are a list of from 2
                 to 2 items which are an existing file name)
                List of paired files

        [Optional]
        ancova: (a boolean)
                Specify ancova-by-factor regressors
        covariates: (a dictionary with keys which are 'vector' or 'name' or
                 'interaction' or 'centering' and with values which are any value)
                covariate dictionary {vector, name, interaction, centering}
        explicit_mask_file: (a file name)
                use an implicit mask file to threshold
        global_calc_mean: (a boolean)
                use mean for global calculation
                mutually_exclusive: global_calc_omit, global_calc_values
        global_calc_omit: (a boolean)
                omit global calculation
                mutually_exclusive: global_calc_mean, global_calc_values
        global_calc_values: (a list of items which are a float)
                omit global calculation
                mutually_exclusive: global_calc_mean, global_calc_omit
        global_normalization: (1 or 2 or 3)
                global normalization None-1, Proportional-2, ANCOVA-3
        grand_mean_scaling: (a boolean)
                Perform grand mean scaling
        ignore_exception: (a boolean, nipype default value: False)
                Print an error message instead of throwing an exception in case the
                interface fails to run
        matlab_cmd: (a string)
                matlab command to use
        mfile: (a boolean, nipype default value: True)
                Run m-code using m-file
        no_grand_mean_scaling: (a boolean)
                do not perform grand mean scaling
        paths: (a directory name)
                Paths to add to matlabpath
        spm_mat_dir: (an existing directory name)
                directory to store SPM.mat file (opt)
        threshold_mask_absolute: (a float)
                use an absolute threshold
                mutually_exclusive: threshold_mask_none, threshold_mask_relative
        threshold_mask_none: (a boolean)
                do not use threshold masking
                mutually_exclusive: threshold_mask_absolute, threshold_mask_relative
        threshold_mask_relative: (a float)
                threshold using a proportion of the global value
                mutually_exclusive: threshold_mask_absolute, threshold_mask_none
        use_implicit_threshold: (a boolean)
                use implicit mask NaNs or zeros to threshold
        use_mcr: (a boolean)
                Run m-code using SPM MCR
        use_v8struct: (a boolean, nipype default value: True)
                Generate SPM8 and higher compatible jobs

Outputs::

        spm_mat_file: (an existing file name)
                SPM mat file

.. _nipype.interfaces.spm.model.Threshold:


.. index:: Threshold

Threshold
---------

`Link to code <http://github.com/nipy/nipype/tree/e63e055194d62d2bdc4665688261c03a42fd0025/nipype/interfaces/spm/model.py#L439>`__

Topological FDR thresholding based on cluster extent/size. Smoothness is
estimated from GLM residuals but is assumed to be the same for all of the
voxels.

Examples
~~~~~~~~

>>> thresh = Threshold()
>>> thresh.inputs.spm_mat_file = 'SPM.mat'
>>> thresh.inputs.stat_image = 'spmT_0001.img'
>>> thresh.inputs.contrast_index = 1
>>> thresh.inputs.extent_fdr_p_threshold = 0.05
>>> thresh.run() # doctest: +SKIP

Inputs::

        [Mandatory]
        contrast_index: (an integer)
                which contrast in the SPM.mat to use
        spm_mat_file: (an existing file name)
                absolute path to SPM.mat
        stat_image: (an existing file name)
                stat image

        [Optional]
        extent_fdr_p_threshold: (a float, nipype default value: 0.05)
                p threshold on FDR corrected cluster size probabilities
        extent_threshold: (an integer, nipype default value: 0)
                Minimum cluster size in voxels
        force_activation: (a boolean, nipype default value: False)
                In case no clusters survive the topological inference step this will
                pick a culster with the highes sum of t-values. Use with care.
        height_threshold: (a float, nipype default value: 0.05)
                value for initial thresholding (defining clusters)
        height_threshold_type: ('p-value' or 'stat', nipype default value:
                 p-value)
                Is the cluster forming threshold a stat value or p-value?
        ignore_exception: (a boolean, nipype default value: False)
                Print an error message instead of throwing an exception in case the
                interface fails to run
        matlab_cmd: (a string)
                matlab command to use
        mfile: (a boolean, nipype default value: True)
                Run m-code using m-file
        paths: (a directory name)
                Paths to add to matlabpath
        use_fwe_correction: (a boolean, nipype default value: True)
                whether to use FWE (Bonferroni) correction for initial threshold
                (height_threshold_type has to be set to p-value)
        use_mcr: (a boolean)
                Run m-code using SPM MCR
        use_topo_fdr: (a boolean, nipype default value: True)
                whether to use FDR over cluster extent probabilities
        use_v8struct: (a boolean, nipype default value: True)
                Generate SPM8 and higher compatible jobs

Outputs::

        activation_forced: (a boolean)
        cluster_forming_thr: (a float)
        n_clusters: (an integer)
        pre_topo_fdr_map: (an existing file name)
        pre_topo_n_clusters: (an integer)
        thresholded_map: (an existing file name)

.. _nipype.interfaces.spm.model.ThresholdStatistics:


.. index:: ThresholdStatistics

ThresholdStatistics
-------------------

`Link to code <http://github.com/nipy/nipype/tree/e63e055194d62d2bdc4665688261c03a42fd0025/nipype/interfaces/spm/model.py#L618>`__

Given height and cluster size threshold calculate theoretical probabilities
concerning false positives

Examples
~~~~~~~~

>>> thresh = ThresholdStatistics()
>>> thresh.inputs.spm_mat_file = 'SPM.mat'
>>> thresh.inputs.stat_image = 'spmT_0001.img'
>>> thresh.inputs.contrast_index = 1
>>> thresh.inputs.height_threshold = 4.56
>>> thresh.run() # doctest: +SKIP

Inputs::

        [Mandatory]
        contrast_index: (an integer)
                which contrast in the SPM.mat to use
        height_threshold: (a float)
                stat value for initial thresholding (defining clusters)
        spm_mat_file: (an existing file name)
                absolute path to SPM.mat
        stat_image: (an existing file name)
                stat image

        [Optional]
        extent_threshold: (an integer, nipype default value: 0)
                Minimum cluster size in voxels
        ignore_exception: (a boolean, nipype default value: False)
                Print an error message instead of throwing an exception in case the
                interface fails to run
        matlab_cmd: (a string)
                matlab command to use
        mfile: (a boolean, nipype default value: True)
                Run m-code using m-file
        paths: (a directory name)
                Paths to add to matlabpath
        use_mcr: (a boolean)
                Run m-code using SPM MCR
        use_v8struct: (a boolean, nipype default value: True)
                Generate SPM8 and higher compatible jobs

Outputs::

        clusterwise_P_FDR: (a float)
        clusterwise_P_RF: (a float)
        voxelwise_P_Bonf: (a float)
        voxelwise_P_FDR: (a float)
        voxelwise_P_RF: (a float)
        voxelwise_P_uncor: (a float)

.. _nipype.interfaces.spm.model.TwoSampleTTestDesign:


.. index:: TwoSampleTTestDesign

TwoSampleTTestDesign
--------------------

`Link to code <http://github.com/nipy/nipype/tree/e63e055194d62d2bdc4665688261c03a42fd0025/nipype/interfaces/spm/model.py#L831>`__

Create SPM design for two sample t-test

Examples
~~~~~~~~

>>> ttest = TwoSampleTTestDesign()
>>> ttest.inputs.group1_files = ['cont1.nii', 'cont2.nii']
>>> ttest.inputs.group2_files = ['cont1a.nii', 'cont2a.nii']
>>> ttest.run() # doctest: +SKIP

Inputs::

        [Mandatory]
        group1_files: (a list of at least 2 items which are an existing file
                 name)
                Group 1 input files
        group2_files: (a list of at least 2 items which are an existing file
                 name)
                Group 2 input files

        [Optional]
        covariates: (a dictionary with keys which are 'vector' or 'name' or
                 'interaction' or 'centering' and with values which are any value)
                covariate dictionary {vector, name, interaction, centering}
        dependent: (a boolean)
                Are the measurements dependent between levels
        explicit_mask_file: (a file name)
                use an implicit mask file to threshold
        global_calc_mean: (a boolean)
                use mean for global calculation
                mutually_exclusive: global_calc_omit, global_calc_values
        global_calc_omit: (a boolean)
                omit global calculation
                mutually_exclusive: global_calc_mean, global_calc_values
        global_calc_values: (a list of items which are a float)
                omit global calculation
                mutually_exclusive: global_calc_mean, global_calc_omit
        global_normalization: (1 or 2 or 3)
                global normalization None-1, Proportional-2, ANCOVA-3
        ignore_exception: (a boolean, nipype default value: False)
                Print an error message instead of throwing an exception in case the
                interface fails to run
        matlab_cmd: (a string)
                matlab command to use
        mfile: (a boolean, nipype default value: True)
                Run m-code using m-file
        no_grand_mean_scaling: (a boolean)
                do not perform grand mean scaling
        paths: (a directory name)
                Paths to add to matlabpath
        spm_mat_dir: (an existing directory name)
                directory to store SPM.mat file (opt)
        threshold_mask_absolute: (a float)
                use an absolute threshold
                mutually_exclusive: threshold_mask_none, threshold_mask_relative
        threshold_mask_none: (a boolean)
                do not use threshold masking
                mutually_exclusive: threshold_mask_absolute, threshold_mask_relative
        threshold_mask_relative: (a float)
                threshold using a proportion of the global value
                mutually_exclusive: threshold_mask_absolute, threshold_mask_none
        unequal_variance: (a boolean)
                Are the variances equal or unequal between groups
        use_implicit_threshold: (a boolean)
                use implicit mask NaNs or zeros to threshold
        use_mcr: (a boolean)
                Run m-code using SPM MCR
        use_v8struct: (a boolean, nipype default value: True)
                Generate SPM8 and higher compatible jobs

Outputs::

        spm_mat_file: (an existing file name)
                SPM mat file
