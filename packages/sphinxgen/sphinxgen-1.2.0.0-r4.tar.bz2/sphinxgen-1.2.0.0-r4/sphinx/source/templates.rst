Jinja Template Contexts
=========================

|SPHINXGEN| uses `jinja`_ templates for generating the output files.

There are three types of files generated, each has its own template:
:ref:`package <template-package>` files,
:ref:`module <template-module>` files, and :ref:`index <template-index>`
files. The following sections describe the
template contexts available for each type of file:

.. _template-package:

The Package Template
----------------------

The :dfn:`package` files are used for python packages, which are directories
that contain an :file:`__init__.py` file. Packages may contain
:ref:`modules <template-module>` as well as subpackages. The purpose of the
package file is generally to document the top-level contents of the package
(i.e., objects in the packages :file:`__init__.py` module) and link to the
documentation for the contained modules and sub packages. Alternatively,
you can use the :std:option:`--no-modules <sphinxgen --no-modules>` option to supress
generation of individual module files, and document the modules directly in the
package documentation file.

The context for the package template is a dictionary describing the package itself.
The following variables are defined for use in the template:

.. py:data:: name

    The base name of the package, without any hierarchical information. This is simply
    the name of the package directory. For instance, the `name` of package ``foo.bar.baz``
    is simply ``'baz'``.

.. py:data:: doc_name

    The name of the document being generated. This is the basename of the file,
    without extension (:file:`.rst`) or directory. This includes any prefix
    specified by the :std:option:`--prefix <sphinxgen --prefix>` option.

.. py:data:: package

    The fully qualified name of the parent package, if there is any, or ``None``
    if this appears to be a top-level package. For instance, for package ``foo.bar.baz``,
    this value with be ``'foo.bar'``, where as for package ``foo``, it would be ``None``.

    Note that we don't actually search the file system for parent packages, packages
    that were specified as a ``PACKAGE_DIR``
    on the command line are assumed to be top-level packages.

.. py:data:: fullname

    This is simply the fully qualified name of the package, which includes the
    package's base `name` and it's parent `package`. For ``foo.bar.baz``, this would
    be ``'foo.bar.baz'``.

.. py:data:: path

    The filesystem path for where this directory is defined. These are derived from
    the ``PACKAGE_DIR`` values specified on the command
    line, and are not resolved to absolute or normalized paths.

.. py:data:: modules

    A list of dictionaries describing each of the modules contained in this package.
    These are the same objects that will be used as the context for the
    :ref:`module template <template-module>`; see that section for a description
    of these objects.

    Note that the order of the list is arbitrary, so you may want to sort it.
    Also note that this only contains immediate children of the package, no
    deeper descendants.

.. py:data:: sub_packages

    A list of dictionaries describing each of the sub-packages contained in this
    package. These are the same objects that provide the context for the
    package template to generate the files for those packages, so they have the
    same structure as this dictionary itself.

    Note that the order of the list is arbitrary, so you may want to sort it.
    Also note that this only contains immediate children of the package, no
    deeper descendants.

.. py:data:: children

    For convenience, this field is a concatenation of `sub_packages` and `modules`.


.. _template-module:

The Module Template
---------------------

The :dfn:`module` files are used to document individual python modules, each of
which corresponds to a single python source file.

Basic information about each module is placed in a dictionary which provides the
context for this template. The same dictionary is also used to represent the module
in the `modules` member of the `package <template-package>` template context.

The following variables are defined for use in the template (note that these
are all essentially duplicates of the fields in the `package context <template-package>`):

.. py:data:: name

    The base name of the module, without any hierarchical information. This is simply
    the base name of the module's file. For instance, the `name` of module ``foo.bar.baz``
    is simply ``'baz'``.

.. py:data:: doc_name

    The name of the document being generated. This is the basename of the file,
    without extension (:file:`.rst`) or directory. This includes any prefix
    specified by the :std:option:`--prefix <sphinxgen --prefix>` option.

.. py:data:: package

    The fully qualified name of the parent package. For instance, for module ``foo.bar.baz``,
    this value with be ``'foo.bar'``.

.. py:data:: fullname

    This is simply the fully qualified name of the module, which includes the
    modules's base `name` and it's parent `package`. For ``foo.bar.baz``, this would
    be ``'foo.bar.baz'``.

.. py:data:: path

    The filesystem path to this module's source file.
    These are derived from the ``PACKAGE_DIR``
    values specified on the command line, and are not resolved to absolute or
    normalized paths.

.. _template-index:

The Index Template
---------------------

A single :dfn:`index` file is generated by an invocation of |sphinxgen|. It's intended
purpose is to create a :rst:dir:`toctree` for all of the top-level packages specified
on the command line. It can also be used to provide high-level information about the
project if appropriate.

There is only a single variable defined for this template:

.. py:data:: packages

    A list of all the top-level packages processed by |sphinxgen|. Each element is
    a dictionary describing the package, as documented under the `package <template-package>`
    section, above. These appear in the same order as they were specified on
    the command line.

