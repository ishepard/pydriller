[![Build Status](https://github.com/ishepard/pydriller/workflows/Pydriller%20workflow/badge.svg?branch=master)](https://github.com/ishepard/pydriller/actions)
[![Documentation Status](https://readthedocs.org/projects/pydriller/badge/?version=latest)](https://pydriller.readthedocs.io/en/latest/?badge=latest)
[![codecov](https://codecov.io/gh/ishepard/pydriller/branch/master/graph/badge.svg)](https://codecov.io/gh/ishepard/pydriller)
[![BCH compliance](https://bettercodehub.com/edge/badge/ishepard/pydriller?branch=master&token=fdd54de940e65d248cd892ac8791a1445f38c88f)](https://bettercodehub.com/)

[![Downloads](https://pepy.tech/badge/pydriller/month)](https://pepy.tech/project/pydriller/month)
[![Language grade: Python](https://img.shields.io/lgtm/grade/python/g/ishepard/pydriller.svg?logo=lgtm&logoWidth=18)](https://lgtm.com/projects/g/ishepard/pydriller/context:python)

# PyDriller

PyDriller is a Python framework that helps developers in analyzing Git repositories. With PyDriller you can easily extract information such as commits, developers, modifications, diffs, and source codes. 

![Alt Text](https://ishepard.github.io/images/mygif.gif)

## Table of contents
* **[How to cite PyDriller](#how-to-cite-pydriller)**
* **[Requirements](#requirements)**
* **[Install](#install)**
* **[Source code](#source-code)**
* **[Tutorial](#tutorial)**
* **[How to contribute](#how-to-contribute)**

## How to cite PyDriller

```
@inproceedings{Spadini2018,
	address = {New York, New York, USA},
	author = {Spadini, Davide and Aniche, Maur\'{i}cio and Bacchelli, Alberto},
	booktitle = {Proceedings of the 2018 26th ACM Joint Meeting on European Software Engineering Conference and Symposium on the Foundations of Software Engineering - ESEC/FSE 2018},
	doi = {10.1145/3236024.3264598},
	isbn = {9781450355735},
	keywords = {2018,acm reference format,and alberto bacchelli,davide spadini,git,gitpython,maur\'{i}cio aniche,mining software repositories,pydriller,python},
	pages = {908--911},
	publisher = {ACM Press},
	title = {{PyDriller: Python framework for mining software repositories}},
	url = {http://dl.acm.org/citation.cfm?doid=3236024.3264598},
	year = {2018}
}

```

## REQUIREMENTS
Very few! Just:

- Python3
- Git

The list of dependencies is shown in `./requirements.txt`, however the installer takes care of installing them for you.

## INSTALL

Installing PyDriller is easily done using pip. Assuming it is installed, just run the following from the command-line:

```
pip install pydriller
```
This will also install the necessary dependencies.

## SOURCE CODE

If you like to clone from source, you can do it with very simple steps.
First, clone the repo:

```
> git clone https://github.com/ishepard/pydriller.git
> cd pydriller
```

### OPTIONAL

It is suggested to make use of `virtualenv`:

```
> virtualenv -p python3 venv
> source venv/bin/activate
```

### INSTALL THE REQUIREMENTS AND RUN THE TESTS

Install the requirements:

```
> pip install -r requirements.txt
```

to run the tests (using pytest):

```
> unzip test-repos.zip
> pip install -r test-requirements.txt
> pytest
```


## TUTORIAL
For information on how to use PyDriller, refer to the official documentation:

- [http://pydriller.readthedocs.io](http://pydriller.readthedocs.io)
- a video on Youtube: [https://www.youtube.com/watch?v=7Oui4bP9eN8](https://www.youtube.com/watch?v=7Oui4bP9eN8)

or have a look at our [example](https://github.com/ishepard/pydriller/tree/master/examples) folder.

## How to contribute
Fork the project and follow the instructions on how to get started with [source code](#source-code). I tend to not accept a Pull Request without tests, so:

- unzip the `test-repos.zip` zip file
- inside you will find many "small repositories" that I manually created to test PyDriller. Choose the one you prefer the most, and test your feature (check the tests I have already written, you'll find inspiration there)
- if you do not find a repository that is suitable to test your feature, create a new one. **Be careful**: if you create a new one, do not forget to upload a new zip file `test-repos.zip` that includes your new repository, otherwise the tests will fail.

## License

This software is licensed under the Apache 2.0 License.

This project has received funding from the European Unions’ Horizon 2020 research and innovation programme under the Marie Sklodowska-Curie grant agreement No. 642954.
