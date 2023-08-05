.. AUTO-GENERATED FILE -- DO NOT EDIT!

interfaces.cmtk.nx
==================


.. _nipype.interfaces.cmtk.nx.AverageNetworks:


.. index:: AverageNetworks

AverageNetworks
---------------

`Link to code <http://github.com/nipy/nipype/tree/e63e055194d62d2bdc4665688261c03a42fd0025/nipype/interfaces/cmtk/nx.py#L505>`__

Calculates and outputs the average network given a set of input NetworkX gpickle files

This interface will only keep an edge in the averaged network if that edge is present in
at least half of the input networks.

Example
~~~~~~~

>>> import nipype.interfaces.cmtk as cmtk
>>> avg = cmtk.AverageNetworks()
>>> avg.inputs.in_files = ['subj1.pck', 'subj2.pck']
>>> avg.run()                 # doctest: +SKIP

Inputs::

        [Mandatory]
        in_files: (an existing file name)
                Networks for a group of subjects

        [Optional]
        group_id: (a string, nipype default value: group1)
                ID for group
        ignore_exception: (a boolean, nipype default value: False)
                Print an error message instead of throwing an exception in case the
                interface fails to run
        out_gexf_groupavg: (a file name)
                Average network saved as a .gexf file
        out_gpickled_groupavg: (a file name)
                Average network saved as a NetworkX .pck
        resolution_network_file: (an existing file name)
                Parcellation files from Connectome Mapping Toolkit. This is not
                necessary, but if included, the interface will output the
                statistical maps as networkx graphs.

Outputs::

        gexf_groupavg: (a file name)
                Average network saved as a .gexf file
        gpickled_groupavg: (a file name)
                Average network saved as a NetworkX .pck
        matlab_groupavgs: (a file name)

.. _nipype.interfaces.cmtk.nx.NetworkXMetrics:


.. index:: NetworkXMetrics

NetworkXMetrics
---------------

`Link to code <http://github.com/nipy/nipype/tree/e63e055194d62d2bdc4665688261c03a42fd0025/nipype/interfaces/cmtk/nx.py#L362>`__

Calculates and outputs NetworkX-based measures for an input network

Example
~~~~~~~

>>> import nipype.interfaces.cmtk as cmtk
>>> nxmetrics = cmtk.NetworkXMetrics()
>>> nxmetrics.inputs.in_file = 'subj1.pck'
>>> nxmetrics.run()                 # doctest: +SKIP

Inputs::

        [Mandatory]
        in_file: (an existing file name)
                Input network

        [Optional]
        compute_clique_related_measures: (a boolean, nipype default value:
                 False)
                Computing clique-related measures (e.g. node clique number) can be
                very time consuming
        ignore_exception: (a boolean, nipype default value: False)
                Print an error message instead of throwing an exception in case the
                interface fails to run
        out_edge_metrics_matlab: (a file name)
                Output edge metrics in MATLAB .mat format
        out_global_metrics_matlab: (a file name)
                Output node metrics in MATLAB .mat format
        out_k_core: (a file name, nipype default value: k_core)
                Computed k-core network stored as a NetworkX pickle.
        out_k_crust: (a file name, nipype default value: k_crust)
                Computed k-crust network stored as a NetworkX pickle.
        out_k_shell: (a file name, nipype default value: k_shell)
                Computed k-shell network stored as a NetworkX pickle.
        out_node_metrics_matlab: (a file name)
                Output node metrics in MATLAB .mat format
        out_pickled_extra_measures: (a file name, nipype default value:
                 extra_measures)
                Network measures for group 1 that return dictionaries stored as a
                Pickle.
        treat_as_weighted_graph: (a boolean, nipype default value: True)
                Some network metrics can be calculated while considering only a
                binarized version of the graph

Outputs::

        edge_measure_networks: (a file name)
        edge_measures_matlab: (a file name)
                Output edge metrics in MATLAB .mat format
        global_measures_matlab: (a file name)
                Output global metrics in MATLAB .mat format
        gpickled_network_files: (a file name)
        k_core: (a file name)
                Computed k-core network stored as a NetworkX pickle.
        k_crust: (a file name)
                Computed k-crust network stored as a NetworkX pickle.
        k_networks: (a file name)
        k_shell: (a file name)
                Computed k-shell network stored as a NetworkX pickle.
        matlab_dict_measures: (a file name)
        matlab_matrix_files: (a file name)
        node_measure_networks: (a file name)
        node_measures_matlab: (a file name)
                Output node metrics in MATLAB .mat format
        pickled_extra_measures: (a file name)
                Network measures for the group that return dictionaries, stored as a
                Pickle.

.. module:: nipype.interfaces.cmtk.nx


.. _nipype.interfaces.cmtk.nx.add_dicts_by_key:

:func:`add_dicts_by_key`
------------------------

`Link to code <http://github.com/nipy/nipype/tree/e63e055194d62d2bdc4665688261c03a42fd0025/nipype/interfaces/cmtk/nx.py#L85>`__



Combines two dictionaries and adds the values for those keys that are shared


.. _nipype.interfaces.cmtk.nx.add_edge_data:

:func:`add_edge_data`
---------------------

`Link to code <http://github.com/nipy/nipype/tree/e63e055194d62d2bdc4665688261c03a42fd0025/nipype/interfaces/cmtk/nx.py#L319>`__






.. _nipype.interfaces.cmtk.nx.add_node_data:

:func:`add_node_data`
---------------------

`Link to code <http://github.com/nipy/nipype/tree/e63e055194d62d2bdc4665688261c03a42fd0025/nipype/interfaces/cmtk/nx.py#L308>`__






.. _nipype.interfaces.cmtk.nx.average_networks:

:func:`average_networks`
------------------------

`Link to code <http://github.com/nipy/nipype/tree/e63e055194d62d2bdc4665688261c03a42fd0025/nipype/interfaces/cmtk/nx.py#L97>`__



Sums the edges of input networks and divides by the number of networks
Writes the average network as .pck and .gexf and returns the name of the written networks


.. _nipype.interfaces.cmtk.nx.compute_dict_measures:

:func:`compute_dict_measures`
-----------------------------

`Link to code <http://github.com/nipy/nipype/tree/e63e055194d62d2bdc4665688261c03a42fd0025/nipype/interfaces/cmtk/nx.py#L246>`__



Returns a dictionary


.. _nipype.interfaces.cmtk.nx.compute_edge_measures:

:func:`compute_edge_measures`
-----------------------------

`Link to code <http://github.com/nipy/nipype/tree/e63e055194d62d2bdc4665688261c03a42fd0025/nipype/interfaces/cmtk/nx.py#L231>`__



These return edge-based measures


.. _nipype.interfaces.cmtk.nx.compute_network_measures:

:func:`compute_network_measures`
--------------------------------

`Link to code <http://github.com/nipy/nipype/tree/e63e055194d62d2bdc4665688261c03a42fd0025/nipype/interfaces/cmtk/nx.py#L297>`__






.. _nipype.interfaces.cmtk.nx.compute_node_measures:

:func:`compute_node_measures`
-----------------------------

`Link to code <http://github.com/nipy/nipype/tree/e63e055194d62d2bdc4665688261c03a42fd0025/nipype/interfaces/cmtk/nx.py#L192>`__



These return node-based measures


.. _nipype.interfaces.cmtk.nx.compute_singlevalued_measures:

:func:`compute_singlevalued_measures`
-------------------------------------

`Link to code <http://github.com/nipy/nipype/tree/e63e055194d62d2bdc4665688261c03a42fd0025/nipype/interfaces/cmtk/nx.py#L257>`__



Returns a single value per network


.. _nipype.interfaces.cmtk.nx.fix_keys_for_gexf:

:func:`fix_keys_for_gexf`
-------------------------

`Link to code <http://github.com/nipy/nipype/tree/e63e055194d62d2bdc4665688261c03a42fd0025/nipype/interfaces/cmtk/nx.py#L54>`__



GEXF Networks can be read in Gephi, however, the keys for the node and edge IDs must be converted to strings


.. _nipype.interfaces.cmtk.nx.read_unknown_ntwk:

:func:`read_unknown_ntwk`
-------------------------

`Link to code <http://github.com/nipy/nipype/tree/e63e055194d62d2bdc4665688261c03a42fd0025/nipype/interfaces/cmtk/nx.py#L36>`__






.. _nipype.interfaces.cmtk.nx.remove_all_edges:

:func:`remove_all_edges`
------------------------

`Link to code <http://github.com/nipy/nipype/tree/e63e055194d62d2bdc4665688261c03a42fd0025/nipype/interfaces/cmtk/nx.py#L46>`__





