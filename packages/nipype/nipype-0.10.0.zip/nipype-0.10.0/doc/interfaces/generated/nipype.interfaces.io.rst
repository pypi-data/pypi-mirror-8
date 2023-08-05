.. AUTO-GENERATED FILE -- DO NOT EDIT!

interfaces.io
=============


.. _nipype.interfaces.io.DataFinder:


.. index:: DataFinder

DataFinder
----------

`Link to code <http://github.com/nipy/nipype/tree/e63e055194d62d2bdc4665688261c03a42fd0025/nipype/interfaces/io.py#L732>`__

Search for paths that match a given regular expression. Allows a less
proscriptive approach to gathering input files compared to DataGrabber.
Will recursively search any subdirectories by default. This can be limited
with the min/max depth options.
Matched paths are available in the output 'out_paths'. Any named groups of
captured text from the regular expression are also available as ouputs of
the same name.

Examples
~~~~~~~~

>>> from nipype.interfaces.io import DataFinder
>>> df = DataFinder()
>>> df.inputs.root_paths = '.'
>>> df.inputs.match_regex = '.+/(?P<series_dir>.+(qT1|ep2d_fid_T1).+)/(?P<basename>.+)\.nii.gz'
>>> result = df.run() # doctest: +SKIP
>>> print result.outputs.out_paths # doctest: +SKIP
['./027-ep2d_fid_T1_Gd4/acquisition.nii.gz',
 './018-ep2d_fid_T1_Gd2/acquisition.nii.gz',
 './016-ep2d_fid_T1_Gd1/acquisition.nii.gz',
 './013-ep2d_fid_T1_pre/acquisition.nii.gz']
>>> print result.outputs.series_dir # doctest: +SKIP
['027-ep2d_fid_T1_Gd4',
 '018-ep2d_fid_T1_Gd2',
 '016-ep2d_fid_T1_Gd1',
 '013-ep2d_fid_T1_pre']
>>> print result.outputs.basename # doctest: +SKIP
['acquisition',
 'acquisition'
 'acquisition',
 'acquisition']

Inputs::

        [Mandatory]
        root_paths: (a list of items which are any value or a string)

        [Optional]
        ignore_exception: (a boolean, nipype default value: False)
                Print an error message instead of throwing an exception in case the
                interface fails to run
        ignore_regexes: (a list of items which are any value)
                List of regular expressions, if any match the path it will be
                ignored.
        match_regex: (a string, nipype default value: (.+))
                Regular expression for matching paths.
        max_depth: (an integer)
                The maximum depth to search beneath the root_paths
        min_depth: (an integer)
                The minimum depth to search beneath the root paths
        unpack_single: (a boolean, nipype default value: False)
                Unpack single results from list

Outputs::

        None

.. _nipype.interfaces.io.DataGrabber:


.. index:: DataGrabber

DataGrabber
-----------

`Link to code <http://github.com/nipy/nipype/tree/e63e055194d62d2bdc4665688261c03a42fd0025/nipype/interfaces/io.py#L381>`__

Generic datagrabber module that wraps around glob in an
intelligent way for neuroimaging tasks to grab files


.. attention::

   Doesn't support directories currently

Examples
~~~~~~~~

>>> from nipype.interfaces.io import DataGrabber

Pick all files from current directory

>>> dg = DataGrabber()
>>> dg.inputs.template = '*'

Pick file foo/foo.nii from current directory

>>> dg.inputs.template = '%s/%s.dcm'
>>> dg.inputs.template_args['outfiles']=[['dicomdir','123456-1-1.dcm']]

Same thing but with dynamically created fields

>>> dg = DataGrabber(infields=['arg1','arg2'])
>>> dg.inputs.template = '%s/%s.nii'
>>> dg.inputs.arg1 = 'foo'
>>> dg.inputs.arg2 = 'foo'

however this latter form can be used with iterables and iterfield in a
pipeline.

Dynamically created, user-defined input and output fields

>>> dg = DataGrabber(infields=['sid'], outfields=['func','struct','ref'])
>>> dg.inputs.base_directory = '.'
>>> dg.inputs.template = '%s/%s.nii'
>>> dg.inputs.template_args['func'] = [['sid',['f3','f5']]]
>>> dg.inputs.template_args['struct'] = [['sid',['struct']]]
>>> dg.inputs.template_args['ref'] = [['sid','ref']]
>>> dg.inputs.sid = 's1'

Change the template only for output field struct. The rest use the
general template

>>> dg.inputs.field_template = dict(struct='%s/struct.nii')
>>> dg.inputs.template_args['struct'] = [['sid']]

Inputs::

        [Mandatory]
        sort_filelist: (a boolean)
                Sort the filelist that matches the template
        template: (a string)
                Layout used to get files. relative to base directory if defined

        [Optional]
        base_directory: (an existing directory name)
                Path to the base directory consisting of subject data.
        ignore_exception: (a boolean, nipype default value: False)
                Print an error message instead of throwing an exception in case the
                interface fails to run
        raise_on_empty: (a boolean, nipype default value: True)
                Generate exception if list is empty for a given field
        template_args: (a dictionary with keys which are a string and with
                 values which are a list of items which are a list of items which
                 are any value)
                Information to plug into template

Outputs::

        None

.. _nipype.interfaces.io.DataSink:


.. index:: DataSink

DataSink
--------

`Link to code <http://github.com/nipy/nipype/tree/e63e055194d62d2bdc4665688261c03a42fd0025/nipype/interfaces/io.py#L162>`__

Generic datasink module to store structured outputs

Primarily for use within a workflow. This interface allows arbitrary
creation of input attributes. The names of these attributes define the
directory structure to create for storage of the files or directories.

The attributes take the following form:

string[[.[@]]string[[.[@]]string]] ...

where parts between [] are optional.

An attribute such as contrasts.@con will create a 'contrasts' directory
to store the results linked to the attribute. If the @ is left out, such
as in 'contrasts.con', a subdirectory 'con' will be created under
'contrasts'.

the general form of the output is::

   'base_directory/container/parameterization/destloc/filename'

   destloc = string[[.[@]]string[[.[@]]string]] and
   filename comesfrom the input to the connect statement.

.. warning::

    This is not a thread-safe node because it can write to a common
    shared location. It will not complain when it overwrites a file.

.. note::

    If both substitutions and regexp_substitutions are used, then
    substitutions are applied first followed by regexp_substitutions.

    This interface **cannot** be used in a MapNode as the inputs are
    defined only when the connect statement is executed.

Examples
~~~~~~~~

>>> ds = DataSink()
>>> ds.inputs.base_directory = 'results_dir'
>>> ds.inputs.container = 'subject'
>>> ds.inputs.structural = 'structural.nii'
>>> setattr(ds.inputs, 'contrasts.@con', ['cont1.nii', 'cont2.nii'])
>>> setattr(ds.inputs, 'contrasts.alt', ['cont1a.nii', 'cont2a.nii'])
>>> ds.run() # doctest: +SKIP

To use DataSink in a MapNode, its inputs have to be defined at the
time the interface is created.

>>> ds = DataSink(infields=['contasts.@con'])
>>> ds.inputs.base_directory = 'results_dir'
>>> ds.inputs.container = 'subject'
>>> ds.inputs.structural = 'structural.nii'
>>> setattr(ds.inputs, 'contrasts.@con', ['cont1.nii', 'cont2.nii'])
>>> setattr(ds.inputs, 'contrasts.alt', ['cont1a.nii', 'cont2a.nii'])
>>> ds.run() # doctest: +SKIP

Inputs::

        [Mandatory]

        [Optional]
        _outputs: (a dictionary with keys which are a string and with values
                 which are any value, nipype default value: {})
        base_directory: (a directory name)
                Path to the base directory for storing data.
        container: (a string)
                Folder within base directory in which to store output
        ignore_exception: (a boolean, nipype default value: False)
                Print an error message instead of throwing an exception in case the
                interface fails to run
        parameterization: (a boolean, nipype default value: True)
                store output in parametrized structure
        regexp_substitutions: (a tuple of the form: (a string, a string))
                List of 2-tuples reflecting a pair of a Python regexp pattern and a
                replacement string. Invoked after string `substitutions`
        remove_dest_dir: (a boolean, nipype default value: False)
                remove dest directory when copying dirs
        strip_dir: (a directory name)
                path to strip out of filename
        substitutions: (a tuple of the form: (a string, a string))
                List of 2-tuples reflecting string to substitute and string to
                replace it with

Outputs::

        out_file
                datasink output

.. _nipype.interfaces.io.FreeSurferSource:


.. index:: FreeSurferSource

FreeSurferSource
----------------

`Link to code <http://github.com/nipy/nipype/tree/e63e055194d62d2bdc4665688261c03a42fd0025/nipype/interfaces/io.py#L947>`__

Generates freesurfer subject info from their directories

Examples
~~~~~~~~

>>> from nipype.interfaces.io import FreeSurferSource
>>> fs = FreeSurferSource()
>>> #fs.inputs.subjects_dir = '.'
>>> fs.inputs.subject_id = 'PWS04'
>>> res = fs.run() # doctest: +SKIP

>>> fs.inputs.hemi = 'lh'
>>> res = fs.run() # doctest: +SKIP

Inputs::

        [Mandatory]
        subject_id: (a string)
                Subject name for whom to retrieve data
        subjects_dir: (a directory name)
                Freesurfer subjects directory.

        [Optional]
        hemi: ('both' or 'lh' or 'rh', nipype default value: both)
                Selects hemisphere specific outputs
        ignore_exception: (a boolean, nipype default value: False)
                Print an error message instead of throwing an exception in case the
                interface fails to run

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

.. _nipype.interfaces.io.IOBase:


.. index:: IOBase

IOBase
------

`Link to code <http://github.com/nipy/nipype/tree/e63e055194d62d2bdc4665688261c03a42fd0025/nipype/interfaces/io.py#L109>`__

Inputs::

        [Mandatory]

        [Optional]
        ignore_exception: (a boolean, nipype default value: False)
                Print an error message instead of throwing an exception in case the
                interface fails to run

Outputs::

        None

.. _nipype.interfaces.io.MySQLSink:


.. index:: MySQLSink

MySQLSink
---------

`Link to code <http://github.com/nipy/nipype/tree/e63e055194d62d2bdc4665688261c03a42fd0025/nipype/interfaces/io.py#L1505>`__

Very simple frontend for storing values into MySQL database.

Examples
~~~~~~~~

>>> sql = MySQLSink(input_names=['subject_id', 'some_measurement'])
>>> sql.inputs.database_name = 'my_database'
>>> sql.inputs.table_name = 'experiment_results'
>>> sql.inputs.username = 'root'
>>> sql.inputs.password = 'secret'
>>> sql.inputs.subject_id = 's1'
>>> sql.inputs.some_measurement = 11.4
>>> sql.run() # doctest: +SKIP

Inputs::

        [Mandatory]
        config: (a file name)
                MySQL Options File (same format as my.cnf)
                mutually_exclusive: host
        database_name: (a string)
                Otherwise known as the schema name
        host: (a string, nipype default value: localhost)
                mutually_exclusive: config
                requires: username, password
        table_name: (a string)

        [Optional]
        ignore_exception: (a boolean, nipype default value: False)
                Print an error message instead of throwing an exception in case the
                interface fails to run
        password: (a string)
        username: (a string)

Outputs::

        None

.. _nipype.interfaces.io.SQLiteSink:


.. index:: SQLiteSink

SQLiteSink
----------

`Link to code <http://github.com/nipy/nipype/tree/e63e055194d62d2bdc4665688261c03a42fd0025/nipype/interfaces/io.py#L1449>`__

Very simple frontend for storing values into SQLite database.

.. warning::

    This is not a thread-safe node because it can write to a common
    shared location. It will not complain when it overwrites a file.

Examples
~~~~~~~~

>>> sql = SQLiteSink(input_names=['subject_id', 'some_measurement'])
>>> sql.inputs.database_file = 'my_database.db'
>>> sql.inputs.table_name = 'experiment_results'
>>> sql.inputs.subject_id = 's1'
>>> sql.inputs.some_measurement = 11.4
>>> sql.run() # doctest: +SKIP

Inputs::

        [Mandatory]
        database_file: (an existing file name)
        table_name: (a string)

        [Optional]
        ignore_exception: (a boolean, nipype default value: False)
                Print an error message instead of throwing an exception in case the
                interface fails to run

Outputs::

        None

.. _nipype.interfaces.io.SSHDataGrabber:


.. index:: SSHDataGrabber

SSHDataGrabber
--------------

`Link to code <http://github.com/nipy/nipype/tree/e63e055194d62d2bdc4665688261c03a42fd0025/nipype/interfaces/io.py#L1565>`__

Extension of DataGrabber module that downloads the file list and
optionally the files from a SSH server. The SSH operation must
not need user and password so an SSH agent must be active in
where this module is being run.


.. attention::

   Doesn't support directories currently

Examples
~~~~~~~~

>>> from nipype.interfaces.io import SSHDataGrabber
>>> dg = SSHDataGrabber()
>>> dg.inputs.hostname = 'test.rebex.net'
>>> dg.inputs.user = 'demo'
>>> dg.inputs.password = 'password'
>>> dg.inputs.base_directory = 'pub/example'

Pick all files from the base directory

>>> dg.inputs.template = '*'

Pick all files starting with "s" and a number from current directory

>>> dg.inputs.template_expression = 'regexp'
>>> dg.inputs.template = 'pop[0-9].*'

Same thing but with dynamically created fields

>>> dg = SSHDataGrabber(infields=['arg1','arg2'])
>>> dg.inputs.hostname = 'test.rebex.net'
>>> dg.inputs.user = 'demo'
>>> dg.inputs.password = 'password'
>>> dg.inputs.base_directory = 'pub'
>>> dg.inputs.template = '%s/%s.txt'
>>> dg.inputs.arg1 = 'example'
>>> dg.inputs.arg2 = 'foo'

however this latter form can be used with iterables and iterfield in a
pipeline.

Dynamically created, user-defined input and output fields

>>> dg = SSHDataGrabber(infields=['sid'], outfields=['func','struct','ref'])
>>> dg.inputs.hostname = 'myhost.com'
>>> dg.inputs.base_directory = '/main_folder/my_remote_dir'
>>> dg.inputs.template_args['func'] = [['sid',['f3','f5']]]
>>> dg.inputs.template_args['struct'] = [['sid',['struct']]]
>>> dg.inputs.template_args['ref'] = [['sid','ref']]
>>> dg.inputs.sid = 's1'

Change the template only for output field struct. The rest use the
general template

>>> dg.inputs.field_template = dict(struct='%s/struct.nii')
>>> dg.inputs.template_args['struct'] = [['sid']]

Inputs::

        [Mandatory]
        base_directory: (a string)
                Path to the base directory consisting of subject data.
        hostname: (a string)
                Server hostname.
        sort_filelist: (a boolean)
                Sort the filelist that matches the template
        template: (a string)
                Layout used to get files. relative to base directory if defined

        [Optional]
        download_files: (a boolean, nipype default value: True)
                If false it will return the file names without downloading them
        ignore_exception: (a boolean, nipype default value: False)
                Print an error message instead of throwing an exception in case the
                interface fails to run
        password: (a string)
                Server password.
        raise_on_empty: (a boolean, nipype default value: True)
                Generate exception if list is empty for a given field
        ssh_log_to_file: (a string, nipype default value: )
                If set SSH commands will be logged to the given file
        template_args: (a dictionary with keys which are a string and with
                 values which are a list of items which are a list of items which
                 are any value)
                Information to plug into template
        template_expression: ('fnmatch' or 'regexp', nipype default value:
                 fnmatch)
                Use either fnmatch or regexp to express templates
        username: (a string)
                Server username.

Outputs::

        None

.. _nipype.interfaces.io.SelectFiles:


.. index:: SelectFiles

SelectFiles
-----------

`Link to code <http://github.com/nipy/nipype/tree/e63e055194d62d2bdc4665688261c03a42fd0025/nipype/interfaces/io.py#L584>`__

Flexibly collect data from disk to feed into workflows.

This interface uses the {}-based string formatting syntax to plug
values (possibly known only at workflow execution time) into string
templates and collect files from persistant storage. These templates
can also be combined with glob wildcards. The field names in the
formatting template (i.e. the terms in braces) will become inputs
fields on the interface, and the keys in the templates dictionary
will form the output fields.

Examples
~~~~~~~~

>>> from nipype import SelectFiles, Node
>>> templates={"T1": "{subject_id}/struct/T1.nii",
...            "epi": "{subject_id}/func/f[0, 1].nii"}
>>> dg = Node(SelectFiles(templates), "selectfiles")
>>> dg.inputs.subject_id = "subj1"
>>> dg.outputs.get()
{'T1': <undefined>, 'epi': <undefined>}

The same thing with dynamic grabbing of specific files:

>>> templates["epi"] = "{subject_id}/func/f{run!s}.nii"
>>> dg = Node(SelectFiles(templates), "selectfiles")
>>> dg.inputs.subject_id = "subj1"
>>> dg.inputs.run = [2, 4]

Inputs::

        [Mandatory]

        [Optional]
        base_directory: (an existing directory name)
                Root path common to templates.
        force_lists: (a boolean or a list of items which are a string, nipype
                 default value: False)
                Whether to return outputs as a list even when only one file matches
                the template. Either a boolean that applies to all output fields or
                a list of output field names to coerce to a list
        ignore_exception: (a boolean, nipype default value: False)
                Print an error message instead of throwing an exception in case the
                interface fails to run
        raise_on_empty: (a boolean, nipype default value: True)
                Raise an exception if a template pattern matches no files.
        sort_filelist: (a boolean, nipype default value: True)
                When matching mutliple files, return them in sorted order.

Outputs::

        None

.. _nipype.interfaces.io.XNATSink:


.. index:: XNATSink

XNATSink
--------

`Link to code <http://github.com/nipy/nipype/tree/e63e055194d62d2bdc4665688261c03a42fd0025/nipype/interfaces/io.py#L1266>`__

Generic datasink module that takes a directory containing a
list of nifti files and provides a set of structured output
fields.

Inputs::

        [Mandatory]
        config: (a file name)
                mutually_exclusive: server
        experiment_id: (a string)
                Set to workflow name
        project_id: (a string)
                Project in which to store the outputs
        server: (a string)
                mutually_exclusive: config
                requires: user, pwd
        subject_id: (a string)
                Set to subject id

        [Optional]
        _outputs: (a dictionary with keys which are a string and with values
                 which are any value, nipype default value: {})
        assessor_id: (a string)
                Option to customize ouputs representation in XNAT - assessor level
                will be used with specified id
                mutually_exclusive: reconstruction_id
        cache_dir: (a directory name)
        ignore_exception: (a boolean, nipype default value: False)
                Print an error message instead of throwing an exception in case the
                interface fails to run
        pwd: (a string)
        reconstruction_id: (a string)
                Option to customize ouputs representation in XNAT - reconstruction
                level will be used with specified id
                mutually_exclusive: assessor_id
        share: (a boolean, nipype default value: False)
                Option to share the subjects from the original projectinstead of
                creating new ones when possible - the created experiments are then
                shared back to the original project
        user: (a string)

Outputs::

        None

.. _nipype.interfaces.io.XNATSource:


.. index:: XNATSource

XNATSource
----------

`Link to code <http://github.com/nipy/nipype/tree/e63e055194d62d2bdc4665688261c03a42fd0025/nipype/interfaces/io.py#L1031>`__

Generic XNATSource module that wraps around the pyxnat module in
an intelligent way for neuroimaging tasks to grab files and data
from an XNAT server.

Examples
~~~~~~~~

>>> from nipype.interfaces.io import XNATSource

Pick all files from current directory

>>> dg = XNATSource()
>>> dg.inputs.template = '*'

>>> dg = XNATSource(infields=['project','subject','experiment','assessor','inout'])
>>> dg.inputs.query_template = '/projects/%s/subjects/%s/experiments/%s'                    '/assessors/%s/%s_resources/files'
>>> dg.inputs.project = 'IMAGEN'
>>> dg.inputs.subject = 'IMAGEN_000000001274'
>>> dg.inputs.experiment = '*SessionA*'
>>> dg.inputs.assessor = '*ADNI_MPRAGE_nii'
>>> dg.inputs.inout = 'out'

>>> dg = XNATSource(infields=['sid'],outfields=['struct','func'])
>>> dg.inputs.query_template = '/projects/IMAGEN/subjects/%s/experiments/*SessionA*'                    '/assessors/*%s_nii/out_resources/files'
>>> dg.inputs.query_template_args['struct'] = [['sid','ADNI_MPRAGE']]
>>> dg.inputs.query_template_args['func'] = [['sid','EPI_faces']]
>>> dg.inputs.sid = 'IMAGEN_000000001274'

Inputs::

        [Mandatory]
        config: (a file name)
                mutually_exclusive: server
        query_template: (a string)
                Layout used to get files. Relative to base directory if defined
        server: (a string)
                mutually_exclusive: config
                requires: user, pwd

        [Optional]
        cache_dir: (a directory name)
                Cache directory
        ignore_exception: (a boolean, nipype default value: False)
                Print an error message instead of throwing an exception in case the
                interface fails to run
        pwd: (a string)
        query_template_args: (a dictionary with keys which are a string and
                 with values which are a list of items which are a list of items
                 which are any value, nipype default value: {'outfiles': []})
                Information to plug into template
        user: (a string)

Outputs::

        None

.. module:: nipype.interfaces.io


.. _nipype.interfaces.io.add_traits:

:func:`add_traits`
------------------

`Link to code <http://github.com/nipy/nipype/tree/e63e055194d62d2bdc4665688261c03a42fd0025/nipype/interfaces/io.py#L91>`__



Add traits to a traited class.

All traits are set to Undefined by default


.. _nipype.interfaces.io.copytree:

:func:`copytree`
----------------

`Link to code <http://github.com/nipy/nipype/tree/e63e055194d62d2bdc4665688261c03a42fd0025/nipype/interfaces/io.py#L56>`__



Recursively copy a directory tree using
nipype.utils.filemanip.copyfile()

This is not a thread-safe routine. However, in the case of creating new
directories, it checks to see if a particular directory has already been
created by another process.


.. _nipype.interfaces.io.push_file:

:func:`push_file`
-----------------

`Link to code <http://github.com/nipy/nipype/tree/e63e055194d62d2bdc4665688261c03a42fd0025/nipype/interfaces/io.py#L1358>`__






.. _nipype.interfaces.io.quote_id:

:func:`quote_id`
----------------

`Link to code <http://github.com/nipy/nipype/tree/e63e055194d62d2bdc4665688261c03a42fd0025/nipype/interfaces/io.py#L1350>`__






.. _nipype.interfaces.io.unquote_id:

:func:`unquote_id`
------------------

`Link to code <http://github.com/nipy/nipype/tree/e63e055194d62d2bdc4665688261c03a42fd0025/nipype/interfaces/io.py#L1354>`__





