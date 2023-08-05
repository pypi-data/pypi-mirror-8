.. AUTO-GENERATED FILE -- DO NOT EDIT!

interfaces.meshfix
==================


.. _nipype.interfaces.meshfix.MeshFix:


.. index:: MeshFix

MeshFix
-------

`Link to code <http://github.com/nipy/nipype/tree/e63e055194d62d2bdc4665688261c03a42fd0025/nipype/interfaces/meshfix.py#L76>`__

Wraps command **meshfix**

MeshFix v1.2-alpha - by Marco Attene, Mirko Windhoff, Axel Thielscher.

.. seealso::

    http://jmeshlib.sourceforge.net
        Sourceforge page

    http://simnibs.de/installation/meshfixandgetfem
        Ubuntu installation instructions

If MeshFix is used for research purposes, please cite the following paper:
M. Attene - A lightweight approach to repairing digitized polygon meshes.
The Visual Computer, 2010. (c) Springer.

Accepted input formats are OFF, PLY and STL.
Other formats (like .msh for gmsh) are supported only partially.

Example
~~~~~~~

>>> import nipype.interfaces.meshfix as mf
>>> fix = mf.MeshFix()
>>> fix.inputs.in_file1 = 'lh-pial.stl'
>>> fix.inputs.in_file2 = 'rh-pial.stl'
>>> fix.run()                                    # doctest: +SKIP

Inputs::

        [Mandatory]
        in_file1: (an existing file name)
                flag: %s, position: 1
        terminal_output: ('stream' or 'allatonce' or 'file' or 'none')
                Control terminal output: `stream` - displays to terminal
                immediately, `allatonce` - waits till command is finished to display
                output, `file` - writes output to file, `none` - output is ignored

        [Optional]
        args: (a string)
                Additional parameters to the command
                flag: %s
        cut_inner: (an integer)
                Remove triangles of 1st that are inside of the 2nd shell. Dilate 2nd
                by N; Fill holes and keep only 1st afterwards.
                flag: --cut-inner %d
        cut_outer: (an integer)
                Remove triangles of 1st that are outside of the 2nd shell.
                flag: --cut-outer %d
        decouple_inin: (an integer)
                Treat 1st file as inner, 2nd file as outer component.Resolve
                overlaps by moving inners triangles inwards. Constrain the min
                distance between the components > d.
                flag: --decouple-inin %d
        decouple_outin: (an integer)
                Treat 1st file as outer, 2nd file as inner component.Resolve
                overlaps by moving outers triangles inwards. Constrain the min
                distance between the components > d.
                flag: --decouple-outin %d
        decouple_outout: (an integer)
                Treat 1st file as outer, 2nd file as inner component.Resolve
                overlaps by moving outers triangles outwards. Constrain the min
                distance between the components > d.
                flag: --decouple-outout %d
        dilation: (an integer)
                Dilate the surface by d. d < 0 means shrinking.
                flag: --dilate %d
        dont_clean: (a boolean)
                Don't Clean
                flag: --no-clean
        environ: (a dictionary with keys which are a value of type 'str' and
                 with values which are a value of type 'str', nipype default value:
                 {})
                Environment variables
        epsilon_angle: (0.0 <= a floating point number <= 2.0)
                Epsilon angle in degrees (must be between 0 and 2)
                flag: -a %f
        finetuning_distance: (a float)
                Used to fine-tune the minimal distance between surfaces.A minimal
                distance d is ensured, and reached in n substeps. When using the
                surfaces for subsequent volume meshing by gmsh, this step prevent
                too flat tetrahedra2)
                flag: %f
                requires: finetuning_substeps
        finetuning_inwards: (a boolean)
                flag: --fineTuneIn
                requires: finetuning_distance, finetuning_substeps
        finetuning_outwards: (a boolean)
                Similar to finetuning_inwards, but ensures minimal distance in the
                other direction
                flag: --fineTuneIn
                mutually_exclusive: finetuning_inwards
                requires: finetuning_distance, finetuning_substeps
        finetuning_substeps: (an integer)
                Used to fine-tune the minimal distance between surfaces.A minimal
                distance d is ensured, and reached in n substeps. When using the
                surfaces for subsequent volume meshing by gmsh, this step prevent
                too flat tetrahedra2)
                flag: %d
                requires: finetuning_distance
        ignore_exception: (a boolean, nipype default value: False)
                Print an error message instead of throwing an exception in case the
                interface fails to run
        in_file2: (an existing file name)
                flag: %s, position: 2
        join_closest_components: (a boolean)
                Join the closest pair of components.
                flag: -jc
                mutually_exclusive: join_closest_components
        join_overlapping_largest_components: (a boolean)
                Join 2 biggest components if they overlap, remove the rest.
                flag: -j
                mutually_exclusive: join_closest_components
        laplacian_smoothing_steps: (an integer)
                The number of laplacian smoothing steps to apply
                flag: --smooth %d
        number_of_biggest_shells: (an integer)
                Only the N biggest shells are kept
                flag: --shells %d
        out_filename: (a file name)
                The output filename for the fixed mesh file
                flag: -o %s
        output_type: ('stl' or 'msh' or 'wrl' or 'vrml' or 'fs' or 'off',
                 nipype default value: off)
                The output type to save the file as.
        quiet_mode: (a boolean)
                Quiet mode, don't write much to stdout.
                flag: -q
        remove_handles: (a boolean)
                Remove handles
                flag: --remove-handles
        save_as_freesurfer_mesh: (a boolean)
                Result is saved in freesurfer mesh format
                flag: --fsmesh
                mutually_exclusive: save_as_vrml, save_as_stl
        save_as_stl: (a boolean)
                Result is saved in stereolithographic format (.stl)
                flag: --stl
                mutually_exclusive: save_as_vmrl, save_as_freesurfer_mesh
        save_as_vmrl: (a boolean)
                Result is saved in VRML1.0 format (.wrl)
                flag: --wrl
                mutually_exclusive: save_as_stl, save_as_freesurfer_mesh
        set_intersections_to_one: (a boolean)
                If the mesh contains intersections, return value = 1.If saved in
                gmsh format, intersections will be highlighted.
                flag: --intersect
        uniform_remeshing_steps: (an integer)
                Number of steps for uniform remeshing of the whole mesh
                flag: -u %d
                requires: uniform_remeshing_vertices
        uniform_remeshing_vertices: (an integer)
                Constrains the number of vertices.Must be used with
                uniform_remeshing_steps
                flag: --vertices %d
                requires: uniform_remeshing_steps
        x_shift: (an integer)
                Shifts the coordinates of the vertices when saving. Output must be
                in FreeSurfer format
                flag: --smooth %d

Outputs::

        mesh_file: (an existing file name)
                The output mesh file
