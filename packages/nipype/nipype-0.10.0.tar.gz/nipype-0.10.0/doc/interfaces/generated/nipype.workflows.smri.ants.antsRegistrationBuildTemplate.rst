.. AUTO-GENERATED FILE -- DO NOT EDIT!

workflows.smri.ants.antsRegistrationBuildTemplate
=================================================


.. module:: nipype.workflows.smri.ants.antsRegistrationBuildTemplate


.. _nipype.workflows.smri.ants.antsRegistrationBuildTemplate.antsRegistrationTemplateBuildSingleIterationWF:

:func:`antsRegistrationTemplateBuildSingleIterationWF`
------------------------------------------------------

`Link to code <http://github.com/nipy/nipype/tree/e63e055194d62d2bdc4665688261c03a42fd0025/nipype/workflows/smri/ants/antsRegistrationBuildTemplate.py#L152>`__



Inputs::

       inputspec.images :
       inputspec.fixed_image :
       inputspec.ListOfPassiveImagesDictionaries :
       inputspec.interpolationMapping :

Outputs::

       outputspec.template :
       outputspec.transforms_list :
       outputspec.passive_deformed_templates :


Graph
~~~~~

.. graphviz::

	digraph antsRegistrationTemplateBuildSingleIterationWF_{

	  label="antsRegistrationTemplateBuildSingleIterationWF_";

	  antsRegistrationTemplateBuildSingleIterationWF__inputspec[label="inputspec (utility)"];

	  antsRegistrationTemplateBuildSingleIterationWF__99_GetPassiveImagesNode[label="99_GetPassiveImagesNode (utility)"];

	  antsRegistrationTemplateBuildSingleIterationWF__99_GetMovingImagesNode[label="99_GetMovingImagesNode (utility)"];

	  antsRegistrationTemplateBuildSingleIterationWF__BeginANTS[label="BeginANTS (ants)"];

	  antsRegistrationTemplateBuildSingleIterationWF__99_SplitAffineAndWarpsNode[label="99_SplitAffineAndWarpsNode (utility)"];

	  antsRegistrationTemplateBuildSingleIterationWF__AvgAffineTransform[label="AvgAffineTransform (ants)"];

	  antsRegistrationTemplateBuildSingleIterationWF__AvgWarpImages[label="AvgWarpImages (ants)"];

	  antsRegistrationTemplateBuildSingleIterationWF__GradientStepWarpImage[label="GradientStepWarpImage (ants)"];

	  antsRegistrationTemplateBuildSingleIterationWF__99_FlattenTransformAndImagesList[label="99_FlattenTransformAndImagesList (utility)"];

	  antsRegistrationTemplateBuildSingleIterationWF__wimtdeformed[label="wimtdeformed (ants)"];

	  antsRegistrationTemplateBuildSingleIterationWF__AvgDeformedImages[label="AvgDeformedImages (ants)"];

	  antsRegistrationTemplateBuildSingleIterationWF__UpdateTemplateShape[label="UpdateTemplateShape (ants)"];

	  antsRegistrationTemplateBuildSingleIterationWF__99_MakeTransformListWithGradientWarps[label="99_MakeTransformListWithGradientWarps (utility)"];

	  antsRegistrationTemplateBuildSingleIterationWF__ReshapeAverageImageWithShapeUpdate[label="ReshapeAverageImageWithShapeUpdate (ants)"];

	  antsRegistrationTemplateBuildSingleIterationWF__wimtPassivedeformed[label="wimtPassivedeformed (ants)"];

	  antsRegistrationTemplateBuildSingleIterationWF__99_RenestDeformedPassiveImages[label="99_RenestDeformedPassiveImages (utility)"];

	  antsRegistrationTemplateBuildSingleIterationWF__AvgDeformedPassiveImages[label="AvgDeformedPassiveImages (ants)"];

	  antsRegistrationTemplateBuildSingleIterationWF__ReshapeAveragePassiveImageWithShapeUpdate[label="ReshapeAveragePassiveImageWithShapeUpdate (ants)"];

	  antsRegistrationTemplateBuildSingleIterationWF__outputspec[label="outputspec (utility)"];

	  antsRegistrationTemplateBuildSingleIterationWF__inputspec -> antsRegistrationTemplateBuildSingleIterationWF__wimtdeformed;

	  antsRegistrationTemplateBuildSingleIterationWF__inputspec -> antsRegistrationTemplateBuildSingleIterationWF__99_GetPassiveImagesNode;

	  antsRegistrationTemplateBuildSingleIterationWF__inputspec -> antsRegistrationTemplateBuildSingleIterationWF__99_GetPassiveImagesNode;

	  antsRegistrationTemplateBuildSingleIterationWF__inputspec -> antsRegistrationTemplateBuildSingleIterationWF__BeginANTS;

	  antsRegistrationTemplateBuildSingleIterationWF__inputspec -> antsRegistrationTemplateBuildSingleIterationWF__99_FlattenTransformAndImagesList;

	  antsRegistrationTemplateBuildSingleIterationWF__inputspec -> antsRegistrationTemplateBuildSingleIterationWF__99_GetMovingImagesNode;

	  antsRegistrationTemplateBuildSingleIterationWF__inputspec -> antsRegistrationTemplateBuildSingleIterationWF__99_GetMovingImagesNode;

	  antsRegistrationTemplateBuildSingleIterationWF__inputspec -> antsRegistrationTemplateBuildSingleIterationWF__99_GetMovingImagesNode;

	  antsRegistrationTemplateBuildSingleIterationWF__inputspec -> antsRegistrationTemplateBuildSingleIterationWF__99_RenestDeformedPassiveImages;

	  antsRegistrationTemplateBuildSingleIterationWF__99_GetPassiveImagesNode -> antsRegistrationTemplateBuildSingleIterationWF__99_FlattenTransformAndImagesList;

	  antsRegistrationTemplateBuildSingleIterationWF__99_GetMovingImagesNode -> antsRegistrationTemplateBuildSingleIterationWF__BeginANTS;

	  antsRegistrationTemplateBuildSingleIterationWF__99_GetMovingImagesNode -> antsRegistrationTemplateBuildSingleIterationWF__BeginANTS;

	  antsRegistrationTemplateBuildSingleIterationWF__99_GetMovingImagesNode -> antsRegistrationTemplateBuildSingleIterationWF__wimtdeformed;

	  antsRegistrationTemplateBuildSingleIterationWF__BeginANTS -> antsRegistrationTemplateBuildSingleIterationWF__99_SplitAffineAndWarpsNode;

	  antsRegistrationTemplateBuildSingleIterationWF__BeginANTS -> antsRegistrationTemplateBuildSingleIterationWF__wimtdeformed;

	  antsRegistrationTemplateBuildSingleIterationWF__BeginANTS -> antsRegistrationTemplateBuildSingleIterationWF__wimtdeformed;

	  antsRegistrationTemplateBuildSingleIterationWF__BeginANTS -> antsRegistrationTemplateBuildSingleIterationWF__99_FlattenTransformAndImagesList;

	  antsRegistrationTemplateBuildSingleIterationWF__BeginANTS -> antsRegistrationTemplateBuildSingleIterationWF__99_FlattenTransformAndImagesList;

	  antsRegistrationTemplateBuildSingleIterationWF__99_SplitAffineAndWarpsNode -> antsRegistrationTemplateBuildSingleIterationWF__AvgAffineTransform;

	  antsRegistrationTemplateBuildSingleIterationWF__99_SplitAffineAndWarpsNode -> antsRegistrationTemplateBuildSingleIterationWF__AvgWarpImages;

	  antsRegistrationTemplateBuildSingleIterationWF__AvgAffineTransform -> antsRegistrationTemplateBuildSingleIterationWF__UpdateTemplateShape;

	  antsRegistrationTemplateBuildSingleIterationWF__AvgAffineTransform -> antsRegistrationTemplateBuildSingleIterationWF__99_MakeTransformListWithGradientWarps;

	  antsRegistrationTemplateBuildSingleIterationWF__AvgWarpImages -> antsRegistrationTemplateBuildSingleIterationWF__GradientStepWarpImage;

	  antsRegistrationTemplateBuildSingleIterationWF__GradientStepWarpImage -> antsRegistrationTemplateBuildSingleIterationWF__UpdateTemplateShape;

	  antsRegistrationTemplateBuildSingleIterationWF__99_FlattenTransformAndImagesList -> antsRegistrationTemplateBuildSingleIterationWF__wimtPassivedeformed;

	  antsRegistrationTemplateBuildSingleIterationWF__99_FlattenTransformAndImagesList -> antsRegistrationTemplateBuildSingleIterationWF__wimtPassivedeformed;

	  antsRegistrationTemplateBuildSingleIterationWF__99_FlattenTransformAndImagesList -> antsRegistrationTemplateBuildSingleIterationWF__wimtPassivedeformed;

	  antsRegistrationTemplateBuildSingleIterationWF__99_FlattenTransformAndImagesList -> antsRegistrationTemplateBuildSingleIterationWF__wimtPassivedeformed;

	  antsRegistrationTemplateBuildSingleIterationWF__99_FlattenTransformAndImagesList -> antsRegistrationTemplateBuildSingleIterationWF__99_RenestDeformedPassiveImages;

	  antsRegistrationTemplateBuildSingleIterationWF__wimtdeformed -> antsRegistrationTemplateBuildSingleIterationWF__AvgDeformedImages;

	  antsRegistrationTemplateBuildSingleIterationWF__AvgDeformedImages -> antsRegistrationTemplateBuildSingleIterationWF__UpdateTemplateShape;

	  antsRegistrationTemplateBuildSingleIterationWF__AvgDeformedImages -> antsRegistrationTemplateBuildSingleIterationWF__ReshapeAverageImageWithShapeUpdate;

	  antsRegistrationTemplateBuildSingleIterationWF__AvgDeformedImages -> antsRegistrationTemplateBuildSingleIterationWF__ReshapeAverageImageWithShapeUpdate;

	  antsRegistrationTemplateBuildSingleIterationWF__AvgDeformedImages -> antsRegistrationTemplateBuildSingleIterationWF__wimtPassivedeformed;

	  antsRegistrationTemplateBuildSingleIterationWF__UpdateTemplateShape -> antsRegistrationTemplateBuildSingleIterationWF__99_MakeTransformListWithGradientWarps;

	  antsRegistrationTemplateBuildSingleIterationWF__99_MakeTransformListWithGradientWarps -> antsRegistrationTemplateBuildSingleIterationWF__ReshapeAverageImageWithShapeUpdate;

	  antsRegistrationTemplateBuildSingleIterationWF__99_MakeTransformListWithGradientWarps -> antsRegistrationTemplateBuildSingleIterationWF__ReshapeAveragePassiveImageWithShapeUpdate;

	  antsRegistrationTemplateBuildSingleIterationWF__ReshapeAverageImageWithShapeUpdate -> antsRegistrationTemplateBuildSingleIterationWF__outputspec;

	  antsRegistrationTemplateBuildSingleIterationWF__wimtPassivedeformed -> antsRegistrationTemplateBuildSingleIterationWF__99_RenestDeformedPassiveImages;

	  antsRegistrationTemplateBuildSingleIterationWF__99_RenestDeformedPassiveImages -> antsRegistrationTemplateBuildSingleIterationWF__AvgDeformedPassiveImages;

	  antsRegistrationTemplateBuildSingleIterationWF__99_RenestDeformedPassiveImages -> antsRegistrationTemplateBuildSingleIterationWF__AvgDeformedPassiveImages;

	  antsRegistrationTemplateBuildSingleIterationWF__99_RenestDeformedPassiveImages -> antsRegistrationTemplateBuildSingleIterationWF__ReshapeAveragePassiveImageWithShapeUpdate;

	  antsRegistrationTemplateBuildSingleIterationWF__99_RenestDeformedPassiveImages -> antsRegistrationTemplateBuildSingleIterationWF__ReshapeAveragePassiveImageWithShapeUpdate;

	  antsRegistrationTemplateBuildSingleIterationWF__AvgDeformedPassiveImages -> antsRegistrationTemplateBuildSingleIterationWF__ReshapeAveragePassiveImageWithShapeUpdate;

	  antsRegistrationTemplateBuildSingleIterationWF__AvgDeformedPassiveImages -> antsRegistrationTemplateBuildSingleIterationWF__ReshapeAveragePassiveImageWithShapeUpdate;

	  antsRegistrationTemplateBuildSingleIterationWF__ReshapeAveragePassiveImageWithShapeUpdate -> antsRegistrationTemplateBuildSingleIterationWF__outputspec;

	}


.. _nipype.workflows.smri.ants.antsRegistrationBuildTemplate.FlattenTransformAndImagesList:

:func:`FlattenTransformAndImagesList`
-------------------------------------

`Link to code <http://github.com/nipy/nipype/tree/e63e055194d62d2bdc4665688261c03a42fd0025/nipype/workflows/smri/ants/antsRegistrationBuildTemplate.py#L81>`__






.. _nipype.workflows.smri.ants.antsRegistrationBuildTemplate.GetFirstListElement:

:func:`GetFirstListElement`
---------------------------

`Link to code <http://github.com/nipy/nipype/tree/e63e055194d62d2bdc4665688261c03a42fd0025/nipype/workflows/smri/ants/antsRegistrationBuildTemplate.py#L27>`__






.. _nipype.workflows.smri.ants.antsRegistrationBuildTemplate.GetMovingImages:

:func:`GetMovingImages`
-----------------------

`Link to code <http://github.com/nipy/nipype/tree/e63e055194d62d2bdc4665688261c03a42fd0025/nipype/workflows/smri/ants/antsRegistrationBuildTemplate.py#L122>`__



This currently ONLY works when registrationImageTypes has
length of exactly 1.  When the new multi-variate registration
is introduced, it will be expanded.


.. _nipype.workflows.smri.ants.antsRegistrationBuildTemplate.GetPassiveImages:

:func:`GetPassiveImages`
------------------------

`Link to code <http://github.com/nipy/nipype/tree/e63e055194d62d2bdc4665688261c03a42fd0025/nipype/workflows/smri/ants/antsRegistrationBuildTemplate.py#L134>`__






.. _nipype.workflows.smri.ants.antsRegistrationBuildTemplate.MakeTransformListWithGradientWarps:

:func:`MakeTransformListWithGradientWarps`
------------------------------------------

`Link to code <http://github.com/nipy/nipype/tree/e63e055194d62d2bdc4665688261c03a42fd0025/nipype/workflows/smri/ants/antsRegistrationBuildTemplate.py#L30>`__






.. _nipype.workflows.smri.ants.antsRegistrationBuildTemplate.RenestDeformedPassiveImages:

:func:`RenestDeformedPassiveImages`
-----------------------------------

`Link to code <http://github.com/nipy/nipype/tree/e63e055194d62d2bdc4665688261c03a42fd0025/nipype/workflows/smri/ants/antsRegistrationBuildTemplate.py#L34>`__






.. _nipype.workflows.smri.ants.antsRegistrationBuildTemplate.SplitAffineAndWarpComponents:

:func:`SplitAffineAndWarpComponents`
------------------------------------

`Link to code <http://github.com/nipy/nipype/tree/e63e055194d62d2bdc4665688261c03a42fd0025/nipype/workflows/smri/ants/antsRegistrationBuildTemplate.py#L69>`__






.. _nipype.workflows.smri.ants.antsRegistrationBuildTemplate.makeListOfOneElement:

:func:`makeListOfOneElement`
----------------------------

`Link to code <http://github.com/nipy/nipype/tree/e63e055194d62d2bdc4665688261c03a42fd0025/nipype/workflows/smri/ants/antsRegistrationBuildTemplate.py#L23>`__





