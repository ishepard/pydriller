.. _intro_toplevel:

==================
Overview / Install
==================

PyDriller is a Python framework that helps developers on mining software repositories. With PyDriller you can easily extract information from any Git repository, such as commits, developers, modifications, diffs, and source codes, and quickly export CSV files.

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

How to cite PyDriller
=====================

.. sourcecode:: none

    @inbook{PyDriller,
        title = "PyDriller: Python Framework for Mining Software Repositories",
        abstract = "Software repositories contain historical and valuable information about the overall development of software systems. Mining software repositories (MSR) is nowadays considered one of the most interesting growing fields within software engineering. MSR focuses on extracting and analyzing data available in software repositories to uncover interesting, useful, and actionable information about the system. Even though MSR plays an important role in software engineering research, few tools have been created and made public to support developers in extracting information from Git repository. In this paper, we present PyDriller, a Python Framework that eases the process of mining Git. We compare our tool against the state-of-the-art Python Framework GitPython, demonstrating that PyDriller can achieve the same results with, on average, 50% less LOC and significantly lower complexity.URL: https://github.com/ishepard/pydrillerMaterials: https://doi.org/10.5281/zenodo.1327363Pre-print: https://doi.org/10.5281/zenodo.1327411",
        author = "Spadini, Davide and Aniche, Maurício and Bacchelli, Alberto",
        year = "2018",
        doi = "10.1145/3236024.3264598",
        booktitle = "The 26th ACM Joint European Software Engineering Conference and Symposium on the Foundations of Software Engineering (ESEC/FSE)",
    }


