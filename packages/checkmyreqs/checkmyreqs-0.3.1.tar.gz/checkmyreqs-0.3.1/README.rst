===========
checkmyreqs
===========

checkmyreqs allows you to check the packages in your requirements file against a specified Python version.

.. image:: https://api.travis-ci.org/dustinmm80/checkmyreqs.png
    :target: https://travis-ci.org/dustinmm80/checkmyreqs

Usage
=====

This command will check 2 requirements files, to see if their packages are compatible with Python 3.3 ::

    checkmyreqs -f requirements.txt,requirements_dev.txt -p 3.3

If you don't pass in a filename, it will use requirements.txt in the directory it is called ::

    checkmyreqs -p 3.2

The output is a list of packages not supported by the given Python version.

For each package, checkmyreqs will tell you if updating them will give you support.

There are 3 parameters ::

    -f, --files   : comma-separated list of files to check (optional, default is requirements.txt)
    -p, --python  : Python version to check compatibility, example 2.7 or 3.2 (optional, default is system Python)

You can also use ``pip freeze`` to check a Python environment without a requirements file, like so ::

    pip freeze | checkmyreqs -p 3.3

Caveat
======

checkmyreqs looks at packages on pypi.python.org to see if their author has included a classifier saying which
Python versions are supported.

If the package has incorrect or missing classifiers, checkmyreqs will show it as unsupported.

This tool is meant as an addition to other porting tools. 2to3 and six can help you make your code Python 3 ready,
and checkmyreqs lets you quickly check if your packages are ready to move as well.

Installation
============
::

    pip install checkmyreqs

----

Supports Python 2.7, 3.2, 3.3, 3.4

Python <=2.6, 3.0 and 3.1 are not supported, they don't have argparse

Development
===========

You can install the requirements with ::


    pip install -r requirements.txt
    pip install -r requirements_dev.txt

Then, run the tests with ::

    py.test
