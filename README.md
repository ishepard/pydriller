[![Build Status](https://travis-ci.org/ishepard/pydriller.svg?branch=master)](https://travis-ci.org/ishepard/pydriller)
[![BCH compliance](https://bettercodehub.com/edge/badge/ishepard/pydriller?branch=master&token=fdd54de940e65d248cd892ac8791a1445f38c88f)](https://bettercodehub.com/)


# PyDriller

PyDriller is a Python framework that helps developers on mining software repositories. Born as a fork of [RepoDriller](https://github.com/mauricioaniche/repodriller), with PyDriller you can easily extract information from any Git repository, such as commits, developers, modifications, diffs, and source codes, and quickly export CSV files.

<!--Take a look at our [manual folder](https://www.github.com/mauricioaniche/repodriller/tree/master/manual) and [our many examples](https://github.com/mauricioaniche/repodriller-tutorial).-->


# REQUIREMENTS
Very few! Just:

- Python3
- Git

The list of dependencies are listed in ./requirements.txt, however the installer takes care of installing them for you.

# INSTALL

Installing PyDriller is easily done using pip. Assuming it is installed, just run the following from the command-line:

```
pip install pydriller
```
This will also install the necessary dependencies.

# SOURCE CODE

If you like to clone from source, you can do it with very simple steps.

## OPTIONAL

It is suggested to make use of `virtualenv`:

```
> virtualenv -p python3 venv
> source venv/bin/activate
```

## INSTALL FROM SOURCE
Clone the repo:

```
> git clone https://github.com/ishepard/pydriller.git
```

install the requirements:

```
> cd pydriller
> pip install -r requirements
```
and run the tests using pytest:

```
> pytest
```


# TUTORIAL
For information on how to use PyDriller, refer to the ufficial documentation:

- [http://pydriller.readthedocs.io](http://pydriller.readthedocs.io)

or have a look at our [example](https://github.com/ishepard/pydriller/tree/master/examples) folder.

## How do I cite PyDriller?

For now, cite the repository.


# License

This software is licensed under the Apache 2.0 License.
