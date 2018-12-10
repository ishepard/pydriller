[![Build Status](https://travis-ci.org/ishepard/pydriller.svg?branch=master)](https://travis-ci.org/ishepard/pydriller)
[![BCH compliance](https://bettercodehub.com/edge/badge/ishepard/pydriller?branch=master&token=fdd54de940e65d248cd892ac8791a1445f38c88f)](https://bettercodehub.com/)
[![codecov](https://codecov.io/gh/ishepard/pydriller/branch/master/graph/badge.svg)](https://codecov.io/gh/ishepard/pydriller)
[![Build status](https://ci.appveyor.com/api/projects/status/s7uni50v4wd54q43/branch/master?svg=true&retina=true&passingText=Windows%20passing&failingText=Windows%20failing)](https://ci.appveyor.com/project/ishepard/pydriller/branch/master)


# PyDriller

PyDriller is a Python framework that helps developers in analyzing Git repositories. With PyDriller you can easily extract information such as commits, developers, modifications, diffs, and source codes. 

![Alt Text](https://ishepard.github.io/images/mygif.gif)

## Table of contents
* **[Requirements](#requirements)**
* **[Install](#install)**
* **[Source code](#source-code)**
* **[Tutorial](#tutorial)**
* **[How to contribute](#how-to-contribute)**
* **[How to cite PyDriller](#how-to-cite-pydriller)**


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

## How to cite PyDriller

```
@inbook{PyDriller,
	title = "PyDriller: Python Framework for Mining Software Repositories",
	abstract = "Software repositories contain historical and valuable information about the overall development of software systems. Mining software repositories (MSR) is nowadays considered one of the most interesting growing fields within software engineering. MSR focuses on extracting and analyzing data available in software repositories to uncover interesting, useful, and actionable information about the system. Even though MSR plays an important role in software engineering research, few tools have been created and made public to support developers in extracting information from Git repository. In this paper, we present PyDriller, a Python Framework that eases the process of mining Git. We compare our tool against the state-of-the-art Python Framework GitPython, demonstrating that PyDriller can achieve the same results with, on average, 50% less LOC and significantly lower complexity.URL: https://github.com/ishepard/pydrillerMaterials: https://doi.org/10.5281/zenodo.1327363Pre-print: https://doi.org/10.5281/zenodo.1327411",
	author = "Spadini, Davide and Aniche, Maurício and Bacchelli, Alberto",
	year = "2018",
	doi = "10.1145/3236024.3264598",
	booktitle = "The 26th ACM Joint European Software Engineering Conference and Symposium on the Foundations of Software Engineering (ESEC/FSE)",
}
```

This project has received funding from the European Unions’ Horizon 2020 research and innovation programme under the Marie Sklodowska-Curie grant agreement No. 642954.

## License

This software is licensed under the Apache 2.0 License.
