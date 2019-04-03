===============================
Data Validation
===============================


NOTE: This is a version of the package without any confidential information used to show it. It is not the actual system and many parts have been changed. Therefore, it is highly likely that whole modules will NOT work. If you would like to use the full-featured package or get involved in the project then contact me and we may be able to arrange something.



A micro-service to perform data validation on bike geometries.


* Free software: GNU Affero General Public License v3
* Documentation: https://jchiyah.github.io/data-validation


Features
--------

* Normalise bike parameter values and convert them to a common representation (e.g., remove symbols, substitute commas for dots, convert to degrees and millimetres).
* Calculate values for missing bike parameters (e.g., calculate chainstay using wheelbase).
* Validate each bike parameter and output how likely that parameter fits the overall bike geometry.


To read more about why this is important, check the :ref:`original problem <problem>` and the :ref:`extended information on the solution <solution>`.

Information
-----------


==============  ==========================================================
Python support  Python >= 3.6
Source          https://github.com/jchiyah/data-validation
Docs            https://jchiyah.github.io/data-validation
Issues          https://github.com/jchiyah/data-validation/issues
License         `AGPLv3`_.
git repo        .. code-block:: bash

                    $ git clone https://github.com/jchiyah/data-validation.git
==============  ==========================================================


.. _`problem`:

Problem
-------

Datasets, especially crowdsourced, often have inconsistent values and are prone to containing a lot of errors. GeometryGeeks, a website to compare bike geometries, crowdsources the collection of bike measures. This raises issues with:

- Inconsistent geometry parameter values and metrics (e.g. inches and millimetres mixed together, commas instead of dots).
- Missing bike geometry parameters.
- Wrong geometry parameter values (e.g. typos, human error).


There is a limit on the amount of validation that you can do on a web form without affecting some bike geometries. For instance, using maximum and minimum threshold values works until you need to input a children bike outside that range.
We, as humans, also make mistakes in terms of typing all the time - it is very easy to write 110 instead of 101 for example. The example may seem trivial, but if we consider something like 064 instead of 604 then it is a substantial change.


Therefore, we need to work out how we can deal with this. New methods for validating bike geometries reliably are needed.




.. _`solution`:

Solution
--------

The system developed here aims to provide an easy and reliable way to validate bike geometries using simple maths. The parameters of a bike geometry are all linked together, e.g. increasing the wheelbase may also increase the chainstay and front centre. This allows us to calculate and validate the values of said parameters in a given geometry.


The aim of this project is to develop a system that could validate a given bike geometry and calculate its missing parameters if possible.

Therefore, the objectives of the project are:

- Understand the relationship between the various bike geometry parameters.
- Derive a reliable way of validating bike geometry parameters exploiting these relationships.
- Normalise the values of the bike geometry into a standardised format.
- Implement the validation of the bike geometry parameters.
- Calculate missing bike geometry parameters.
- Return the validated bike geometry pointing out the geometry parameters that may be incorrect.


The system developed can deal with the validation of bike geometries and calculate missing parameters as needed using a mathematical model of bike geometries.

Each parameter returned has a confidence value representing the likelihood of that parameter being correct in the context of a given bike geometry. Parameters with high confidence values are more likely to be correct.



Credits
---------

This package was created with Cookiecutter_ and the `lgiordani/cookiecutter-pypackage`_ project template.


.. _`AGPLv3`: https://www.gnu.org/licenses/agpl-3.0.en.html
.. _`Google format`: https://stackoverflow.com/questions/3898572/what-is-the-standard-python-docstring-format
.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`lgiordani/cookiecutter-pypackage`: https://github.com/lgiordani/cookiecutter-pypackage

