.. _intro_toplevel:

==================
Overview / Install
==================

PyDriller is a Python framework that helps developers on mining software repositories. Born as a fork of `RepoDriller`_, with PyDriller you can easily extract information from any Git repository, such as commits, developers, modifications, diffs, and source codes, and quickly export CSV files.

.. _Repodriller: https://github.com/mauricioaniche/repodriller

.. image:: mygif.*

Requirements
============

* `Python`_ 3.4 or newer
* `Git`_

.. _Python: https://www.python.org
.. _Git: https://git-scm.com/

Installing PyDriller
====================

Installing PyDriller is easily done using `pip`_. Assuming it is installed, just run the following from the command-line:

.. _pip: https://pip.pypa.io/en/latest/installing.html

.. sourcecode:: none

    # pip install pydriller


This command will download the latest version of GitPython from the
`Python Package Index <http://pypi.python.org/pypi/GitPython>`_ and install it
to your system. This will also install the necessary dependencies.


Source Code
===========

PyDriller's git repo is available on GitHub, which can be browsed at:

 * https://github.com/ishepard/pydriller

and cloned using::

    $ git clone https://github.com/ishepard/pydriller
    $ cd pydriller

Optionally (but suggested), make use of virtualenv::
    
    $ virtualenv -p python3 venv
    $ source venv/bin/activate

Install the requirements::
    
    $ pip install -r requirements
    $ unzip test-repos.zip

and run the tests using pytest::

    $ pytest

