.. AUTO-GENERATED FILE -- DO NOT EDIT!

interfaces.cmtk.nbs
===================


.. _nipype.interfaces.cmtk.nbs.NetworkBasedStatistic:


.. index:: NetworkBasedStatistic

NetworkBasedStatistic
---------------------

`Link to code <http://github.com/nipy/nipype/tree/e63e055194d62d2bdc4665688261c03a42fd0025/nipype/interfaces/cmtk/nbs.py#L56>`__

Calculates and outputs the average network given a set of input NetworkX gpickle files

For documentation of Network-based statistic parameters:

        https://github.com/LTS5/connectomeviewer/blob/master/cviewer/libs/pyconto/groupstatistics/nbs/_nbs.py

Example
~~~~~~~

>>> import nipype.interfaces.cmtk as cmtk
>>> nbs = cmtk.NetworkBasedStatistic()
>>> nbs.inputs.in_group1 = ['subj1.pck', 'subj2.pck'] # doctest: +SKIP
>>> nbs.inputs.in_group2 = ['pat1.pck', 'pat2.pck'] # doctest: +SKIP
>>> nbs.run()                 # doctest: +SKIP

Inputs::

        [Mandatory]
        in_group1: (an existing file name)
                Networks for the first group of subjects
        in_group2: (an existing file name)
                Networks for the second group of subjects

        [Optional]
        edge_key: (a string, nipype default value: number_of_fibers)
                Usually "number_of_fibers, "fiber_length_mean", "fiber_length_std"
                for matrices made with CMTKSometimes "weight" or "value" for
                functional networks.
        ignore_exception: (a boolean, nipype default value: False)
                Print an error message instead of throwing an exception in case the
                interface fails to run
        node_position_network: (a file name)
                An optional network used to position the nodes for the output
                networks
        number_of_permutations: (an integer, nipype default value: 1000)
                Number of permutations to perform
        out_nbs_network: (a file name)
                Output network with edges identified by the NBS
        out_nbs_pval_network: (a file name)
                Output network with p-values to weight the edges identified by the
                NBS
        t_tail: ('left' or 'right' or 'both', nipype default value: left)
                Can be one of "left", "right", or "both"
        threshold: (a float, nipype default value: 3)
                T-statistic threshold

Outputs::

        nbs_network: (an existing file name)
                Output network with edges identified by the NBS
        nbs_pval_network: (an existing file name)
                Output network with p-values to weight the edges identified by the
                NBS
        network_files: (an existing file name)
                Output network with edges identified by the NBS

.. module:: nipype.interfaces.cmtk.nbs


.. _nipype.interfaces.cmtk.nbs.ntwks_to_matrices:

:func:`ntwks_to_matrices`
-------------------------

`Link to code <http://github.com/nipy/nipype/tree/e63e055194d62d2bdc4665688261c03a42fd0025/nipype/interfaces/cmtk/nbs.py#L24>`__





