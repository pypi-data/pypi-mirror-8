.. AUTO-GENERATED FILE -- DO NOT EDIT!

interfaces.slicer.surface
=========================


.. _nipype.interfaces.slicer.surface.GrayscaleModelMaker:


.. index:: GrayscaleModelMaker

GrayscaleModelMaker
-------------------

`Link to code <http://github.com/nipy/nipype/tree/e63e055194d62d2bdc4665688261c03a42fd0025/nipype/interfaces/slicer/surface.py#L91>`__

Wraps command **GrayscaleModelMaker **

title: Grayscale Model Maker

category: Surface Models

description: Create 3D surface models from grayscale data. This module uses Marching Cubes to create an isosurface at a given threshold. The resulting surface consists of triangles that separate a volume into regions below and above the threshold. The resulting surface can be smoothed and decimated. This model works on continuous data while the module Model Maker works on labeled (or discrete) data.

version: 3.0

documentation-url: http://wiki.slicer.org/slicerWiki/index.php/Documentation/4.1/Modules/GrayscaleModelMaker

license: slicer3

contributor: Nicole Aucoin (SPL, BWH), Bill Lorensen (GE)

acknowledgements: This work is part of the National Alliance for Medical Image Computing (NAMIC), funded by the National Institutes of Health through the NIH Roadmap for Medical Research, Grant U54 EB005149.

Inputs::

        [Mandatory]
        terminal_output: ('stream' or 'allatonce' or 'file' or 'none')
                Control terminal output: `stream` - displays to terminal
                immediately, `allatonce` - waits till command is finished to display
                output, `file` - writes output to file, `none` - output is ignored

        [Optional]
        InputVolume: (an existing file name)
                Volume containing the input grayscale data.
                flag: %s, position: -2
        OutputGeometry: (a boolean or a file name)
                Output that contains geometry model.
                flag: %s, position: -1
        args: (a string)
                Additional parameters to the command
                flag: %s
        decimate: (a float)
                Target reduction during decimation, as a decimal percentage
                reduction in the number of polygons. If 0, no decimation will be
                done.
                flag: --decimate %f
        environ: (a dictionary with keys which are a value of type 'str' and
                 with values which are a value of type 'str', nipype default value:
                 {})
                Environment variables
        ignore_exception: (a boolean, nipype default value: False)
                Print an error message instead of throwing an exception in case the
                interface fails to run
        name: (a string)
                Name to use for this model.
                flag: --name %s
        pointnormals: (a boolean)
                Calculate the point normals? Calculated point normals make the
                surface appear smooth. Without point normals, the surface will
                appear faceted.
                flag: --pointnormals
        smooth: (an integer)
                Number of smoothing iterations. If 0, no smoothing will be done.
                flag: --smooth %d
        splitnormals: (a boolean)
                Splitting normals is useful for visualizing sharp features. However
                it creates holes in surfaces which affect measurements
                flag: --splitnormals
        threshold: (a float)
                Grayscale threshold of isosurface. The resulting surface of
                triangles separates the volume into voxels that lie above (inside)
                and below (outside) the threshold.
                flag: --threshold %f

Outputs::

        OutputGeometry: (an existing file name)
                Output that contains geometry model.

.. _nipype.interfaces.slicer.surface.LabelMapSmoothing:


.. index:: LabelMapSmoothing

LabelMapSmoothing
-----------------

`Link to code <http://github.com/nipy/nipype/tree/e63e055194d62d2bdc4665688261c03a42fd0025/nipype/interfaces/slicer/surface.py#L162>`__

Wraps command **LabelMapSmoothing **

title: Label Map Smoothing

category: Surface Models

description: This filter smoothes a binary label map.  With a label map as input, this filter runs an anti-alising algorithm followed by a Gaussian smoothing algorithm.  The output is a smoothed label map.

version: 1.0

documentation-url: http://wiki.slicer.org/slicerWiki/index.php/Documentation/4.1/Modules/LabelMapSmoothing

contributor: Dirk Padfield (GE), Josh Cates (Utah), Ross Whitaker (Utah)

acknowledgements: This work is part of the National Alliance for Medical Image Computing (NAMIC), funded by the National Institutes of Health through the NIH Roadmap for Medical Research, Grant U54 EB005149.  This filter is based on work developed at the University of Utah, and implemented at GE Research.

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
        gaussianSigma: (a float)
                The standard deviation of the Gaussian kernel
                flag: --gaussianSigma %f
        ignore_exception: (a boolean, nipype default value: False)
                Print an error message instead of throwing an exception in case the
                interface fails to run
        inputVolume: (an existing file name)
                Input label map to smooth
                flag: %s, position: -2
        labelToSmooth: (an integer)
                The label to smooth. All others will be ignored. If no label is
                selected by the user, the maximum label in the image is chosen by
                default.
                flag: --labelToSmooth %d
        maxRMSError: (a float)
                The maximum RMS error.
                flag: --maxRMSError %f
        numberOfIterations: (an integer)
                The number of iterations of the level set AntiAliasing algorithm
                flag: --numberOfIterations %d
        outputVolume: (a boolean or a file name)
                Smoothed label map
                flag: %s, position: -1

Outputs::

        outputVolume: (an existing file name)
                Smoothed label map

.. _nipype.interfaces.slicer.surface.MergeModels:


.. index:: MergeModels

MergeModels
-----------

`Link to code <http://github.com/nipy/nipype/tree/e63e055194d62d2bdc4665688261c03a42fd0025/nipype/interfaces/slicer/surface.py#L19>`__

Wraps command **MergeModels **

title: Merge Models

category: Surface Models

description: Merge the polydata from two input models and output a new model with the added polydata. Uses the vtkAppendPolyData filter. Works on .vtp and .vtk surface files.

version: $Revision$

documentation-url: http://wiki.slicer.org/slicerWiki/index.php/Documentation/4.1/Modules/MergeModels

contributor: Nicole Aucoin (SPL, BWH), Ron Kikinis (SPL, BWH), Daniel Haehn (SPL, BWH)

acknowledgements: This work is part of the National Alliance for Medical Image Computing (NAMIC), funded by the National Institutes of Health through the NIH Roadmap for Medical Research, Grant U54 EB005149.

Inputs::

        [Mandatory]
        terminal_output: ('stream' or 'allatonce' or 'file' or 'none')
                Control terminal output: `stream` - displays to terminal
                immediately, `allatonce` - waits till command is finished to display
                output, `file` - writes output to file, `none` - output is ignored

        [Optional]
        Model1: (an existing file name)
                Model
                flag: %s, position: -3
        Model2: (an existing file name)
                Model
                flag: %s, position: -2
        ModelOutput: (a boolean or a file name)
                Model
                flag: %s, position: -1
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

Outputs::

        ModelOutput: (an existing file name)
                Model

.. _nipype.interfaces.slicer.surface.ModelMaker:


.. index:: ModelMaker

ModelMaker
----------

`Link to code <http://github.com/nipy/nipype/tree/e63e055194d62d2bdc4665688261c03a42fd0025/nipype/interfaces/slicer/surface.py#L210>`__

Wraps command **ModelMaker **

title: Model Maker

category: Surface Models

description: Create 3D surface models from segmented data.<p>Models are imported into Slicer under a model hierarchy node in a MRML scene. The model colors are set by the color table associated with the input volume (these colours will only be visible if you load the model scene file).</p><p><b>Create Multiple:</b></p><p>If you specify a list of Labels, it will over ride any start/end label settings.</p><p>If you click<i>Generate All</i>it will over ride the list of lables and any start/end label settings.</p><p><b>Model Maker Settings:</b></p><p>You can set the number of smoothing iterations, target reduction in number of polygons (decimal percentage). Use 0 and 1 if you wish no smoothing nor decimation.<br>You can set the flags to split normals or generate point normals in this pane as well.<br>You can save a copy of the models after intermediate steps (marching cubes, smoothing, and decimation if not joint smoothing, otherwise just after decimation); these models are not saved in the mrml file, turn off deleting temporary files first in the python window:<br><i>slicer.modules.modelmaker.cliModuleLogic().DeleteTemporaryFilesOff()</i></p>

version: 4.1

documentation-url: http://wiki.slicer.org/slicerWiki/index.php/Documentation/4.1/Modules/ModelMaker

license: slicer4

contributor: Nicole Aucoin (SPL, BWH), Ron Kikinis (SPL, BWH), Bill Lorensen (GE)

acknowledgements: This work is part of the National Alliance for Medical Image Computing (NAMIC), funded by the National Institutes of Health through the NIH Roadmap for Medical Research, Grant U54 EB005149.

Inputs::

        [Mandatory]
        terminal_output: ('stream' or 'allatonce' or 'file' or 'none')
                Control terminal output: `stream` - displays to terminal
                immediately, `allatonce` - waits till command is finished to display
                output, `file` - writes output to file, `none` - output is ignored

        [Optional]
        InputVolume: (an existing file name)
                Input label map. The Input Volume drop down menu is populated with
                the label map volumes that are present in the scene, select one from
                which to generate models.
                flag: %s, position: -1
        args: (a string)
                Additional parameters to the command
                flag: %s
        color: (an existing file name)
                Color table to make labels to colors and objects
                flag: --color %s
        debug: (a boolean)
                turn this flag on in order to see debugging output (look in the
                Error Log window that is accessed via the View menu)
                flag: --debug
        decimate: (a float)
                Chose the target reduction in number of polygons as a decimal
                percentage (between 0 and 1) of the number of polygons. Specifies
                the percentage of triangles to be removed. For example, 0.1 means
                10% reduction and 0.9 means 90% reduction.
                flag: --decimate %f
        end: (an integer)
                If you want to specify a continuous range of labels from which to
                generate models, enter the higher label here. Voxel value up to
                which to continue making models. Skip any values with zero voxels.
                flag: --end %d
        environ: (a dictionary with keys which are a value of type 'str' and
                 with values which are a value of type 'str', nipype default value:
                 {})
                Environment variables
        filtertype: ('Sinc' or 'Laplacian')
                You can control the type of smoothing done on the models by
                selecting a filter type of either Sinc or Laplacian.
                flag: --filtertype %s
        generateAll: (a boolean)
                Generate models for all labels in the input volume. select this
                option if you want to create all models that correspond to all
                values in a labelmap volume (using the Joint Smoothing option below
                is useful with this option). Ignores Labels, Start Label, End Label
                settings. Skips label 0.
                flag: --generateAll
        ignore_exception: (a boolean, nipype default value: False)
                Print an error message instead of throwing an exception in case the
                interface fails to run
        jointsmooth: (a boolean)
                This will ensure that all resulting models fit together smoothly,
                like jigsaw puzzle pieces. Otherwise the models will be smoothed
                independently and may overlap.
                flag: --jointsmooth
        labels: (an integer)
                A comma separated list of label values from which to make models. f
                you specify a list of Labels, it will override any start/end label
                settings. If you click Generate All Models it will override the list
                of labels and any start/end label settings.
                flag: --labels %s
        modelSceneFile: (a boolean or a list of items which are a file name)
                Generated models, under a model hierarchy node. Models are imported
                into Slicer under a model hierarchy node, and their colors are set
                by the color table associated with the input label map volume. The
                model hierarchy node must be created before running the model maker,
                by selecting Create New ModelHierarchy from the Models drop down
                menu. If you're running from the command line, a model hierarchy
                node in a new mrml scene will be created for you.
                flag: --modelSceneFile %s...
        name: (a string)
                Name to use for this model. Any text entered in the entry box will
                be the starting string for the created model file names. The label
                number and the color name will also be part of the file name. If
                making multiple models, use this as a prefix to the label and color
                name.
                flag: --name %s
        pad: (a boolean)
                Pad the input volume with zero value voxels on all 6 faces in order
                to ensure the production of closed surfaces. Sets the origin
                translation and extent translation so that the models still line up
                with the unpadded input volume.
                flag: --pad
        pointnormals: (a boolean)
                Turn this flag on if you wish to calculate the normal vectors for
                the points.
                flag: --pointnormals
        saveIntermediateModels: (a boolean)
                You can save a copy of the models after each of the intermediate
                steps (marching cubes, smoothing, and decimation if not joint
                smoothing, otherwise just after decimation). These intermediate
                models are not saved in the mrml file, you have to load them
                manually after turning off deleting temporary files in they python
                console (View ->Python Interactor) using the following command slice
                r.modules.modelmaker.cliModuleLogic().DeleteTemporaryFilesOff().
                flag: --saveIntermediateModels
        skipUnNamed: (a boolean)
                Select this to not generate models from labels that do not have
                names defined in the color look up table associated with the input
                label map. If true, only models which have an entry in the color
                table will be generated. If false, generate all models that exist
                within the label range.
                flag: --skipUnNamed
        smooth: (an integer)
                Here you can set the number of smoothing iterations for Laplacian
                smoothing, or the degree of the polynomial approximating the
                windowed Sinc function. Use 0 if you wish no smoothing.
                flag: --smooth %d
        splitnormals: (a boolean)
                Splitting normals is useful for visualizing sharp features. However
                it creates holes in surfaces which affects measurements.
                flag: --splitnormals
        start: (an integer)
                If you want to specify a continuous range of labels from which to
                generate models, enter the lower label here. Voxel value from which
                to start making models. Used instead of the label list to specify a
                range (make sure the label list is empty or it will over ride this).
                flag: --start %d

Outputs::

        modelSceneFile: (an existing file name)
                Generated models, under a model hierarchy node. Models are imported
                into Slicer under a model hierarchy node, and their colors are set
                by the color table associated with the input label map volume. The
                model hierarchy node must be created before running the model maker,
                by selecting Create New ModelHierarchy from the Models drop down
                menu. If you're running from the command line, a model hierarchy
                node in a new mrml scene will be created for you.

.. _nipype.interfaces.slicer.surface.ModelToLabelMap:


.. index:: ModelToLabelMap

ModelToLabelMap
---------------

`Link to code <http://github.com/nipy/nipype/tree/e63e055194d62d2bdc4665688261c03a42fd0025/nipype/interfaces/slicer/surface.py#L53>`__

Wraps command **ModelToLabelMap **

title: Model To Label Map

category: Surface Models

description: Intersects an input model with an reference volume and produces an output label map.

version: 0.1.0.$Revision: 8643 $(alpha)

documentation-url: http://wiki.slicer.org/slicerWiki/index.php/Documentation/4.1/Modules/PolyDataToLabelMap

contributor: Nicole Aucoin (SPL, BWH), Xiaodong Tao (GE)

acknowledgements: This work is part of the National Alliance for Medical Image Computing (NAMIC), funded by the National Institutes of Health through the NIH Roadmap for Medical Research, Grant U54 EB005149.

Inputs::

        [Mandatory]
        terminal_output: ('stream' or 'allatonce' or 'file' or 'none')
                Control terminal output: `stream` - displays to terminal
                immediately, `allatonce` - waits till command is finished to display
                output, `file` - writes output to file, `none` - output is ignored

        [Optional]
        InputVolume: (an existing file name)
                Input volume
                flag: %s, position: -3
        OutputVolume: (a boolean or a file name)
                The label volume
                flag: %s, position: -1
        args: (a string)
                Additional parameters to the command
                flag: %s
        distance: (a float)
                Sample distance
                flag: --distance %f
        environ: (a dictionary with keys which are a value of type 'str' and
                 with values which are a value of type 'str', nipype default value:
                 {})
                Environment variables
        ignore_exception: (a boolean, nipype default value: False)
                Print an error message instead of throwing an exception in case the
                interface fails to run
        surface: (an existing file name)
                Model
                flag: %s, position: -2

Outputs::

        OutputVolume: (an existing file name)
                The label volume

.. _nipype.interfaces.slicer.surface.ProbeVolumeWithModel:


.. index:: ProbeVolumeWithModel

ProbeVolumeWithModel
--------------------

`Link to code <http://github.com/nipy/nipype/tree/e63e055194d62d2bdc4665688261c03a42fd0025/nipype/interfaces/slicer/surface.py#L126>`__

Wraps command **ProbeVolumeWithModel **

title: Probe Volume With Model

category: Surface Models

description: Paint a model by a volume (using vtkProbeFilter).

version: 0.1.0.$Revision: 1892 $(alpha)

documentation-url: http://wiki.slicer.org/slicerWiki/index.php/Documentation/4.1/Modules/ProbeVolumeWithModel

contributor: Lauren O'Donnell (SPL, BWH)

acknowledgements: BWH, NCIGT/LMI

Inputs::

        [Mandatory]
        terminal_output: ('stream' or 'allatonce' or 'file' or 'none')
                Control terminal output: `stream` - displays to terminal
                immediately, `allatonce` - waits till command is finished to display
                output, `file` - writes output to file, `none` - output is ignored

        [Optional]
        InputModel: (an existing file name)
                Input model
                flag: %s, position: -2
        InputVolume: (an existing file name)
                Volume to use to 'paint' the model
                flag: %s, position: -3
        OutputModel: (a boolean or a file name)
                Output 'painted' model
                flag: %s, position: -1
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

Outputs::

        OutputModel: (an existing file name)
                Output 'painted' model
