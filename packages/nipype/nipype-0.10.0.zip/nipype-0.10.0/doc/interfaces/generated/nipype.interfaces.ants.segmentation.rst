.. AUTO-GENERATED FILE -- DO NOT EDIT!

interfaces.ants.segmentation
============================


.. _nipype.interfaces.ants.segmentation.Atropos:


.. index:: Atropos

Atropos
-------

`Link to code <http://github.com/nipy/nipype/tree/e63e055194d62d2bdc4665688261c03a42fd0025/nipype/interfaces/ants/segmentation.py#L57>`__

Wraps command **Atropos**

A finite mixture modeling (FMM) segmentation approach with possibilities for
specifying prior constraints. These prior constraints include the specification
of a prior label image, prior probability images (one for each class), and/or an
MRF prior to enforce spatial smoothing of the labels. Similar algorithms include
FAST and SPM.

Examples
~~~~~~~~

>>> from nipype.interfaces.ants import Atropos
>>> at = Atropos()
>>> at.inputs.dimension = 3
>>> at.inputs.intensity_images = 'structural.nii'
>>> at.inputs.mask_image = 'mask.nii'
>>> at.inputs.initialization = 'PriorProbabilityImages'
>>> at.inputs.prior_probability_images = ['rc1s1.nii', 'rc1s2.nii']
>>> at.inputs.number_of_tissue_classes = 2
>>> at.inputs.prior_weighting = 0.8
>>> at.inputs.prior_probability_threshold = 0.0000001
>>> at.inputs.likelihood_model = 'Gaussian'
>>> at.inputs.mrf_smoothing_factor = 0.2
>>> at.inputs.mrf_radius = [1, 1, 1]
>>> at.inputs.icm_use_synchronous_update = True
>>> at.inputs.maximum_number_of_icm_terations = 1
>>> at.inputs.n_iterations = 5
>>> at.inputs.convergence_threshold = 0.000001
>>> at.inputs.posterior_formulation = 'Socrates'
>>> at.inputs.use_mixture_model_proportions = True
>>> at.inputs.save_posteriors = True
>>> at.cmdline
'Atropos --image-dimensionality 3 --icm [1,1] --initialization PriorProbabilityImages[2,priors/priorProbImages%02d.nii,0.8,1e-07] --intensity-image structural.nii --likelihood-model Gaussian --mask-image mask.nii --mrf [0.2,1x1x1] --convergence [5,1e-06] --output [structural_labeled.nii,POSTERIOR_%02d.nii.gz] --posterior-formulation Socrates[1]'

Inputs::

        [Mandatory]
        initialization: ('Random' or 'Otsu' or 'KMeans' or
                 'PriorProbabilityImages' or 'PriorLabelImage')
                flag: %s
                requires: number_of_tissue_classes
        intensity_images: (an existing file name)
                flag: --intensity-image %s...
        mask_image: (an existing file name)
                flag: --mask-image %s
        number_of_tissue_classes: (an integer)
        terminal_output: ('stream' or 'allatonce' or 'file' or 'none')
                Control terminal output: `stream` - displays to terminal
                immediately, `allatonce` - waits till command is finished to display
                output, `file` - writes output to file, `none` - output is ignored

        [Optional]
        args: (a string)
                Additional parameters to the command
                flag: %s
        convergence_threshold: (a float)
                requires: n_iterations
        dimension: (3 or 2 or 4, nipype default value: 3)
                image dimension (2, 3, or 4)
                flag: --image-dimensionality %d
        environ: (a dictionary with keys which are a value of type 'str' and
                 with values which are a value of type 'str', nipype default value:
                 {})
                Environment variables
        icm_use_synchronous_update: (a boolean)
                flag: %s
        ignore_exception: (a boolean, nipype default value: False)
                Print an error message instead of throwing an exception in case the
                interface fails to run
        likelihood_model: (a string)
                flag: --likelihood-model %s
        maximum_number_of_icm_terations: (an integer)
                requires: icm_use_synchronous_update
        mrf_radius: (a list of items which are an integer)
                requires: mrf_smoothing_factor
        mrf_smoothing_factor: (a float)
                flag: %s
        n_iterations: (an integer)
                flag: %s
        num_threads: (an integer, nipype default value: 1)
                Number of ITK threads to use
        out_classified_image_name: (a file name)
                flag: %s
        output_posteriors_name_template: (a string, nipype default value:
                 POSTERIOR_%02d.nii.gz)
        posterior_formulation: (a string)
                flag: %s
        prior_probability_images: (an existing file name)
        prior_probability_threshold: (a float)
                requires: prior_weighting
        prior_weighting: (a float)
        save_posteriors: (a boolean)
        use_mixture_model_proportions: (a boolean)
                requires: posterior_formulation

Outputs::

        classified_image: (an existing file name)
        posteriors: (a file name)

.. _nipype.interfaces.ants.segmentation.LaplacianThickness:


.. index:: LaplacianThickness

LaplacianThickness
------------------

`Link to code <http://github.com/nipy/nipype/tree/e63e055194d62d2bdc4665688261c03a42fd0025/nipype/interfaces/ants/segmentation.py#L185>`__

Wraps command **LaplacianThickness**

Calculates the cortical thickness from an anatomical image

Examples
~~~~~~~~

>>> from nipype.interfaces.ants import LaplacianThickness
>>> cort_thick = LaplacianThickness()
>>> cort_thick.inputs.input_wm = 'white_matter.nii.gz'
>>> cort_thick.inputs.input_gm = 'gray_matter.nii.gz'
>>> cort_thick.inputs.output_image = 'output_thickness.nii.gz'
>>> cort_thick.cmdline
'LaplacianThickness white_matter.nii.gz gray_matter.nii.gz output_thickness.nii.gz'

Inputs::

        [Mandatory]
        input_gm: (a file name)
                gray matter segmentation image
                flag: %s, position: 2
        input_wm: (a file name)
                white matter segmentation image
                flag: %s, position: 1
        terminal_output: ('stream' or 'allatonce' or 'file' or 'none')
                Control terminal output: `stream` - displays to terminal
                immediately, `allatonce` - waits till command is finished to display
                output, `file` - writes output to file, `none` - output is ignored

        [Optional]
        args: (a string)
                Additional parameters to the command
                flag: %s
        dT: (a float)
                flag: dT=%d, position: 6
        environ: (a dictionary with keys which are a value of type 'str' and
                 with values which are a value of type 'str', nipype default value:
                 {})
                Environment variables
        ignore_exception: (a boolean, nipype default value: False)
                Print an error message instead of throwing an exception in case the
                interface fails to run
        num_threads: (an integer, nipype default value: 1)
                Number of ITK threads to use
        opt_tolerance: (a float)
                flag: optional-laplacian-tolerance=%d, position: 8
        output_image: (a file name)
                name of output file
                flag: %s, position: 3
        prior_thickness: (a float)
                flag: priorthickval=%d, position: 5
        smooth_param: (a float)
                flag: smoothparam=%d, position: 4
        sulcus_prior: (a boolean)
                flag: use-sulcus-prior, position: 7

Outputs::

        output_image: (an existing file name)
                Cortical thickness

.. _nipype.interfaces.ants.segmentation.N4BiasFieldCorrection:


.. index:: N4BiasFieldCorrection

N4BiasFieldCorrection
---------------------

`Link to code <http://github.com/nipy/nipype/tree/e63e055194d62d2bdc4665688261c03a42fd0025/nipype/interfaces/ants/segmentation.py#L255>`__

Wraps command **N4BiasFieldCorrection**

N4 is a variant of the popular N3 (nonparameteric nonuniform normalization)
retrospective bias correction algorithm. Based on the assumption that the
corruption of the low frequency bias field can be modeled as a convolution of
the intensity histogram by a Gaussian, the basic algorithmic protocol is to
iterate between deconvolving the intensity histogram by a Gaussian, remapping
the intensities, and then spatially smoothing this result by a B-spline modeling
of the bias field itself. The modifications from and improvements obtained over
the original N3 algorithm are described in [Tustison2010]_.

.. [Tustison2010] N. Tustison et al.,
  N4ITK: Improved N3 Bias Correction, IEEE Transactions on Medical Imaging,
  29(6):1310-1320, June 2010.

Examples
~~~~~~~~

>>> from nipype.interfaces.ants import N4BiasFieldCorrection
>>> n4 = N4BiasFieldCorrection()
>>> n4.inputs.dimension = 3
>>> n4.inputs.input_image = 'structural.nii'
>>> n4.inputs.bspline_fitting_distance = 300
>>> n4.inputs.shrink_factor = 3
>>> n4.inputs.n_iterations = [50,50,30,20]
>>> n4.inputs.convergence_threshold = 1e-6
>>> n4.cmdline
'N4BiasFieldCorrection --convergence [ 50x50x30x20 ,1e-06] --bsline-fitting [300] --image-dimension 3 --input-image structural.nii --output structural_corrected.nii --shrink-factor 3'

>>> n4_2 = N4BiasFieldCorrection()
>>> n4_2.inputs.input_image = 'structural.nii'
>>> n4_2.inputs.save_bias = True
>>> n4_2.cmdline
'N4BiasFieldCorrection --image-dimension 3 --input-image structural.nii --output [structural_corrected.nii,structural_bias.nii]'

Inputs::

        [Mandatory]
        input_image: (a file name)
                image to apply transformation to (generally a coregistered
                functional)
                flag: --input-image %s
        save_bias: (a boolean, nipype default value: False)
                True if the estimated bias should be saved to file.
                mutually_exclusive: bias_image
        terminal_output: ('stream' or 'allatonce' or 'file' or 'none')
                Control terminal output: `stream` - displays to terminal
                immediately, `allatonce` - waits till command is finished to display
                output, `file` - writes output to file, `none` - output is ignored

        [Optional]
        args: (a string)
                Additional parameters to the command
                flag: %s
        bias_image: (a file name)
                Filename for the estimated bias.
        bspline_fitting_distance: (a float)
                flag: --bsline-fitting [%g]
        convergence_threshold: (a float)
                flag: ,%g], position: 2
                requires: n_iterations
        dimension: (3 or 2, nipype default value: 3)
                image dimension (2 or 3)
                flag: --image-dimension %d
        environ: (a dictionary with keys which are a value of type 'str' and
                 with values which are a value of type 'str', nipype default value:
                 {})
                Environment variables
        ignore_exception: (a boolean, nipype default value: False)
                Print an error message instead of throwing an exception in case the
                interface fails to run
        mask_image: (a file name)
                flag: --mask-image %s
        n_iterations: (a list of items which are an integer)
                flag: --convergence [ %s, position: 1
                requires: convergence_threshold
        num_threads: (an integer, nipype default value: 1)
                Number of ITK threads to use
        output_image: (a string)
                output file name
                flag: --output %s
        shrink_factor: (an integer)
                flag: --shrink-factor %d

Outputs::

        bias_image: (an existing file name)
                Estimated bias
        output_image: (an existing file name)
                Warped image

.. _nipype.interfaces.ants.segmentation.antsCorticalThickness:


.. index:: antsCorticalThickness

antsCorticalThickness
---------------------

`Link to code <http://github.com/nipy/nipype/tree/e63e055194d62d2bdc4665688261c03a42fd0025/nipype/interfaces/ants/segmentation.py#L453>`__

Wraps command **antsCorticalThickness.sh**

Examples
~~~~~~~~
>>> from nipype.interfaces.ants.segmentation import antsCorticalThickness
>>> corticalthickness = antsCorticalThickness()
>>> corticalthickness.inputs.dimension = 3
>>> corticalthickness.inputs.anatomical_image ='T1.nii.gz'
>>> corticalthickness.inputs.brain_template = 'study_template.nii.gz'
>>> corticalthickness.inputs.brain_probability_mask ='ProbabilityMaskOfStudyTemplate.nii.gz'
>>> corticalthickness.inputs.segmentation_priors = ['BrainSegmentationPrior01.nii.gz', 'BrainSegmentationPrior02.nii.gz', 'BrainSegmentationPrior03.nii.gz', 'BrainSegmentationPrior04.nii.gz']
>>> corticalthickness.inputs.t1_registration_template = 'brain_study_template.nii.gz'
>>> corticalthickness.cmdline
'antsCorticalThickness.sh -a T1.nii.gz -m ProbabilityMaskOfStudyTemplate.nii.gz -e study_template.nii.gz -d 3 -s nii.gz -o antsCT_ -p BrainSegmentationPrior%02d.nii.gz -t brain_study_template.nii.gz'

Inputs::

        [Mandatory]
        anatomical_image: (an existing file name)
                Structural *intensity* image, typically T1.If more than one
                anatomical image is specified,subsequently specified images are used
                during thesegmentation process. However, only the firstimage is used
                in the registration of priors.Our suggestion would be to specify the
                T1as the first image.
                flag: -a %s
        brain_probability_mask: (an existing file name)
                brain probability mask in template space
                flag: -m %s
        brain_template: (an existing file name)
                Anatomical *intensity* template (possibly created using apopulation
                data set with buildtemplateparallel.sh in ANTs).This template is
                *not* skull-stripped.
                flag: -e %s
        segmentation_priors: (an existing file name)
                flag: -p %s
        t1_registration_template: (an existing file name)
                Anatomical *intensity* template(assumed to be skull-stripped). A
                commoncase would be where this would be the sametemplate as
                specified in the -e option whichis not skull stripped.
                flag: -t %s
        terminal_output: ('stream' or 'allatonce' or 'file' or 'none')
                Control terminal output: `stream` - displays to terminal
                immediately, `allatonce` - waits till command is finished to display
                output, `file` - writes output to file, `none` - output is ignored

        [Optional]
        args: (a string)
                Additional parameters to the command
                flag: %s
        b_spline_smoothing: (a boolean)
                Use B-spline SyN for registrations and B-splineexponential mapping
                in DiReCT.
                flag: -v
        cortical_label_image: (an existing file name)
                Cortical ROI labels to use as a prior for ATITH.
        debug: (a boolean)
                If > 0, runs a faster version of the script.Only for testing.
                Implies -u 0.Requires single thread computation for complete
                reproducibility.
                flag: -z 1
        dimension: (3 or 2, nipype default value: 3)
                image dimension (2 or 3)
                flag: -d %d
        environ: (a dictionary with keys which are a value of type 'str' and
                 with values which are a value of type 'str', nipype default value:
                 {})
                Environment variables
        extraction_registration_mask: (an existing file name)
                Mask (defined in the template space) used during registration for
                brain extraction.
                flag: -f %s
        ignore_exception: (a boolean, nipype default value: False)
                Print an error message instead of throwing an exception in case the
                interface fails to run
        image_suffix: (a string, nipype default value: nii.gz)
                any of standard ITK formats, nii.gz is default
                flag: -s %s
        keep_temporary_files: (an integer)
                Keep brain extraction/segmentation warps, etc (default = 0).
                flag: -k %d
        label_propagation: (a string)
                Incorporate a distance prior one the posterior formulation. Should
                beof the form 'label[lambda,boundaryProbability]' where labelis a
                value of 1,2,3,... denoting label ID. The labelprobability for
                anything outside the current label = boundaryProbability * exp(
                -lambda * distanceFromBoundary )Intuitively, smaller lambda values
                will increase the spatial capturerange of the distance prior. To
                apply to all label values, simply omitspecifying the label, i.e. -l
                [lambda,boundaryProbability].
                flag: -l %s
        max_iterations: (an integer)
                ANTS registration max iterations(default = 100x100x70x20)
                flag: -i %d
        num_threads: (an integer, nipype default value: 1)
                Number of ITK threads to use
        out_prefix: (a string, nipype default value: antsCT_)
                Prefix that is prepended to all output files (default = antsCT_)
                flag: -o %s
        posterior_formulation: (a string)
                Atropos posterior formulation and whether or notto use mixture model
                proportions.e.g 'Socrates[1]' (default) or 'Aristotle[1]'.Choose the
                latter if youwant use the distance priors (see also the -l optionfor
                label propagation control).
                flag: -b %s
        prior_segmentation_weight: (a float)
                Atropos spatial prior *probability* weight forthe segmentation
                flag: -w %f
        quick_registration: (a boolean)
                If = 1, use antsRegistrationSyNQuick.sh as the basis for
                registrationduring brain extraction, brain segmentation,
                and(optional) normalization to a template.Otherwise use
                antsRegistrationSyN.sh (default = 0).
                flag: -q 1
        segmentation_iterations: (an integer)
                N4 -> Atropos -> N4 iterations during segmentation(default = 3)
                flag: -n %d
        use_floatingpoint_precision: (0 or 1)
                Use floating point precision in registrations (default = 0)
                flag: -j %d
        use_random_seeding: (0 or 1)
                Use random number generated from system clock in Atropos(default =
                1)
                flag: -u %d

Outputs::

        BrainExtractionMask: (an existing file name)
                brain extraction mask
        BrainSegmentation: (an existing file name)
                brain segmentaion image
        BrainSegmentationN4: (an existing file name)
                N4 corrected image
        BrainSegmentationPosteriorsCSF: (an existing file name)
                CSF posterior probability image
        BrainSegmentationPosteriorsDGM: (an existing file name)
                DGM posterior probability image
        BrainSegmentationPosteriorsGM: (an existing file name)
                GM posterior probability image
        BrainSegmentationPosteriorsWM: (an existing file name)
                WM posterior probability image
        CorticalThickness: (an existing file name)
                cortical thickness file
        SubjectToTemplate0GenericAffine: (an existing file name)
                Template to subject inverse affine
        SubjectToTemplate1Warp: (an existing file name)
                Template to subject inverse warp
        TemplateToSubject0Warp: (an existing file name)
                Template to subject warp
        TemplateToSubject1GenericAffine: (an existing file name)
                Template to subject affine
        TemplateToSubjectLogJacobian: (an existing file name)
                Template to subject log jacobian
