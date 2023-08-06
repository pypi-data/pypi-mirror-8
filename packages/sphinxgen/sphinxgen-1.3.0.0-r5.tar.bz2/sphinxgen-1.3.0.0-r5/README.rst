=================================================================
sphinxgen
=================================================================

.. # POST TITLE
.. # BEGIN BADGES

.. # END BADGES


.. contents:: **Page Contents**
    :local:
    :depth: 2
    :backlinks: top

tl;dr
---------------

What?
~~~~~~~~~~~~~~

**sphinxgen** is used to generate files from python packages and modules found
in a specified set of directories. It is intended for generating sphinx autodoc
stub files, but can be used for other purposes. Files are generated using
`jinja`_ templates to provide maximum flexbility. You can use a set of built-in
templates, or provide your own.


Install?
~~~~~~~~~~~~~

Install with `pip`_:

.. code:: bash

    $ pip install sphinxgen

Or, from source:

.. code:: bash

    $ python setup.py install


Examples?
~~~~~~~~~~~~~~~~~~

.. code:: bash

    > sphinxgen -o sphinx/source src/python/my_package src/python/my_other_package

You can also use it as a `setuptools`_ command:

.. code:: ini

    #setup.cfg

    [sphinxgen]
    package_dirs = src/python/my_package,src/python/my_other_package
    output = sphinx/source
    
.. code:: bash

    > setup.py sphinxgen

Dependencies?
~~~~~~~~~~~~~~~~

sphinxgen is developed against `python`_ version 2.7.

Other dependencies are handled by `pip`_.

For building the docs from source with `sphinx`_, you will need the packages listed
under ``sphinx/requirements.pip``.

Docs?
~~~~~~~~

* `Read The Docs (.org) <http://sphinxgen.readthedocs.org/>`_
* `Python Hosted (.org) <http://pythonhosted.org/sphinxgen/>`_


Misc.
---------------


Contact Information
~~~~~~~~~~~~~~~~~~~~~~~~

This project is currently hosted on `bitbucket <https://bitbucket.org>`_, 
at `https://bitbucket.org/bmearns/sphinxgen <https://bitbucket.org/bmearns/sphinxgen/>`_.
The primary author is Brian Mearns, whom you can contact through bitbucket at
`https://bitbucket.org/bmearns <https://bitbucket.org/bmearns>`_. 


Copyright and License
~~~~~~~~~~~~~~~~~~~~~~~~~~

\ ``sphinxgen``\  is \ *free software*\ : you can redistribute it and/or modify
it under the terms of the \ **GNU General Public License**\  as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version. 



\ ``sphinxgen``\  is distributed in the hope that it will be useful,
but \ **without any warranty**\ ; without even the implied warranty of
\ *merchantability*\  or \ *fitness for a particular purpose*\ .  See the
GNU General Public License for more details. 



A copy of the GNU General Public License is available in the
\ ``sphinxgen``\ distribution under the file LICENSE.txt. If you did not
receive a copy of this file, see
`http://www.gnu.org/licenses/ <http://www.gnu.org/licenses/>`_. 


.. _jinja: http://jinja.pocoo.org/
.. _sphinx_rtd_theme: https://github.com/snide/sphinx_rtd_theme
.. _sphinx: http://sphinx-doc.org/
.. _pip: https://pypi.python.org/pypi/pip
.. _setuptools: https://pythonhosted.org/setuptools/
.. _python: http://python.org/

