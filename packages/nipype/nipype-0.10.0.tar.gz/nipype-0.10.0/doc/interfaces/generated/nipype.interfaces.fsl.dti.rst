.. AUTO-GENERATED FILE -- DO NOT EDIT!

interfaces.fsl.dti
==================


.. _nipype.interfaces.fsl.dti.BEDPOSTX:


.. index:: BEDPOSTX

BEDPOSTX
--------

`Link to code <http://github.com/nipy/nipype/tree/e63e055194d62d2bdc4665688261c03a42fd0025/nipype/interfaces/fsl/dti.py#L638>`__

Wraps command **bedpostx**


Inputs::

        [Mandatory]
        bvals: (an existing file name)
                b values file
                flag: --bvals=%s
        bvecs: (an existing file name)
                b vectors file
                flag: --bvecs=%s
        dwi: (an existing file name)
                diffusion weighted image data file
                flag: --data=%s
        mask: (an existing file name)
                brain binary mask file (i.e. from BET)
                flag: --mask=%s
        out_dir: (a directory name, nipype default value: .)
                output directory
                flag: %s, position: 1
        terminal_output: ('stream' or 'allatonce' or 'file' or 'none')
                Control terminal output: `stream` - displays to terminal
                immediately, `allatonce` - waits till command is finished to display
                output, `file` - writes output to file, `none` - output is ignored

        [Optional]
        all_ard: (a boolean)
                Turn ARD on on all fibres
                flag: --allard
                mutually_exclusive: no_ard, all_ard
        args: (a string)
                Additional parameters to the command
                flag: %s
        burn_in: (an integer >= 0)
                Total num of jumps at start of MCMC to be discarded
                flag: --burnin=%d
        burn_in_no_ard: (an integer >= 0)
                num of burnin jumps before the ard is imposed
                flag: --burninnoard=%d
        cnlinear: (a boolean)
                Initialise with constrained nonlinear fitting
                flag: --cnonlinear
                mutually_exclusive: no_spat, non_linear, cnlinear
        environ: (a dictionary with keys which are a value of type 'str' and
                 with values which are a value of type 'str', nipype default value:
                 {})
                Environment variables
        f0_ard: (a boolean)
                Noise floor model: add to the model an unattenuated signal
                compartment f0
                flag: --f0 --ardf0
                mutually_exclusive: f0_noard, f0_ard, all_ard
        f0_noard: (a boolean)
                Noise floor model: add to the model an unattenuated signal
                compartment f0
                flag: --f0
                mutually_exclusive: f0_noard, f0_ard
        force_dir: (a boolean, nipype default value: True)
                use the actual directory name given (do not add + to make a new
                directory)
                flag: --forcedir
        fudge: (an integer)
                ARD fudge factor
                flag: --fudge=%d
        gradnonlin: (a boolean)
                consider gradient nonlinearities, default off
                flag: -g
        ignore_exception: (a boolean, nipype default value: False)
                Print an error message instead of throwing an exception in case the
                interface fails to run
        logdir: (a directory name, nipype default value: .)
                flag: --logdir=%s
        model: (1 or 2)
                use monoexponential (1, default, required for single-shell) or
                multiexponential (2, multi-shell) model
                flag: --model=%d
        n_fibres: (an integer >= 1)
                Maximum number of fibres to fit in each voxel
                flag: --nfibres=%d
        n_jumps: (an integer)
                Num of jumps to be made by MCMC
                flag: --njumps=%d
        no_ard: (a boolean)
                Turn ARD off on all fibres
                flag: --noard
                mutually_exclusive: no_ard, all_ard
        no_spat: (a boolean)
                Initialise with tensor, not spatially
                flag: --nospat
                mutually_exclusive: no_spat, non_linear, cnlinear
        non_linear: (a boolean)
                Initialise with nonlinear fitting
                flag: --nonlinear
                mutually_exclusive: no_spat, non_linear, cnlinear
        output_type: ('NIFTI_PAIR' or 'NIFTI_PAIR_GZ' or 'NIFTI_GZ' or
                 'NIFTI')
                FSL output type
        rician: (a boolean)
                use Rician noise modeling
                flag: --rician
        sample_every: (an integer >= 0)
                Num of jumps for each sample (MCMC)
                flag: --sampleevery=%d
        seed: (an integer)
                seed for pseudo random number generator
                flag: --seed=%d
        update_proposal_every: (an integer >= 1)
                Num of jumps for each update to the proposal density std (MCMC)
                flag: --updateproposalevery=%d
        use_gpu: (a boolean)
                Use the GPU version of bedpostx

Outputs::

        d_stdsamples: (a file name)
                Std of samples from the distribution d
        dsamples: (a file name)
                Samples from the distribution on diffusivity d
        dyads: (a file name)
                Mean of PDD distribution in vector form.
        dyads_disp: (a file name)
                Uncertainty on the estimated fiber orientation
        fsamples: (a file name)
                Samples from the distribution on f anisotropy
        mean_S0samples: (a file name)
                Mean of distribution on T2wbaseline signal intensity S0
        mean_d_stdsamples: (a file name)
                Mean of distribution on diffusivity d
        mean_dsamples: (a file name)
                Mean of distribution on diffusivity d
        mean_fsamples: (a file name)
                Mean of distribution on f anisotropy
        mean_phsamples: (a file name)
                Mean of distribution on phi
        mean_tausamples: (a file name)
                Mean of distribution on tau samples (only with rician noise)
        mean_thsamples: (a file name)
                Mean of distribution on theta
        merged_fsamples: (a file name)
                Samples from the distribution on anisotropic volume fraction.
        merged_phsamples: (a file name)
                Samples from the distribution on phi
        merged_thsamples: (a file name)
                Samples from the distribution on theta
        phsamples: (a file name)
                phi samples, per fiber
        thsamples: (a file name)
                theta samples, per fiber

.. _nipype.interfaces.fsl.dti.BEDPOSTX4:


.. index:: BEDPOSTX4

BEDPOSTX4
---------

`Link to code <http://github.com/nipy/nipype/tree/e63e055194d62d2bdc4665688261c03a42fd0025/nipype/interfaces/fsl/dti.py#L533>`__

Wraps command **bedpostx**

bedpostx has an old interface, implemented here


Example
~~~~~~~

>>> from nipype.interfaces import fsl
>>> bedp = fsl.BEDPOSTX4(bpx_directory='subjdir', bvecs='bvecs', bvals='bvals', dwi='diffusion.nii', mask='mask.nii', fibres=1)
>>> bedp.cmdline
'bedpostx subjdir -n 1 --forcedir --logdir=logdir'

Inputs::

        [Mandatory]
        bvals: (an existing file name)
                b values file
        bvecs: (an existing file name)
                b vectors file
        dwi: (an existing file name)
                diffusion weighted image data file
        mask: (an existing file name)
                bet binary mask file
        terminal_output: ('stream' or 'allatonce' or 'file' or 'none')
                Control terminal output: `stream` - displays to terminal
                immediately, `allatonce` - waits till command is finished to display
                output, `file` - writes output to file, `none` - output is ignored

        [Optional]
        all_ard: (a boolean)
                Turn ARD on on all fibres
                flag: --allard
                mutually_exclusive: no_ard, all_ard
        args: (a string)
                Additional parameters to the command
                flag: %s
        bpx_directory: (a directory name, nipype default value: bedpostx)
                the name for this subject's bedpostx folder
                flag: %s
        burn_in: (an integer >= 0)
                Total num of jumps at start of MCMC to be discarded
                flag: --burnin=%d
        burn_in_no_ard: (an integer >= 0)
                num of burnin jumps before the ard is imposed
                flag: --burninnoard=%d
        burn_period: (an integer)
                burnin period
                flag: -b %d
        environ: (a dictionary with keys which are a value of type 'str' and
                 with values which are a value of type 'str', nipype default value:
                 {})
                Environment variables
        fibres: (an integer)
                number of fibres per voxel
                flag: -n %d
        force_dir: (a boolean, nipype default value: True)
                use the actual directory name given - i.e. do not add + to make a
                new directory
                flag: --forcedir
        fudge: (an integer)
                ARD fudge factor
                flag: --fudge=%d
        gradnonlin: (an existing file name)
                flag: --gradnonlin=%s
        ignore_exception: (a boolean, nipype default value: False)
                Print an error message instead of throwing an exception in case the
                interface fails to run
        jumps: (an integer)
                number of jumps
                flag: -j %d
        logdir: (a directory name, nipype default value: logdir)
                flag: --logdir=%s
        model: (1 or 2)
                model choice: monoexponential (1) or multiexponential (2).
                flag: -model %d
        n_fibres: (an integer >= 1)
                Maximum nukmber of fibres to fit in each voxel
                flag: --nfibres=%d
        n_jumps: (an integer >= 1)
                Num of jumps to be made by MCMC
                flag: --njumps=%d
        nlgradient: (a boolean)
                consider gradientnonlinearities, default off
                flag: -g
        no_ard: (a boolean)
                Turn ARD off on all fibres
                flag: --noard
                mutually_exclusive: no_ard, all_ard
        no_cuda: (a boolean)
                do not use CUDA capable hardware/queue (if found)
                flag: -c
        no_spat: (a boolean)
                Initialise with tensor, not spatially
                flag: --nospat
                mutually_exclusive: no_spat, non_linear
        non_linear: (a boolean)
                Initialise with nonlinear fitting
                flag: --nonlinear
                mutually_exclusive: no_spat, non_linear
        output_type: ('NIFTI_PAIR' or 'NIFTI_PAIR_GZ' or 'NIFTI_GZ' or
                 'NIFTI')
                FSL output type
        sample_every: (an integer >= 0)
                Num of jumps for each sample (MCMC)
                flag: --sampleevery=%d
        sampling: (an integer)
                sample every
                flag: -s %d
        seed: (an integer)
                seed for pseudo random number generator
                flag: --seed=%d
        update_proposal_every: (an integer >= 1)
                Num of jumps for each update to the proposal density std (MCMC)
                flag: --updateproposalevery=%d
        weight: (a float)
                ARD weight, more weight means less secondary fibres per voxel
                flag: -w %.2f

Outputs::

        bpx_out_directory: (an existing directory name)
                path/name of directory with all bedpostx output files for this
                subject
        dyads: (a list of items which are an existing file name)
                a list of path/name of mean of PDD distribution in vector form
        mean_fsamples: (a list of items which are an existing file name)
                a list of path/name of 3D volume with mean of distribution on f
                anisotropy
        mean_phsamples: (a list of items which are an existing file name)
                a list of path/name of 3D volume with mean of distribution on phi
        mean_thsamples: (a list of items which are an existing file name)
                a list of path/name of 3D volume with mean of distribution on theta
        merged_fsamples: (a list of items which are an existing file name)
                a list of path/name of 4D volume with samples from the distribution
                on anisotropic volume fraction
        merged_phsamples: (a list of items which are an existing file name)
                a list of path/name of file with samples from the distribution on
                phi
        merged_thsamples: (a list of items which are an existing file name)
                a list of path/name of 4D volume with samples from the distribution
                on theta
        xfms_directory: (an existing directory name)
                path/name of directory with the tranformation matrices

.. _nipype.interfaces.fsl.dti.BEDPOSTX5:


.. index:: BEDPOSTX5

BEDPOSTX5
---------

`Link to code <http://github.com/nipy/nipype/tree/e63e055194d62d2bdc4665688261c03a42fd0025/nipype/interfaces/fsl/dti.py#L266>`__

Wraps command **bedpostx**

BEDPOSTX stands for Bayesian Estimation of Diffusion Parameters Obtained
using Sampling Techniques. The X stands for modelling Crossing Fibres.
bedpostx runs Markov Chain Monte Carlo sampling to build up distributions
on diffusion parameters at each voxel. It creates all the files necessary
for running probabilistic tractography. For an overview of the modelling
carried out within bedpostx see this `technical report
<http://www.fmrib.ox.ac.uk/analysis/techrep/tr03tb1/tr03tb1/index.html>`_.


.. note:: Consider using
  :func:`nipype.workflows.fsl.dmri.create_bedpostx_pipeline` instead.


Example
~~~~~~~

>>> from nipype.interfaces import fsl
>>> bedp = fsl.BEDPOSTX5(bvecs='bvecs', bvals='bvals', dwi='diffusion.nii',
...                     mask='mask.nii', n_fibres=1)
>>> bedp.cmdline
'bedpostx . --bvals=bvals --bvecs=bvecs --data=diffusion.nii --forcedir --logdir=. --mask=mask.nii --nfibres=1'

Inputs::

        [Mandatory]
        bvals: (an existing file name)
                b values file
                flag: --bvals=%s
        bvecs: (an existing file name)
                b vectors file
                flag: --bvecs=%s
        dwi: (an existing file name)
                diffusion weighted image data file
                flag: --data=%s
        mask: (an existing file name)
                brain binary mask file (i.e. from BET)
                flag: --mask=%s
        out_dir: (a directory name, nipype default value: .)
                output directory
                flag: %s, position: 1
        terminal_output: ('stream' or 'allatonce' or 'file' or 'none')
                Control terminal output: `stream` - displays to terminal
                immediately, `allatonce` - waits till command is finished to display
                output, `file` - writes output to file, `none` - output is ignored

        [Optional]
        all_ard: (a boolean)
                Turn ARD on on all fibres
                flag: --allard
                mutually_exclusive: no_ard, all_ard
        args: (a string)
                Additional parameters to the command
                flag: %s
        burn_in: (an integer >= 0)
                Total num of jumps at start of MCMC to be discarded
                flag: --burnin=%d
        burn_in_no_ard: (an integer >= 0)
                num of burnin jumps before the ard is imposed
                flag: --burninnoard=%d
        cnlinear: (a boolean)
                Initialise with constrained nonlinear fitting
                flag: --cnonlinear
                mutually_exclusive: no_spat, non_linear, cnlinear
        environ: (a dictionary with keys which are a value of type 'str' and
                 with values which are a value of type 'str', nipype default value:
                 {})
                Environment variables
        f0_ard: (a boolean)
                Noise floor model: add to the model an unattenuated signal
                compartment f0
                flag: --f0 --ardf0
                mutually_exclusive: f0_noard, f0_ard, all_ard
        f0_noard: (a boolean)
                Noise floor model: add to the model an unattenuated signal
                compartment f0
                flag: --f0
                mutually_exclusive: f0_noard, f0_ard
        force_dir: (a boolean, nipype default value: True)
                use the actual directory name given (do not add + to make a new
                directory)
                flag: --forcedir
        fudge: (an integer)
                ARD fudge factor
                flag: --fudge=%d
        gradnonlin: (a boolean)
                consider gradient nonlinearities, default off
                flag: -g
        ignore_exception: (a boolean, nipype default value: False)
                Print an error message instead of throwing an exception in case the
                interface fails to run
        logdir: (a directory name, nipype default value: .)
                flag: --logdir=%s
        model: (1 or 2)
                use monoexponential (1, default, required for single-shell) or
                multiexponential (2, multi-shell) model
                flag: --model=%d
        n_fibres: (an integer >= 1)
                Maximum number of fibres to fit in each voxel
                flag: --nfibres=%d
        n_jumps: (an integer)
                Num of jumps to be made by MCMC
                flag: --njumps=%d
        no_ard: (a boolean)
                Turn ARD off on all fibres
                flag: --noard
                mutually_exclusive: no_ard, all_ard
        no_spat: (a boolean)
                Initialise with tensor, not spatially
                flag: --nospat
                mutually_exclusive: no_spat, non_linear, cnlinear
        non_linear: (a boolean)
                Initialise with nonlinear fitting
                flag: --nonlinear
                mutually_exclusive: no_spat, non_linear, cnlinear
        output_type: ('NIFTI_PAIR' or 'NIFTI_PAIR_GZ' or 'NIFTI_GZ' or
                 'NIFTI')
                FSL output type
        rician: (a boolean)
                use Rician noise modeling
                flag: --rician
        sample_every: (an integer >= 0)
                Num of jumps for each sample (MCMC)
                flag: --sampleevery=%d
        seed: (an integer)
                seed for pseudo random number generator
                flag: --seed=%d
        update_proposal_every: (an integer >= 1)
                Num of jumps for each update to the proposal density std (MCMC)
                flag: --updateproposalevery=%d
        use_gpu: (a boolean)
                Use the GPU version of bedpostx

Outputs::

        d_stdsamples: (a file name)
                Std of samples from the distribution d
        dsamples: (a file name)
                Samples from the distribution on diffusivity d
        dyads: (a file name)
                Mean of PDD distribution in vector form.
        dyads_disp: (a file name)
                Uncertainty on the estimated fiber orientation
        fsamples: (a file name)
                Samples from the distribution on f anisotropy
        mean_S0samples: (a file name)
                Mean of distribution on T2wbaseline signal intensity S0
        mean_d_stdsamples: (a file name)
                Mean of distribution on diffusivity d
        mean_dsamples: (a file name)
                Mean of distribution on diffusivity d
        mean_fsamples: (a file name)
                Mean of distribution on f anisotropy
        mean_phsamples: (a file name)
                Mean of distribution on phi
        mean_tausamples: (a file name)
                Mean of distribution on tau samples (only with rician noise)
        mean_thsamples: (a file name)
                Mean of distribution on theta
        merged_fsamples: (a file name)
                Samples from the distribution on anisotropic volume fraction.
        merged_phsamples: (a file name)
                Samples from the distribution on phi
        merged_thsamples: (a file name)
                Samples from the distribution on theta
        phsamples: (a file name)
                phi samples, per fiber
        thsamples: (a file name)
                theta samples, per fiber

.. _nipype.interfaces.fsl.dti.DTIFit:


.. index:: DTIFit

DTIFit
------

`Link to code <http://github.com/nipy/nipype/tree/e63e055194d62d2bdc4665688261c03a42fd0025/nipype/interfaces/fsl/dti.py#L69>`__

Wraps command **dtifit**

Use FSL  dtifit command for fitting a diffusion tensor model at each
voxel

Example
~~~~~~~

>>> from nipype.interfaces import fsl
>>> dti = fsl.DTIFit()
>>> dti.inputs.dwi = 'diffusion.nii'
>>> dti.inputs.bvecs = 'bvecs'
>>> dti.inputs.bvals = 'bvals'
>>> dti.inputs.base_name = 'TP'
>>> dti.inputs.mask = 'mask.nii'
>>> dti.cmdline
'dtifit -k diffusion.nii -o TP -m mask.nii -r bvecs -b bvals'

Inputs::

        [Mandatory]
        bvals: (an existing file name)
                b values file
                flag: -b %s, position: 4
        bvecs: (an existing file name)
                b vectors file
                flag: -r %s, position: 3
        dwi: (an existing file name)
                diffusion weighted image data file
                flag: -k %s, position: 0
        mask: (an existing file name)
                bet binary mask file
                flag: -m %s, position: 2
        terminal_output: ('stream' or 'allatonce' or 'file' or 'none')
                Control terminal output: `stream` - displays to terminal
                immediately, `allatonce` - waits till command is finished to display
                output, `file` - writes output to file, `none` - output is ignored

        [Optional]
        args: (a string)
                Additional parameters to the command
                flag: %s
        base_name: (a string, nipype default value: dtifit_)
                base_name that all output files will start with
                flag: -o %s, position: 1
        cni: (an existing file name)
                input counfound regressors
                flag: --cni=%s
        environ: (a dictionary with keys which are a value of type 'str' and
                 with values which are a value of type 'str', nipype default value:
                 {})
                Environment variables
        ignore_exception: (a boolean, nipype default value: False)
                Print an error message instead of throwing an exception in case the
                interface fails to run
        little_bit: (a boolean)
                only process small area of brain
                flag: --littlebit
        max_x: (an integer)
                max x
                flag: -X %d
        max_y: (an integer)
                max y
                flag: -Y %d
        max_z: (an integer)
                max z
                flag: -Z %d
        min_x: (an integer)
                min x
                flag: -x %d
        min_y: (an integer)
                min y
                flag: -y %d
        min_z: (an integer)
                min z
                flag: -z %d
        output_type: ('NIFTI_PAIR' or 'NIFTI_PAIR_GZ' or 'NIFTI_GZ' or
                 'NIFTI')
                FSL output type
        save_tensor: (a boolean)
                save the elements of the tensor
                flag: --save_tensor
        sse: (a boolean)
                output sum of squared errors
                flag: --sse

Outputs::

        FA: (an existing file name)
                path/name of file with the fractional anisotropy
        L1: (an existing file name)
                path/name of file with the 1st eigenvalue
        L2: (an existing file name)
                path/name of file with the 2nd eigenvalue
        L3: (an existing file name)
                path/name of file with the 3rd eigenvalue
        MD: (an existing file name)
                path/name of file with the mean diffusivity
        MO: (an existing file name)
                path/name of file with the mode of anisotropy
        S0: (an existing file name)
                path/name of file with the raw T2 signal with no diffusion weighting
        V1: (an existing file name)
                path/name of file with the 1st eigenvector
        V2: (an existing file name)
                path/name of file with the 2nd eigenvector
        V3: (an existing file name)
                path/name of file with the 3rd eigenvector
        tensor: (an existing file name)
                path/name of file with the 4D tensor volume

.. _nipype.interfaces.fsl.dti.DistanceMap:


.. index:: DistanceMap

DistanceMap
-----------

`Link to code <http://github.com/nipy/nipype/tree/e63e055194d62d2bdc4665688261c03a42fd0025/nipype/interfaces/fsl/dti.py#L1230>`__

Wraps command **distancemap**

Use FSL's distancemap to generate a map of the distance to the nearest nonzero voxel.

Example
~~~~~~~

>>> import nipype.interfaces.fsl as fsl
>>> mapper = fsl.DistanceMap()
>>> mapper.inputs.in_file = "skeleton_mask.nii.gz"
>>> mapper.run() # doctest: +SKIP

Inputs::

        [Mandatory]
        in_file: (an existing file name)
                image to calculate distance values for
                flag: --in=%s
        terminal_output: ('stream' or 'allatonce' or 'file' or 'none')
                Control terminal output: `stream` - displays to terminal
                immediately, `allatonce` - waits till command is finished to display
                output, `file` - writes output to file, `none` - output is ignored

        [Optional]
        args: (a string)
                Additional parameters to the command
                flag: %s
        distance_map: (a file name)
                distance map to write
                flag: --out=%s
        environ: (a dictionary with keys which are a value of type 'str' and
                 with values which are a value of type 'str', nipype default value:
                 {})
                Environment variables
        ignore_exception: (a boolean, nipype default value: False)
                Print an error message instead of throwing an exception in case the
                interface fails to run
        invert_input: (a boolean)
                invert input image
                flag: --invert
        local_max_file: (a boolean or a file name)
                write an image of the local maxima
                flag: --localmax=%s
        mask_file: (an existing file name)
                binary mask to contrain calculations
                flag: --mask=%s
        output_type: ('NIFTI_PAIR' or 'NIFTI_PAIR_GZ' or 'NIFTI_GZ' or
                 'NIFTI')
                FSL output type

Outputs::

        distance_map: (an existing file name)
                value is distance to nearest nonzero voxels
        local_max_file: (a file name)
                image of local maxima

.. _nipype.interfaces.fsl.dti.FindTheBiggest:


.. index:: FindTheBiggest

FindTheBiggest
--------------

`Link to code <http://github.com/nipy/nipype/tree/e63e055194d62d2bdc4665688261c03a42fd0025/nipype/interfaces/fsl/dti.py#L1074>`__

Wraps command **find_the_biggest**

Use FSL find_the_biggest for performing hard segmentation on
the outputs of connectivity-based thresholding in probtrack.
For complete details, see the `FDT
Documentation. <http://www.fmrib.ox.ac.uk/fsl/fdt/fdt_biggest.html>`_

Example
~~~~~~~

>>> from nipype.interfaces import fsl
>>> ldir = ['seeds_to_M1.nii', 'seeds_to_M2.nii']
>>> fBig = fsl.FindTheBiggest(in_files=ldir, out_file='biggestSegmentation')
>>> fBig.cmdline
'find_the_biggest seeds_to_M1.nii seeds_to_M2.nii biggestSegmentation'

Inputs::

        [Mandatory]
        in_files: (a list of items which are an existing file name)
                a list of input volumes or a singleMatrixFile
                flag: %s, position: 0
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
        out_file: (a file name)
                file with the resulting segmentation
                flag: %s, position: 2
        output_type: ('NIFTI_PAIR' or 'NIFTI_PAIR_GZ' or 'NIFTI_GZ' or
                 'NIFTI')
                FSL output type

Outputs::

        out_file: (an existing file name)
                output file indexed in order of input files
                flag: %s

.. _nipype.interfaces.fsl.dti.MakeDyadicVectors:


.. index:: MakeDyadicVectors

MakeDyadicVectors
-----------------

`Link to code <http://github.com/nipy/nipype/tree/e63e055194d62d2bdc4665688261c03a42fd0025/nipype/interfaces/fsl/dti.py#L1295>`__

Wraps command **make_dyadic_vectors**

Create vector volume representing mean principal diffusion direction
and its uncertainty (dispersion)

Inputs::

        [Mandatory]
        phi_vol: (an existing file name)
                flag: %s, position: 1
        terminal_output: ('stream' or 'allatonce' or 'file' or 'none')
                Control terminal output: `stream` - displays to terminal
                immediately, `allatonce` - waits till command is finished to display
                output, `file` - writes output to file, `none` - output is ignored
        theta_vol: (an existing file name)
                flag: %s, position: 0

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
        mask: (an existing file name)
                flag: %s, position: 2
        output: (a file name, nipype default value: dyads)
                flag: %s, position: 3
        output_type: ('NIFTI_PAIR' or 'NIFTI_PAIR_GZ' or 'NIFTI_GZ' or
                 'NIFTI')
                FSL output type
        perc: (a float)
                the {perc}% angle of the output cone of uncertainty (output will be
                in degrees)
                flag: %f, position: 4

Outputs::

        dispersion: (an existing file name)
        dyads: (an existing file name)

.. _nipype.interfaces.fsl.dti.ProbTrackX:


.. index:: ProbTrackX

ProbTrackX
----------

`Link to code <http://github.com/nipy/nipype/tree/e63e055194d62d2bdc4665688261c03a42fd0025/nipype/interfaces/fsl/dti.py#L736>`__

Wraps command **probtrackx**

Use FSL  probtrackx for tractography on bedpostx results

Examples
~~~~~~~~

>>> from nipype.interfaces import fsl
>>> pbx = fsl.ProbTrackX(samples_base_name='merged', mask='mask.nii',     seed='MASK_average_thal_right.nii', mode='seedmask',     xfm='trans.mat', n_samples=3, n_steps=10, force_dir=True, opd=True, os2t=True,     target_masks = ['targets_MASK1.nii', 'targets_MASK2.nii'],     thsamples='merged_thsamples.nii', fsamples='merged_fsamples.nii', phsamples='merged_phsamples.nii',     out_dir='.')
>>> pbx.cmdline
'probtrackx --forcedir -m mask.nii --mode=seedmask --nsamples=3 --nsteps=10 --opd --os2t --dir=. --samples=merged --seed=MASK_average_thal_right.nii --targetmasks=targets.txt --xfm=trans.mat'

Inputs::

        [Mandatory]
        fsamples: (an existing file name)
        mask: (an existing file name)
                bet binary mask file in diffusion space
                flag: -m %s
        phsamples: (an existing file name)
        seed: (an existing file name or a list of items which are an existing
                 file name or a list of items which are a list of from 3 to 3 items
                 which are an integer)
                seed volume(s), or voxel(s)or freesurfer label file
                flag: --seed=%s
        terminal_output: ('stream' or 'allatonce' or 'file' or 'none')
                Control terminal output: `stream` - displays to terminal
                immediately, `allatonce` - waits till command is finished to display
                output, `file` - writes output to file, `none` - output is ignored
        thsamples: (an existing file name)

        [Optional]
        args: (a string)
                Additional parameters to the command
                flag: %s
        avoid_mp: (an existing file name)
                reject pathways passing through locations given by this mask
                flag: --avoid=%s
        c_thresh: (a float)
                curvature threshold - default=0.2
                flag: --cthr=%.3f
        correct_path_distribution: (a boolean)
                correct path distribution for the length of the pathways
                flag: --pd
        dist_thresh: (a float)
                discards samples shorter than this threshold (in mm - default=0)
                flag: --distthresh=%.3f
        environ: (a dictionary with keys which are a value of type 'str' and
                 with values which are a value of type 'str', nipype default value:
                 {})
                Environment variables
        fibst: (an integer)
                force a starting fibre for tracking - default=1, i.e. first fibre
                orientation. Only works if randfib==0
                flag: --fibst=%d
        force_dir: (a boolean, nipype default value: True)
                use the actual directory name given - i.e. do not add + to make a
                new directory
                flag: --forcedir
        ignore_exception: (a boolean, nipype default value: False)
                Print an error message instead of throwing an exception in case the
                interface fails to run
        inv_xfm: (a file name)
                transformation matrix taking DTI space to seed space (compulsory
                when using a warp_field for seeds_to_dti)
                flag: --invxfm=%s
        loop_check: (a boolean)
                perform loop_checks on paths - slower, but allows lower curvature
                threshold
                flag: --loopcheck
        mask2: (an existing file name)
                second bet binary mask (in diffusion space) in twomask_symm mode
                flag: --mask2=%s
        mesh: (an existing file name)
                Freesurfer-type surface descriptor (in ascii format)
                flag: --mesh=%s
        mod_euler: (a boolean)
                use modified euler streamlining
                flag: --modeuler
        mode: ('simple' or 'two_mask_symm' or 'seedmask')
                options: simple (single seed voxel), seedmask (mask of seed voxels),
                twomask_symm (two bet binary masks)
                flag: --mode=%s
        n_samples: (an integer, nipype default value: 5000)
                number of samples - default=5000
                flag: --nsamples=%d
        n_steps: (an integer)
                number of steps per sample - default=2000
                flag: --nsteps=%d
        network: (a boolean)
                activate network mode - only keep paths going through at least one
                seed mask (required if multiple seed masks)
                flag: --network
        opd: (a boolean, nipype default value: True)
                outputs path distributions
                flag: --opd
        os2t: (a boolean)
                Outputs seeds to targets
                flag: --os2t
        out_dir: (an existing directory name)
                directory to put the final volumes in
                flag: --dir=%s
        output_type: ('NIFTI_PAIR' or 'NIFTI_PAIR_GZ' or 'NIFTI_GZ' or
                 'NIFTI')
                FSL output type
        rand_fib: (0 or 1 or 2 or 3)
                options: 0 - default, 1 - to randomly sample initial fibres (with f
                > fibthresh), 2 - to sample in proportion fibres (with f>fibthresh)
                to f, 3 - to sample ALL populations at random (even if f<fibthresh)
                flag: --randfib=%d
        random_seed: (a boolean)
                random seed
                flag: --rseed
        s2tastext: (a boolean)
                output seed-to-target counts as a text file (useful when seeding
                from a mesh)
                flag: --s2tastext
        sample_random_points: (a boolean)
                sample random points within seed voxels
                flag: --sampvox
        samples_base_name: (a string, nipype default value: merged)
                the rootname/base_name for samples files
                flag: --samples=%s
        seed_ref: (an existing file name)
                reference vol to define seed space in simple mode - diffusion space
                assumed if absent
                flag: --seedref=%s
        step_length: (a float)
                step_length in mm - default=0.5
                flag: --steplength=%.3f
        stop_mask: (an existing file name)
                stop tracking at locations given by this mask file
                flag: --stop=%s
        target_masks: (a file name)
                list of target masks - required for seeds_to_targets classification
                flag: --targetmasks=%s
        use_anisotropy: (a boolean)
                use anisotropy to constrain tracking
                flag: --usef
        verbose: (0 or 1 or 2)
                Verbose level, [0-2].Level 2 is required to output particle files.
                flag: --verbose=%d
        waypoints: (an existing file name)
                waypoint mask or ascii list of waypoint masks - only keep paths
                going through ALL the masks
                flag: --waypoints=%s
        xfm: (an existing file name)
                transformation matrix taking seed space to DTI space (either FLIRT
                matrix or FNIRT warp_field) - default is identity
                flag: --xfm=%s

Outputs::

        fdt_paths: (an existing file name)
                path/name of a 3D image file containing the output connectivity
                distribution to the seed mask
        log: (an existing file name)
                path/name of a text record of the command that was run
        particle_files: (a list of items which are an existing file name)
                Files describing all of the tract samples. Generated only if verbose
                is set to 2
        targets: (a list of items which are an existing file name)
                a list with all generated seeds_to_target files
        way_total: (an existing file name)
                path/name of a text file containing a single number corresponding to
                the total number of generated tracts that have not been rejected by
                inclusion/exclusion mask criteria

.. _nipype.interfaces.fsl.dti.ProbTrackX2:


.. index:: ProbTrackX2

ProbTrackX2
-----------

`Link to code <http://github.com/nipy/nipype/tree/e63e055194d62d2bdc4665688261c03a42fd0025/nipype/interfaces/fsl/dti.py#L897>`__

Wraps command **probtrackx2**

Use FSL  probtrackx2 for tractography on bedpostx results

Examples
~~~~~~~~

>>> from nipype.interfaces import fsl
>>> pbx2 = fsl.ProbTrackX2()
>>> pbx2.inputs.seed = 'seed_source.nii.gz'
>>> pbx2.inputs.thsamples = 'merged_th1samples.nii.gz'
>>> pbx2.inputs.fsamples = 'merged_f1samples.nii.gz'
>>> pbx2.inputs.phsamples = 'merged_ph1samples.nii.gz'
>>> pbx2.inputs.mask = 'nodif_brain_mask.nii.gz'
>>> pbx2.inputs.out_dir = '.'
>>> pbx2.inputs.n_samples = 3
>>> pbx2.inputs.n_steps = 10
>>> pbx2.cmdline
'probtrackx2 --forcedir -m nodif_brain_mask.nii.gz --nsamples=3 --nsteps=10 --opd --dir=. --samples=merged --seed=seed_source.nii.gz'

Inputs::

        [Mandatory]
        fsamples: (an existing file name)
        mask: (an existing file name)
                bet binary mask file in diffusion space
                flag: -m %s
        phsamples: (an existing file name)
        seed: (an existing file name or a list of items which are an existing
                 file name or a list of items which are a list of from 3 to 3 items
                 which are an integer)
                seed volume(s), or voxel(s)or freesurfer label file
                flag: --seed=%s
        terminal_output: ('stream' or 'allatonce' or 'file' or 'none')
                Control terminal output: `stream` - displays to terminal
                immediately, `allatonce` - waits till command is finished to display
                output, `file` - writes output to file, `none` - output is ignored
        thsamples: (an existing file name)

        [Optional]
        args: (a string)
                Additional parameters to the command
                flag: %s
        avoid_mp: (an existing file name)
                reject pathways passing through locations given by this mask
                flag: --avoid=%s
        c_thresh: (a float)
                curvature threshold - default=0.2
                flag: --cthr=%.3f
        colmask4: (an existing file name)
                Mask for columns of matrix4 (default=seed mask)
                flag: --colmask4=%s
        correct_path_distribution: (a boolean)
                correct path distribution for the length of the pathways
                flag: --pd
        dist_thresh: (a float)
                discards samples shorter than this threshold (in mm - default=0)
                flag: --distthresh=%.3f
        distthresh1: (a float)
                Discards samples (in matrix1) shorter than this threshold (in mm -
                default=0)
                flag: --distthresh1=%.3f
        distthresh3: (a float)
                Discards samples (in matrix3) shorter than this threshold (in mm -
                default=0)
                flag: --distthresh3=%.3f
        environ: (a dictionary with keys which are a value of type 'str' and
                 with values which are a value of type 'str', nipype default value:
                 {})
                Environment variables
        fibst: (an integer)
                force a starting fibre for tracking - default=1, i.e. first fibre
                orientation. Only works if randfib==0
                flag: --fibst=%d
        fopd: (an existing file name)
                Other mask for binning tract distribution
                flag: --fopd=%s
        force_dir: (a boolean, nipype default value: True)
                use the actual directory name given - i.e. do not add + to make a
                new directory
                flag: --forcedir
        ignore_exception: (a boolean, nipype default value: False)
                Print an error message instead of throwing an exception in case the
                interface fails to run
        inv_xfm: (a file name)
                transformation matrix taking DTI space to seed space (compulsory
                when using a warp_field for seeds_to_dti)
                flag: --invxfm=%s
        loop_check: (a boolean)
                perform loop_checks on paths - slower, but allows lower curvature
                threshold
                flag: --loopcheck
        lrtarget3: (an existing file name)
                Column-space mask used for Nxn connectivity matrix
                flag: --lrtarget3=%s
        meshspace: ('caret' or 'freesurfer' or 'first' or 'vox')
                Mesh reference space - either "caret" (default) or "freesurfer" or
                "first" or "vox"
                flag: --meshspace=%s
        mod_euler: (a boolean)
                use modified euler streamlining
                flag: --modeuler
        n_samples: (an integer, nipype default value: 5000)
                number of samples - default=5000
                flag: --nsamples=%d
        n_steps: (an integer)
                number of steps per sample - default=2000
                flag: --nsteps=%d
        network: (a boolean)
                activate network mode - only keep paths going through at least one
                seed mask (required if multiple seed masks)
                flag: --network
        omatrix1: (a boolean)
                Output matrix1 - SeedToSeed Connectivity
                flag: --omatrix1
        omatrix2: (a boolean)
                Output matrix2 - SeedToLowResMask
                flag: --omatrix2
                requires: target2
        omatrix3: (a boolean)
                Output matrix3 (NxN connectivity matrix)
                flag: --omatrix3
                requires: target3, lrtarget3
        omatrix4: (a boolean)
                Output matrix4 - DtiMaskToSeed (special Oxford Sparse Format)
                flag: --omatrix4
        onewaycondition: (a boolean)
                Apply waypoint conditions to each half tract separately
                flag: --onewaycondition
        opd: (a boolean, nipype default value: True)
                outputs path distributions
                flag: --opd
        os2t: (a boolean)
                Outputs seeds to targets
                flag: --os2t
        out_dir: (an existing directory name)
                directory to put the final volumes in
                flag: --dir=%s
        output_type: ('NIFTI_PAIR' or 'NIFTI_PAIR_GZ' or 'NIFTI_GZ' or
                 'NIFTI')
                FSL output type
        rand_fib: (0 or 1 or 2 or 3)
                options: 0 - default, 1 - to randomly sample initial fibres (with f
                > fibthresh), 2 - to sample in proportion fibres (with f>fibthresh)
                to f, 3 - to sample ALL populations at random (even if f<fibthresh)
                flag: --randfib=%d
        random_seed: (a boolean)
                random seed
                flag: --rseed
        s2tastext: (a boolean)
                output seed-to-target counts as a text file (useful when seeding
                from a mesh)
                flag: --s2tastext
        sample_random_points: (a boolean)
                sample random points within seed voxels
                flag: --sampvox
        samples_base_name: (a string, nipype default value: merged)
                the rootname/base_name for samples files
                flag: --samples=%s
        seed_ref: (an existing file name)
                reference vol to define seed space in simple mode - diffusion space
                assumed if absent
                flag: --seedref=%s
        simple: (a boolean)
                rack from a list of voxels (seed must be a ASCII list of
                coordinates)
                flag: --simple
        step_length: (a float)
                step_length in mm - default=0.5
                flag: --steplength=%.3f
        stop_mask: (an existing file name)
                stop tracking at locations given by this mask file
                flag: --stop=%s
        target2: (an existing file name)
                Low resolution binary brain mask for storing connectivity
                distribution in matrix2 mode
                flag: --target2=%s
        target3: (an existing file name)
                Mask used for NxN connectivity matrix (or Nxn if lrtarget3 is set)
                flag: --target3=%s
        target4: (an existing file name)
                Brain mask in DTI space
                flag: --target4=%s
        target_masks: (a file name)
                list of target masks - required for seeds_to_targets classification
                flag: --targetmasks=%s
        use_anisotropy: (a boolean)
                use anisotropy to constrain tracking
                flag: --usef
        verbose: (0 or 1 or 2)
                Verbose level, [0-2].Level 2 is required to output particle files.
                flag: --verbose=%d
        waycond: ('OR' or 'AND')
                Waypoint condition. Either "AND" (default) or "OR"
                flag: --waycond=%s
        wayorder: (a boolean)
                Reject streamlines that do not hit waypoints in given order. Only
                valid if waycond=AND
                flag: --wayorder
        waypoints: (an existing file name)
                waypoint mask or ascii list of waypoint masks - only keep paths
                going through ALL the masks
                flag: --waypoints=%s
        xfm: (an existing file name)
                transformation matrix taking seed space to DTI space (either FLIRT
                matrix or FNIRT warp_field) - default is identity
                flag: --xfm=%s

Outputs::

        fdt_paths: (an existing file name)
                path/name of a 3D image file containing the output connectivity
                distribution to the seed mask
        log: (an existing file name)
                path/name of a text record of the command that was run
        lookup_tractspace: (an existing file name)
                lookup_tractspace generated by --omatrix2 option
        matrix1_dot: (an existing file name)
                Output matrix1.dot - SeedToSeed Connectivity
        matrix2_dot: (an existing file name)
                Output matrix2.dot - SeedToLowResMask
        matrix3_dot: (an existing file name)
                Output matrix3 - NxN connectivity matrix
        network_matrix: (an existing file name)
                the network matrix generated by --omatrix1 option
        particle_files: (a list of items which are an existing file name)
                Files describing all of the tract samples. Generated only if verbose
                is set to 2
        targets: (a list of items which are an existing file name)
                a list with all generated seeds_to_target files
        way_total: (an existing file name)
                path/name of a text file containing a single number corresponding to
                the total number of generated tracts that have not been rejected by
                inclusion/exclusion mask criteria

.. _nipype.interfaces.fsl.dti.ProjThresh:


.. index:: ProjThresh

ProjThresh
----------

`Link to code <http://github.com/nipy/nipype/tree/e63e055194d62d2bdc4665688261c03a42fd0025/nipype/interfaces/fsl/dti.py#L1031>`__

Wraps command **proj_thresh**

Use FSL proj_thresh for thresholding some outputs of probtrack
For complete details, see the FDT Documentation
<http://www.fmrib.ox.ac.uk/fsl/fdt/fdt_thresh.html>

Example
~~~~~~~

>>> from nipype.interfaces import fsl
>>> ldir = ['seeds_to_M1.nii', 'seeds_to_M2.nii']
>>> pThresh = fsl.ProjThresh(in_files=ldir, threshold=3)
>>> pThresh.cmdline
'proj_thresh seeds_to_M1.nii seeds_to_M2.nii 3'

Inputs::

        [Mandatory]
        in_files: (a list of items which are an existing file name)
                a list of input volumes
                flag: %s, position: 0
        terminal_output: ('stream' or 'allatonce' or 'file' or 'none')
                Control terminal output: `stream` - displays to terminal
                immediately, `allatonce` - waits till command is finished to display
                output, `file` - writes output to file, `none` - output is ignored
        threshold: (an integer)
                threshold indicating minimum number of seed voxels entering this
                mask region
                flag: %d, position: 1

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
        output_type: ('NIFTI_PAIR' or 'NIFTI_PAIR_GZ' or 'NIFTI_GZ' or
                 'NIFTI')
                FSL output type

Outputs::

        out_files: (a list of items which are an existing file name)
                path/name of output volume after thresholding

.. _nipype.interfaces.fsl.dti.TractSkeleton:


.. index:: TractSkeleton

TractSkeleton
-------------

`Link to code <http://github.com/nipy/nipype/tree/e63e055194d62d2bdc4665688261c03a42fd0025/nipype/interfaces/fsl/dti.py#L1142>`__

Wraps command **tbss_skeleton**

Use FSL's tbss_skeleton to skeletonise an FA image or project arbitrary values onto a skeleton.

There are two ways to use this interface.  To create a skeleton from an FA image, just
supply the ``in_file`` and set ``skeleton_file`` to True (or specify a skeleton filename.
To project values onto a skeleton, you must set ``project_data`` to True, and then also
supply values for ``threshold``, ``distance_map``, and ``data_file``. The ``search_mask_file``
and ``use_cingulum_mask`` inputs are also used in data projection, but ``use_cingulum_mask``
is set to True by default.  This mask controls where the projection algorithm searches
within a circular space around a tract, rather than in a single perpindicular direction.

Example
~~~~~~~

>>> import nipype.interfaces.fsl as fsl
>>> skeletor = fsl.TractSkeleton()
>>> skeletor.inputs.in_file = "all_FA.nii.gz"
>>> skeletor.inputs.skeleton_file = True
>>> skeletor.run() # doctest: +SKIP

Inputs::

        [Mandatory]
        in_file: (an existing file name)
                input image (typcially mean FA volume)
                flag: -i %s
        terminal_output: ('stream' or 'allatonce' or 'file' or 'none')
                Control terminal output: `stream` - displays to terminal
                immediately, `allatonce` - waits till command is finished to display
                output, `file` - writes output to file, `none` - output is ignored

        [Optional]
        alt_data_file: (an existing file name)
                4D non-FA data to project onto skeleton
                flag: -a %s
        alt_skeleton: (an existing file name)
                alternate skeleton to use
                flag: -s %s
        args: (a string)
                Additional parameters to the command
                flag: %s
        data_file: (an existing file name)
                4D data to project onto skeleton (usually FA)
        distance_map: (an existing file name)
                distance map image
        environ: (a dictionary with keys which are a value of type 'str' and
                 with values which are a value of type 'str', nipype default value:
                 {})
                Environment variables
        ignore_exception: (a boolean, nipype default value: False)
                Print an error message instead of throwing an exception in case the
                interface fails to run
        output_type: ('NIFTI_PAIR' or 'NIFTI_PAIR_GZ' or 'NIFTI_GZ' or
                 'NIFTI')
                FSL output type
        project_data: (a boolean)
                project data onto skeleton
                flag: -p %.3f %s %s %s %s
                requires: threshold, distance_map, data_file
        projected_data: (a file name)
                input data projected onto skeleton
        search_mask_file: (an existing file name)
                mask in which to use alternate search rule
                mutually_exclusive: use_cingulum_mask
        skeleton_file: (a boolean or a file name)
                write out skeleton image
                flag: -o %s
        threshold: (a float)
                skeleton threshold value
        use_cingulum_mask: (a boolean, nipype default value: True)
                perform alternate search using built-in cingulum mask
                mutually_exclusive: search_mask_file

Outputs::

        projected_data: (a file name)
                input data projected onto skeleton
        skeleton_file: (a file name)
                tract skeleton image

.. _nipype.interfaces.fsl.dti.VecReg:


.. index:: VecReg

VecReg
------

`Link to code <http://github.com/nipy/nipype/tree/e63e055194d62d2bdc4665688261c03a42fd0025/nipype/interfaces/fsl/dti.py#L972>`__

Wraps command **vecreg**

Use FSL vecreg for registering vector data
For complete details, see the FDT Documentation
<http://www.fmrib.ox.ac.uk/fsl/fdt/fdt_vecreg.html>

Example
~~~~~~~

>>> from nipype.interfaces import fsl
>>> vreg = fsl.VecReg(in_file='diffusion.nii',                  affine_mat='trans.mat',                  ref_vol='mni.nii',                  out_file='diffusion_vreg.nii')
>>> vreg.cmdline
'vecreg -t trans.mat -i diffusion.nii -o diffusion_vreg.nii -r mni.nii'

Inputs::

        [Mandatory]
        in_file: (an existing file name)
                filename for input vector or tensor field
                flag: -i %s
        ref_vol: (an existing file name)
                filename for reference (target) volume
                flag: -r %s
        terminal_output: ('stream' or 'allatonce' or 'file' or 'none')
                Control terminal output: `stream` - displays to terminal
                immediately, `allatonce` - waits till command is finished to display
                output, `file` - writes output to file, `none` - output is ignored

        [Optional]
        affine_mat: (an existing file name)
                filename for affine transformation matrix
                flag: -t %s
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
        interpolation: ('nearestneighbour' or 'trilinear' or 'sinc' or
                 'spline')
                interpolation method : nearestneighbour, trilinear (default), sinc
                or spline
                flag: --interp=%s
        mask: (an existing file name)
                brain mask in input space
                flag: -m %s
        out_file: (a file name)
                filename for output registered vector or tensor field
                flag: -o %s
        output_type: ('NIFTI_PAIR' or 'NIFTI_PAIR_GZ' or 'NIFTI_GZ' or
                 'NIFTI')
                FSL output type
        ref_mask: (an existing file name)
                brain mask in output space (useful for speed up of nonlinear reg)
                flag: --refmask=%s
        rotation_mat: (an existing file name)
                filename for secondary affine matrixif set, this will be used for
                the rotation of the vector/tensor field
                flag: --rotmat=%s
        rotation_warp: (an existing file name)
                filename for secondary warp fieldif set, this will be used for the
                rotation of the vector/tensor field
                flag: --rotwarp=%s
        warp_field: (an existing file name)
                filename for 4D warp field for nonlinear registration
                flag: -w %s

Outputs::

        out_file: (an existing file name)
                path/name of filename for the registered vector or tensor field

.. _nipype.interfaces.fsl.dti.XFibres:


.. index:: XFibres

XFibres
-------

`Link to code <http://github.com/nipy/nipype/tree/e63e055194d62d2bdc4665688261c03a42fd0025/nipype/interfaces/fsl/dti.py#L634>`__

Wraps command **xfibres**


Inputs::

        [Mandatory]
        bvals: (an existing file name)
                b values file
                flag: --bvals=%s
        bvecs: (an existing file name)
                b vectors file
                flag: --bvecs=%s
        dwi: (an existing file name)
                diffusion weighted image data file
                flag: --data=%s
        mask: (an existing file name)
                brain binary mask file (i.e. from BET)
                flag: --mask=%s
        terminal_output: ('stream' or 'allatonce' or 'file' or 'none')
                Control terminal output: `stream` - displays to terminal
                immediately, `allatonce` - waits till command is finished to display
                output, `file` - writes output to file, `none` - output is ignored

        [Optional]
        all_ard: (a boolean)
                Turn ARD on on all fibres
                flag: --allard
                mutually_exclusive: no_ard, all_ard
        args: (a string)
                Additional parameters to the command
                flag: %s
        burn_in: (an integer >= 0)
                Total num of jumps at start of MCMC to be discarded
                flag: --burnin=%d
        burn_in_no_ard: (an integer >= 0)
                num of burnin jumps before the ard is imposed
                flag: --burninnoard=%d
        cnlinear: (a boolean)
                Initialise with constrained nonlinear fitting
                flag: --cnonlinear
                mutually_exclusive: no_spat, non_linear, cnlinear
        environ: (a dictionary with keys which are a value of type 'str' and
                 with values which are a value of type 'str', nipype default value:
                 {})
                Environment variables
        f0_ard: (a boolean)
                Noise floor model: add to the model an unattenuated signal
                compartment f0
                flag: --f0 --ardf0
                mutually_exclusive: f0_noard, f0_ard, all_ard
        f0_noard: (a boolean)
                Noise floor model: add to the model an unattenuated signal
                compartment f0
                flag: --f0
                mutually_exclusive: f0_noard, f0_ard
        force_dir: (a boolean, nipype default value: True)
                use the actual directory name given (do not add + to make a new
                directory)
                flag: --forcedir
        fudge: (an integer)
                ARD fudge factor
                flag: --fudge=%d
        gradnonlin: (an existing file name)
                gradient file corresponding to slice
                flag: --gradnonlin=%s
        ignore_exception: (a boolean, nipype default value: False)
                Print an error message instead of throwing an exception in case the
                interface fails to run
        logdir: (a directory name, nipype default value: .)
                flag: --logdir=%s
        model: (1 or 2)
                use monoexponential (1, default, required for single-shell) or
                multiexponential (2, multi-shell) model
                flag: --model=%d
        n_fibres: (an integer >= 1)
                Maximum number of fibres to fit in each voxel
                flag: --nfibres=%d
        n_jumps: (an integer)
                Num of jumps to be made by MCMC
                flag: --njumps=%d
        no_ard: (a boolean)
                Turn ARD off on all fibres
                flag: --noard
                mutually_exclusive: no_ard, all_ard
        no_spat: (a boolean)
                Initialise with tensor, not spatially
                flag: --nospat
                mutually_exclusive: no_spat, non_linear, cnlinear
        non_linear: (a boolean)
                Initialise with nonlinear fitting
                flag: --nonlinear
                mutually_exclusive: no_spat, non_linear, cnlinear
        output_type: ('NIFTI_PAIR' or 'NIFTI_PAIR_GZ' or 'NIFTI_GZ' or
                 'NIFTI')
                FSL output type
        rician: (a boolean)
                use Rician noise modeling
                flag: --rician
        sample_every: (an integer >= 0)
                Num of jumps for each sample (MCMC)
                flag: --sampleevery=%d
        seed: (an integer)
                seed for pseudo random number generator
                flag: --seed=%d
        update_proposal_every: (an integer >= 1)
                Num of jumps for each update to the proposal density std (MCMC)
                flag: --updateproposalevery=%d

Outputs::

        d_stdsamples: (a file name)
                Std of samples from the distribution d
        dsamples: (a file name)
                Samples from the distribution on diffusivity d
        dyads: (a file name)
                Mean of PDD distribution in vector form.
        fsamples: (a file name)
                Samples from the distribution on f anisotropy
        mean_S0samples: (a file name)
                Mean of distribution on T2wbaseline signal intensity S0
        mean_d_stdsamples: (a file name)
                Mean of distribution on diffusivity d
        mean_dsamples: (a file name)
                Mean of distribution on diffusivity d
        mean_fsamples: (a file name)
                Mean of distribution on f anisotropy
        mean_tausamples: (a file name)
                Mean of distribution on tau samples (only with rician noise)
        phsamples: (a file name)
                phi samples, per fiber
        thsamples: (a file name)
                theta samples, per fiber

.. _nipype.interfaces.fsl.dti.XFibres4:


.. index:: XFibres4

XFibres4
--------

`Link to code <http://github.com/nipy/nipype/tree/e63e055194d62d2bdc4665688261c03a42fd0025/nipype/interfaces/fsl/dti.py#L434>`__

Wraps command **xfibres**

Perform model parameters estimation for local (voxelwise) diffusion
parameters

.. deprecated:: 0.9.2
  Use :class:`.XFibres5` instead.

Inputs::

        [Mandatory]
        bvals: (an existing file name)
                flag: --bvals=%s
        bvecs: (an existing file name)
                flag: --bvecs=%s
        dwi: (an existing file name)
                flag: --data=%s
        mask: (an existing file name)
                flag: --mask=%s
        terminal_output: ('stream' or 'allatonce' or 'file' or 'none')
                Control terminal output: `stream` - displays to terminal
                immediately, `allatonce` - waits till command is finished to display
                output, `file` - writes output to file, `none` - output is ignored

        [Optional]
        all_ard: (a boolean)
                Turn ARD on on all fibres
                flag: --allard
                mutually_exclusive: no_ard, all_ard
        args: (a string)
                Additional parameters to the command
                flag: %s
        burn_in: (an integer >= 0)
                Total num of jumps at start of MCMC to be discarded
                flag: --burnin=%d
        burn_in_no_ard: (an integer >= 0)
                num of burnin jumps before the ard is imposed
                flag: --burninnoard=%d
        environ: (a dictionary with keys which are a value of type 'str' and
                 with values which are a value of type 'str', nipype default value:
                 {})
                Environment variables
        force_dir: (a boolean, nipype default value: True)
                use the actual directory name given - i.e. do not add + to make a
                new directory
                flag: --forcedir
        fudge: (an integer)
                ARD fudge factor
                flag: --fudge=%d
        gradnonlin: (an existing file name)
                flag: --gradnonlin=%s
        ignore_exception: (a boolean, nipype default value: False)
                Print an error message instead of throwing an exception in case the
                interface fails to run
        logdir: (a directory name, nipype default value: logdir)
                flag: --logdir=%s
        model: (an integer)
                Which model to use. 1=mono-exponential (default and required for
                single shell). 2=continous exponential (for multi-shell experiments)
                flag: --model=%d
        n_fibres: (an integer >= 1)
                Maximum nukmber of fibres to fit in each voxel
                flag: --nfibres=%d
        n_jumps: (an integer >= 1)
                Num of jumps to be made by MCMC
                flag: --njumps=%d
        no_ard: (a boolean)
                Turn ARD off on all fibres
                flag: --noard
                mutually_exclusive: no_ard, all_ard
        no_spat: (a boolean)
                Initialise with tensor, not spatially
                flag: --nospat
                mutually_exclusive: no_spat, non_linear
        non_linear: (a boolean)
                Initialise with nonlinear fitting
                flag: --nonlinear
                mutually_exclusive: no_spat, non_linear
        output_type: ('NIFTI_PAIR' or 'NIFTI_PAIR_GZ' or 'NIFTI_GZ' or
                 'NIFTI')
                FSL output type
        sample_every: (an integer >= 0)
                Num of jumps for each sample (MCMC)
                flag: --sampleevery=%d
        seed: (an integer)
                seed for pseudo random number generator
                flag: --seed=%d
        update_proposal_every: (an integer >= 1)
                Num of jumps for each update to the proposal density std (MCMC)
                flag: --updateproposalevery=%d

Outputs::

        dyads: (an existing file name)
                Mean of PDD distribution in vector form.
        fsamples: (an existing file name)
                Samples from the distribution on anisotropic volume fraction
        mean_S0samples: (an existing file name)
                Samples from S0 distribution
        mean_dsamples: (an existing file name)
                Mean of distribution on diffusivity d
        mean_fsamples: (an existing file name)
                Mean of distribution on f anisotropy
        phsamples: (an existing file name)
                Samples from the distribution on phi
        thsamples: (an existing file name)
                Samples from the distribution on theta

.. _nipype.interfaces.fsl.dti.XFibres5:


.. index:: XFibres5

XFibres5
--------

`Link to code <http://github.com/nipy/nipype/tree/e63e055194d62d2bdc4665688261c03a42fd0025/nipype/interfaces/fsl/dti.py#L375>`__

Wraps command **xfibres**

Perform model parameters estimation for local (voxelwise) diffusion
parameters

Inputs::

        [Mandatory]
        bvals: (an existing file name)
                b values file
                flag: --bvals=%s
        bvecs: (an existing file name)
                b vectors file
                flag: --bvecs=%s
        dwi: (an existing file name)
                diffusion weighted image data file
                flag: --data=%s
        mask: (an existing file name)
                brain binary mask file (i.e. from BET)
                flag: --mask=%s
        terminal_output: ('stream' or 'allatonce' or 'file' or 'none')
                Control terminal output: `stream` - displays to terminal
                immediately, `allatonce` - waits till command is finished to display
                output, `file` - writes output to file, `none` - output is ignored

        [Optional]
        all_ard: (a boolean)
                Turn ARD on on all fibres
                flag: --allard
                mutually_exclusive: no_ard, all_ard
        args: (a string)
                Additional parameters to the command
                flag: %s
        burn_in: (an integer >= 0)
                Total num of jumps at start of MCMC to be discarded
                flag: --burnin=%d
        burn_in_no_ard: (an integer >= 0)
                num of burnin jumps before the ard is imposed
                flag: --burninnoard=%d
        cnlinear: (a boolean)
                Initialise with constrained nonlinear fitting
                flag: --cnonlinear
                mutually_exclusive: no_spat, non_linear, cnlinear
        environ: (a dictionary with keys which are a value of type 'str' and
                 with values which are a value of type 'str', nipype default value:
                 {})
                Environment variables
        f0_ard: (a boolean)
                Noise floor model: add to the model an unattenuated signal
                compartment f0
                flag: --f0 --ardf0
                mutually_exclusive: f0_noard, f0_ard, all_ard
        f0_noard: (a boolean)
                Noise floor model: add to the model an unattenuated signal
                compartment f0
                flag: --f0
                mutually_exclusive: f0_noard, f0_ard
        force_dir: (a boolean, nipype default value: True)
                use the actual directory name given (do not add + to make a new
                directory)
                flag: --forcedir
        fudge: (an integer)
                ARD fudge factor
                flag: --fudge=%d
        gradnonlin: (an existing file name)
                gradient file corresponding to slice
                flag: --gradnonlin=%s
        ignore_exception: (a boolean, nipype default value: False)
                Print an error message instead of throwing an exception in case the
                interface fails to run
        logdir: (a directory name, nipype default value: .)
                flag: --logdir=%s
        model: (1 or 2)
                use monoexponential (1, default, required for single-shell) or
                multiexponential (2, multi-shell) model
                flag: --model=%d
        n_fibres: (an integer >= 1)
                Maximum number of fibres to fit in each voxel
                flag: --nfibres=%d
        n_jumps: (an integer)
                Num of jumps to be made by MCMC
                flag: --njumps=%d
        no_ard: (a boolean)
                Turn ARD off on all fibres
                flag: --noard
                mutually_exclusive: no_ard, all_ard
        no_spat: (a boolean)
                Initialise with tensor, not spatially
                flag: --nospat
                mutually_exclusive: no_spat, non_linear, cnlinear
        non_linear: (a boolean)
                Initialise with nonlinear fitting
                flag: --nonlinear
                mutually_exclusive: no_spat, non_linear, cnlinear
        output_type: ('NIFTI_PAIR' or 'NIFTI_PAIR_GZ' or 'NIFTI_GZ' or
                 'NIFTI')
                FSL output type
        rician: (a boolean)
                use Rician noise modeling
                flag: --rician
        sample_every: (an integer >= 0)
                Num of jumps for each sample (MCMC)
                flag: --sampleevery=%d
        seed: (an integer)
                seed for pseudo random number generator
                flag: --seed=%d
        update_proposal_every: (an integer >= 1)
                Num of jumps for each update to the proposal density std (MCMC)
                flag: --updateproposalevery=%d

Outputs::

        d_stdsamples: (a file name)
                Std of samples from the distribution d
        dsamples: (a file name)
                Samples from the distribution on diffusivity d
        dyads: (a file name)
                Mean of PDD distribution in vector form.
        fsamples: (a file name)
                Samples from the distribution on f anisotropy
        mean_S0samples: (a file name)
                Mean of distribution on T2wbaseline signal intensity S0
        mean_d_stdsamples: (a file name)
                Mean of distribution on diffusivity d
        mean_dsamples: (a file name)
                Mean of distribution on diffusivity d
        mean_fsamples: (a file name)
                Mean of distribution on f anisotropy
        mean_tausamples: (a file name)
                Mean of distribution on tau samples (only with rician noise)
        phsamples: (a file name)
                phi samples, per fiber
        thsamples: (a file name)
                theta samples, per fiber
