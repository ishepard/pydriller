[![Build Status](https://github.com/ishepard/pydriller/workflows/Pydriller%20workflow/badge.svg?branch=master)](https://github.com/ishepard/pydriller/actions)
[![Documentation Status](https://readthedocs.org/projects/pydriller/badge/?version=latest)](https://pydriller.readthedocs.io/en/latest/?badge=latest)
[![codecov](https://codecov.io/gh/ishepard/pydriller/branch/master/graph/badge.svg)](https://codecov.io/gh/ishepard/pydriller)
[![Downloads](https://pepy.tech/badge/pydriller/month)](https://pepy.tech/project/pydriller)
[![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)

# PyDriller

PyDriller is a Python framework that helps developers in analyzing Git repositories. With PyDriller you can easily extract information about **commits**, **developers**, **modified files**, **diffs**, and **source code**.

## Install
```
pip install pydriller
```

## Quick usage

```python

from pydriller import Repository

for commit in Repository('https://github.com/ishepard/pydriller').traverse_commits():
    print(commit.hash)
    print(commit.msg)
    print(commit.author.name)

    for file in commit.modified_files:
        print(file.filename, ' has changed')

```

Read the [docs](http://pydriller.readthedocs.io) for more usage examples.
Furthermore, a video is available on [Youtube](https://www.youtube.com/watch?v=7Oui4bP9eN8).

## TestPulse
If you are interested in tests, tests health and code quality, test code coverage, etc..., you might be interested in our new project: **TestPulse!**
Check it out: [https://www.testpulse.io](https://www.testpulse.io)

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

## How to contribute

### Pre-requisites

- First clone the repository:
  ```
  git clone https://github.com/ishepard/pydriller.git
  cd pydriller
  ```
- **(Optional)** It is suggested to make use of `virtualenv`. Therefore, before installing the requirements run:
  ```
  python3 -m venv venv
  source venv/bin/activate
  ```
- Then, install PyDriller's requirements:
  ```
  pip install -r requirements.txt
  ```
- For executing the test suite, extract the test repositories and install the test requirements:
  ```
  unzip test-repos.zip
  pip install -r test-requirements.txt
  ```
- For linting and type checking, install the development requirements
  ```
  pip install -r dev-requirements.txt
  ```

### Testing

**(Important)** I tend to not accept Pull Requests without tests, so:

- unzip the `test-repos.zip` zip file
- inside are many "small repositories" that were manually created to test PyDriller. Use one of your choice to test your feature (check the existing tests for inspiration)
- if none is suitable for testing your feature, create a new one. **Be careful**: if you create a new one, do not forget to upload a new zip file `test-repos.zip` that includes your new repository, otherwise the tests will fail.

Run the test suite with [pytest](https://docs.pytest.org/en/stable/):

```
pytest
```

Run the test suite with a coverage report as terminal output:

```
pytest --cov-report term --cov=pydriller tests/
```

alternatively run:

```
make testcoverage
```

### Type checking

PyDriller source code is annotated for type checking, [see syntax](https://peps.python.org/pep-0484/).
The [mypy type checker](https://www.mypy-lang.org/) is executed on each pull request.
That is, code that does not type check will not pass that build step, see [CI step](https://github.com/ishepard/pydriller/blob/51510ab68b30174f085ceec235cfeaeb1bf3fbc0/.github/workflows/continuous-integration-workflow.yml#L29).
Run the type checker locally:

```
mypy --ignore-missing-imports pydriller/ tests/
```

alternatively run:

```
make typecheck
```

### Linting

PyDriller relies on the [Flake8 linter](https://flake8.pycqa.org/en/latest/) to check and enforce code style.
The linter is executed on each pull request.
That is, code that does not conform to [code style rules as formulated by Flake8](https://www.flake8rules.com/), will not pass that build step, see [CI step](https://github.com/ishepard/pydriller/blob/51510ab68b30174f085ceec235cfeaeb1bf3fbc0/.github/workflows/continuous-integration-workflow.yml#L33).
Run the type checker locally:

```
flake8
```

alternatively run:

```
make lint
```

### CodeQL

PyDriller's CI chain executes a set of CodeQL queries related to Python quality and security.
Currently, a local CodeQL setup is quite big (>1.7GB) and require multiple setup and configuration steps.
Therefore, it is omitted here and in the [Makefile](./Makefile).


## Acknowledgements

This project has received funding from the European Union's Horizon 2020 research and innovation programme under the Marie Sklodowska-Curie grant agreement No. 642954.
