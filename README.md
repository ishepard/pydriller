[![Build Status](https://travis-ci.org/ishepard/pydriller.svg?branch=master)](https://travis-ci.org/ishepard/pydriller)
[![BCH compliance](https://bettercodehub.com/edge/badge/ishepard/pydriller?branch=master&token=fdd54de940e65d248cd892ac8791a1445f38c88f)](https://bettercodehub.com/)
[![codecov](https://codecov.io/gh/ishepard/pydriller/branch/master/graph/badge.svg)](https://codecov.io/gh/ishepard/pydriller)


# PyDriller

PyDriller is a Python framework that helps developers on mining software repositories. With PyDriller you can easily extract information from any Git repository, such as commits, developers, modifications, diffs, and source codes, and quickly export to CSV files.

![Alt Text](https://ishepard.github.io/images/mygif.gif)


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
> unzip test-repos.zip
```
and run the tests using pytest:

```
> pytest
```


# TUTORIAL
For information on how to use PyDriller, refer to the ufficial documentation:

- [http://pydriller.readthedocs.io](http://pydriller.readthedocs.io)
- a video on Youtube: [https://www.youtube.com/watch?v=7Oui4bP9eN8](https://www.youtube.com/watch?v=7Oui4bP9eN8)

or have a look at our [example](https://github.com/ishepard/pydriller/tree/master/examples) folder.

## How do I cite PyDriller?

For now, cite the repository.


# License

This software is licensed under the Apache 2.0 License.
