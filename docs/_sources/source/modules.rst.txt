Documentation
=============


Implementation
--------------

See the `implementation document`_ for detailed information on the package and the theory behind it.


.. _`implementation document`: ../implementation.html


Commands
--------

This is a quick reference for common commands used throughout the project.


======================  ==========================================================
install dev              .. code-block:: bash

                             $ git clone https://github.com/jchiyah/data-validation.git data-validation
                             $ cd ./data-validation
                             $ python3 -m venv env
                             $ source env/Scripts/activate
                             $ pip3 install -r requirements/dev.txt
                             $ python3 setup.py install
tests                    .. code-block:: bash

                             $ pytest -svv
build documentation      .. code-block:: bash

                             $ cd docsrc
                             $ make html
publish documentation    .. code-block:: bash

                             $ cd docsrc
                             $ make github

                         And commit to GitHub!
======================  ==========================================================



Style
-----

This is a quick reference to the coding style used to develop this code. Future work should aim to follow a similar style.


==============  ==========================================================
function name   .. code-block:: python

                   function_name()
private func    .. code-block:: python

                   _private_function_name()
variable name   .. code-block:: python

                   normal_variable
                   objectVariable
                   _private_variable
func comments   reST style, like below:
style           .. code-block:: python

                   def function_x():
                        """
                        This is reST style.

                        :param param1: this is a first param
                        :param param2: this is a second param
                        :returns: this is a description of what is returned
                        :raises keyError: raises an exception
                        """
                        do_something()

whitespace      .. code-block:: python

                   whitespace = your_personal_preference(tabs or spaces)
                   # do not mix both
line endings    Unix \\n

more info       `PEP 8 Style Guide`_

==============  ==========================================================


.. _`PEP 8 Style Guide`: https://www.python.org/dev/peps/pep-0008/


Package
-------


.. toctree::
   :maxdepth: 2

   datavalidation


