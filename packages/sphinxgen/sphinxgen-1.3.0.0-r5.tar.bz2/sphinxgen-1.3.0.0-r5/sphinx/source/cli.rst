
.. program:: sphinxgen

Basic Usage
=========================

The most basic usage is to simple invoke |sphinxgen| from the command line, passing
as arguments the file-system path to whatever python package you want to generate
files for. Note that a python package is a directory containing an :file:`__init__.py`
file.

.. code:: bash

    > sphinxgen src/python/my_package

The program will generate a file for the package, plus one 
file for each module it finds in the package. Additionally, if the package contains any
subpackages, it will recurse into those packages as well, generating one file for each 
package and one file for each module. Lastly, it will generate an index file to summarize
all of the top-level packages it processed.

If you want to generate files for multiple packages, specify each package as an argument:

.. code:: bash

    > sphinxgen src/python/my_package src/python/another_package src/python/etc

To control the directory where the files are generated, use the :std:option:`--output`
option:

.. code:: bash

    > sphinxgen --output sphinx-files src/python/my_package

Template Files
--------------------

Output is based on templates, specifically jinja_ templates. There is a separate template
file for packages, modules, and the index. By default, there are internal templates
built into the program which are used, but you can override any or all of these with
your own template files using the :option:`--package-templte`,
:option:`--module-template`, and :option:`--index-template` options.

Additionally, each individual generated file can have its own template by creating a template
file of the same name inside the :option:`template directory <--template-dir>`. This is useful
for having custom files for certain modules or packages. Watch the output of the command
to see the names of the files it generates.

Note that since there is only one index file, it always uses the template specified by the
:option:`--index-template` option (or the built-in index template if this option is not given).
This is true even if there is a file in the template-directory which has the same name as
the generated index file (e.g., as specified by the :option:`--index` option).

For more information on writing template files, see :doc:`templates`.

Example Usages
-------------------------
.. code:: bash

    > PACKAGE_1=src/python/frob
    > PACkAGE_2=src/python/baz
    > ls -R $PACKAGE_1
    src/python/frob:
    __init__.py  frobnicate.py  version.py

    > ls -R $PACKAGE_2
    src/python/baz:
    __init__.py  foo  util.py  version.py

    src/python/baz/foo:
    __init__.py  bar.py

    > sphinxgen -o sphinx/source --prefix code_ $PACKAGE_1 $PACKAGE_2
    sphinxgen: Generating sphinx\source\code_frob.rst
    sphinxgen: Generating sphinx\source\code_frob.frobnicate.rst
    sphinxgen: Generating sphinx\source\code_frob.version.rst
    sphinxgen: Generating sphinx\source\code_baz.foo.rst
    sphinxgen: Generating sphinx\source\code_baz.foo.bar.rst
    sphinxgen: Generating sphinx\source\code_baz.rst
    sphinxgen: Generating sphinx\source\code_baz.util.rst
    sphinxgen: Generating sphinx\source\code_baz.version.rst
    sphinxgen: Generating sphinx\source\code_index.rst

    > TEMPLATE_DIR=sphinx/source/_sphinxgen
    > mkdir $TEMPLATE_DIR
    > touch $TEMPLATE_DIR/code_baz.util.rst
    > sphinxgen -o sphinx/source --prefix code_ --overwrite \
        --template-dir $TEMPLATE_DIR $PACKAGE_1 $PACKAGE_2
    sphinxgen: Generating sphinx\source\code_frob.rst
    sphinxgen: Generating sphinx\source\code_frob.frobnicate.rst
    sphinxgen: Generating sphinx\source\code_frob.version.rst
    sphinxgen: Generating sphinx\source\code_baz.foo.rst
    sphinxgen: Generating sphinx\source\code_baz.foo.bar.rst
    sphinxgen: Generating sphinx\source\code_baz.rst
    sphinxgen: Found template file for code_baz.util.rst
    sphinxgen: Generating sphinx\source\code_baz.util.rst
    sphinxgen: Generating sphinx\source\code_baz.version.rst
    sphinxgen: Generating sphinx\source\code_index.rst

    >

Command Line Interface
------------------------

.. autoprogram:: sphinxgen:argument_parser
    :prog: sphinxgen

