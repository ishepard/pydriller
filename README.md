[![Build Status](https://travis-ci.com/ishepard/pydriller.svg?token=J3YWhdMEr4RvUk6qZbMK&branch=master)](https://travis-ci.com/ishepard/pydriller)
[![BCH compliance](https://bettercodehub.com/edge/badge/ishepard/pydriller?branch=master&token=fdd54de940e65d248cd892ac8791a1445f38c88f)](https://bettercodehub.com/)


# PyDriller

PyDriller is a Python framework that helps developers on mining software repositories. Born as a fork of [RepoDriller](https://github.com/mauricioaniche/repodriller), with PyDriller you can easily extract information from any Git repository, such as commits, developers, modifications, diffs, and source codes, and quickly export CSV files.

<!--Take a look at our [manual folder](https://www.github.com/mauricioaniche/repodriller/tree/master/manual) and [our many examples](https://github.com/mauricioaniche/repodriller-tutorial).-->


# INSTALL

Installing PyDriller is easily done using pip. Assuming it is installed, just run the following from the command-line:

```
pip install pydriller
```


# SOURCE CODE

If you like to clone from source, you can do it like so:

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


# GETTING STARTED



## How do I cite PyDriller?

For now, cite the repository.


## How do I contribute?

```
git clone https://github.com/ishepard/pydriller.git
unzip test-repos.zip
```

Then, you can:

* compile : `mvn clean compile`
* test    : `mvn test`
* eclipse : `mvn eclipse:eclipse`
* build   : `mvn clean compile assembly:single`

# License

This software is licensed under the Apache 2.0 License.
