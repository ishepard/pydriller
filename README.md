[![Build Status](https://github.com/ishepard/pydriller/workflows/Pydriller%20workflow/badge.svg?branch=master)](https://github.com/ishepard/pydriller/actions)
[![Documentation Status](https://readthedocs.org/projects/pydriller/badge/?version=latest)](https://pydriller.readthedocs.io/en/latest/?badge=latest)
[![codecov](https://codecov.io/gh/ishepard/pydriller/branch/master/graph/badge.svg)](https://codecov.io/gh/ishepard/pydriller)
[![Downloads](https://pepy.tech/badge/pydriller/month)](https://pepy.tech/project/pydriller)
[![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)

# PyDriller

test
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
First clone the repository:
```
git clone https://github.com/ishepard/pydriller.git
cd pydriller
```
**(Optional)** It is suggested to make use of `virtualenv`. Therefore, before installing the requirements run:
```
python3 -m venv venv
source venv/bin/activate
```
Then, install the requirements:
```
pip install -r requirements.txt
```

**(Important)** I tend to not accept Pull Requests without tests, so:

- unzip the `test-repos.zip` zip file
- inside are many "small repositories" that were manually created to test PyDriller. Use one of your choice to test your feature (check the existing tests for inspiration)
- if none is suitable for testing your feature, create a new one. **Be careful**: if you create a new one, do not forget to upload a new zip file `test-repos.zip` that includes your new repository, otherwise the tests will fail.

To run the tests (using pytest):

```
unzip test-repos.zip
pip install -r test-requirements.txt
pytest
```

## Acknowledgements

This project has received funding from the European Union's Horizon 2020 research and innovation programme under the Marie Sklodowska-Curie grant agreement No. 642954.
