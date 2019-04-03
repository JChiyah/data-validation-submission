.. highlight:: shell

============
Installation
============


Stable release from sources
---------------------------

The sources for Data Validation can be downloaded from the `Github repo`_.

You can either clone the public repository:

.. code-block:: bash

    $ git clone git://github.com/jchiyah/datavalidation

Or download the `tarball`_:

.. code-block:: bash

    $ curl  -OL https://github.com/jchiyah/data-validation/tarball/master

Once you have a copy of the source, you can install it with:

.. code-block:: bash

    $ python setup.py install



Development from sources
------------------------

The sources for Data Validation can be downloaded from the `Github repo`_.

To install the package for development follow these steps:

.. code-block:: bash

    $ git clone git://github.com/jchiyah/data-validation data-validation
    $ cd data-validation
    # create virtual environment and activate it
    $ python3 -m venv env
    $ source env/activate
    # install required packages for development
    $ pip3 install -r requirements/dev.txt
    $ python3 setup.py install



Check the `common commands`_ used throughout development and other utilities that you may need to build the documentation or run the tests.


.. _common commands: source/modules.html#commands
.. _Github repo: https://github.com/jchiyah/data-validation
.. _tarball: https://github.com/jchiyah/data-validation/tarball/master
