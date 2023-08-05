.. AUTO-GENERATED FILE -- DO NOT EDIT!

workflows.dmri.connectivity.group_connectivity
==============================================


.. module:: nipype.workflows.dmri.connectivity.group_connectivity


.. _nipype.workflows.dmri.connectivity.group_connectivity.concatcsv:

:func:`concatcsv`
-----------------

`Link to code <http://github.com/nipy/nipype/tree/e63e055194d62d2bdc4665688261c03a42fd0025/nipype/workflows/dmri/connectivity/group_connectivity.py#L47>`__



This function will contatenate two "comma-separated value"
text files, but remove the first row (usually column headers) from
all but the first file.


.. _nipype.workflows.dmri.connectivity.group_connectivity.create_average_networks_by_group_workflow:

:func:`create_average_networks_by_group_workflow`
-------------------------------------------------

`Link to code <http://github.com/nipy/nipype/tree/e63e055194d62d2bdc4665688261c03a42fd0025/nipype/workflows/dmri/connectivity/group_connectivity.py#L429>`__



Creates a fourth-level pipeline to average the networks for two groups and merge them into a single
CFF file. This pipeline will also output the average networks in .gexf format, for visualization in other
graph viewers, such as Gephi.

Example
~~~~~~~

>>> import nipype.workflows.dmri.connectivity.group_connectivity as groupwork
>>> from nipype.testing import example_data
>>> subjects_dir = '.'
>>> data_dir = '.'
>>> output_dir = '.'
>>> group_list = {}
>>> group_list['group1'] = ['subj1', 'subj2']
>>> group_list['group2'] = ['subj3', 'subj4']
>>> l4pipeline = groupwork.create_average_networks_by_group_workflow(group_list, data_dir, subjects_dir, output_dir)
>>> l4pipeline.run()                 # doctest: +SKIP

Inputs::

    group_list: Dictionary of subject lists, keyed by group name
    data_dir: Path to the data directory
    subjects_dir: Path to the Freesurfer 'subjects' directory
    output_dir: Path for the output files
    title: String to use as a title for the output merged CFF file (default 'group')


.. _nipype.workflows.dmri.connectivity.group_connectivity.create_merge_group_network_results_workflow:

:func:`create_merge_group_network_results_workflow`
---------------------------------------------------

`Link to code <http://github.com/nipy/nipype/tree/e63e055194d62d2bdc4665688261c03a42fd0025/nipype/workflows/dmri/connectivity/group_connectivity.py#L349>`__



Creates a third-level pipeline to merge the Connectome File Format (CFF) outputs from each group
and combines them into a single CFF file for each group. This version of the third-level pipeline also
concatenates the comma-separated value files for the NetworkX metrics and the connectivity matrices
into single files.

Example
~~~~~~~

>>> import nipype.workflows.dmri.connectivity.group_connectivity as groupwork
>>> from nipype.testing import example_data
>>> subjects_dir = '.'
>>> data_dir = '.'
>>> output_dir = '.'
>>> group_list = {}
>>> group_list['group1'] = ['subj1', 'subj2']
>>> group_list['group2'] = ['subj3', 'subj4']
>>> l3pipeline = groupwork.create_merge_group_network_results_workflow(group_list, data_dir, subjects_dir, output_dir)
>>> l3pipeline.run()                 # doctest: +SKIP

Inputs::

        group_list: Dictionary of subject lists, keyed by group name
        data_dir: Path to the data directory
        subjects_dir: Path to the Freesurfer 'subjects' directory
        output_dir: Path for the output files
        title: String to use as a title for the output merged CFF file (default 'group')


.. _nipype.workflows.dmri.connectivity.group_connectivity.create_merge_group_networks_workflow:

:func:`create_merge_group_networks_workflow`
--------------------------------------------

`Link to code <http://github.com/nipy/nipype/tree/e63e055194d62d2bdc4665688261c03a42fd0025/nipype/workflows/dmri/connectivity/group_connectivity.py#L289>`__



Creates a third-level pipeline to merge the Connectome File Format (CFF) outputs from each group
and combines them into a single CFF file for each group.

Example
~~~~~~~

>>> import nipype.workflows.dmri.connectivity.group_connectivity as groupwork
>>> from nipype.testing import example_data
>>> subjects_dir = '.'
>>> data_dir = '.'
>>> output_dir = '.'
>>> group_list = {}
>>> group_list['group1'] = ['subj1', 'subj2']
>>> group_list['group2'] = ['subj3', 'subj4']
>>> l3pipeline = groupwork.create_merge_group_networks_workflow(group_list, data_dir, subjects_dir, output_dir)
>>> l3pipeline.run()                 # doctest: +SKIP

Inputs::

    group_list: Dictionary of subject lists, keyed by group name
    data_dir: Path to the data directory
    subjects_dir: Path to the Freesurfer 'subjects' directory
    output_dir: Path for the output files
    title: String to use as a title for the output merged CFF file (default 'group')


.. _nipype.workflows.dmri.connectivity.group_connectivity.create_merge_network_results_by_group_workflow:

:func:`create_merge_network_results_by_group_workflow`
------------------------------------------------------

`Link to code <http://github.com/nipy/nipype/tree/e63e055194d62d2bdc4665688261c03a42fd0025/nipype/workflows/dmri/connectivity/group_connectivity.py#L144>`__



Creates a second-level pipeline to merge the Connectome File Format (CFF) outputs from the group-level
MRtrix structural connectivity processing pipeline into a single CFF file for each group.

Example
~~~~~~~

>>> import nipype.workflows.dmri.connectivity.group_connectivity as groupwork
>>> from nipype.testing import example_data
>>> subjects_dir = '.'
>>> data_dir = '.'
>>> output_dir = '.'
>>> group_list = {}
>>> group_list['group1'] = ['subj1', 'subj2']
>>> group_list['group2'] = ['subj3', 'subj4']
>>> group_id = 'group1'
>>> l2pipeline = groupwork.create_merge_network_results_by_group_workflow(group_list, group_id, data_dir, subjects_dir, output_dir)
>>> l2pipeline.run()                 # doctest: +SKIP

Inputs::

    group_list: Dictionary of subject lists, keyed by group name
    group_id: String containing the group name
    data_dir: Path to the data directory
    subjects_dir: Path to the Freesurfer 'subjects' directory
    output_dir: Path for the output files


.. _nipype.workflows.dmri.connectivity.group_connectivity.create_merge_networks_by_group_workflow:

:func:`create_merge_networks_by_group_workflow`
-----------------------------------------------

`Link to code <http://github.com/nipy/nipype/tree/e63e055194d62d2bdc4665688261c03a42fd0025/nipype/workflows/dmri/connectivity/group_connectivity.py#L73>`__



Creates a second-level pipeline to merge the Connectome File Format (CFF) outputs from the group-level
MRtrix structural connectivity processing pipeline into a single CFF file for each group.

Example
~~~~~~~

>>> import nipype.workflows.dmri.connectivity.group_connectivity as groupwork
>>> from nipype.testing import example_data
>>> subjects_dir = '.'
>>> data_dir = '.'
>>> output_dir = '.'
>>> group_list = {}
>>> group_list['group1'] = ['subj1', 'subj2']
>>> group_list['group2'] = ['subj3', 'subj4']
>>> group_id = 'group1'
>>> l2pipeline = groupwork.create_merge_networks_by_group_workflow(group_list, group_id, data_dir, subjects_dir, output_dir)
>>> l2pipeline.run()                 # doctest: +SKIP

Inputs::

    group_list: Dictionary of subject lists, keyed by group name
    group_id: String containing the group name
    data_dir: Path to the data directory
    subjects_dir: Path to the Freesurfer 'subjects' directory
    output_dir: Path for the output files


.. _nipype.workflows.dmri.connectivity.group_connectivity.pullnodeIDs:

:func:`pullnodeIDs`
-------------------

`Link to code <http://github.com/nipy/nipype/tree/e63e055194d62d2bdc4665688261c03a42fd0025/nipype/workflows/dmri/connectivity/group_connectivity.py#L19>`__



This function will return the values contained, for each node in
a network, given an input key. By default it will return the node names

