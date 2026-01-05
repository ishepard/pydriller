from os import path
from setuptools import setup, find_packages

with open('requirements.txt') as reqs_file:
    requirements = reqs_file.read().splitlines()

with open('test-requirements.txt') as reqs_file:
    test_requirements = reqs_file.read().splitlines()

# Get the long description from the relevant file
long_description = 'PyDriller is a Python framework that helps developers on ' \
                   'mining software repositories. With PyDriller' \
                   ' you can easily extract information from any Git ' \
                   'repository, such as commits, developers, ' \
                   'modifications, diffs, and source codes, and ' \
                   'quickly export CSV files.'


def get_version():
    with open(path.join(path.dirname(__file__), 'pydriller', '__init__.py')) as f:
        for line in f:
            if line.startswith('__version__'):
                delim = '"' if '"' in line else "'"
                return line.split(delim)[1]
        raise RuntimeError("Unable to find version string.")


setup(
    name='PyDriller',
    description='Framework for MSR',
    long_description=long_description,
    author='Davide Spadini',
    author_email='spadini.davide@gmail.com',
    version=get_version(),
    packages=find_packages('.', exclude=['tests*']),
    include_package_data=True,
    data_files=[('', ['requirements.txt', 'test-requirements.txt'])],
    url='https://github.com/ishepard/pydriller',
    license='Apache License',
    package_dir={'pydriller': 'pydriller'},
    python_requires='>=3.5',
    install_requires=requirements,
    tests_require=requirements + test_requirements,
    classifiers=[
            # How mature is this project? Common values are
            #   3 - Alpha
            #   4 - Beta
            #   5 - Production/Stable
            'Development Status :: 5 - Production/Stable',
            'Environment :: Console',
            'Intended Audience :: Developers',
            'Intended Audience :: Science/Research',
            'License :: OSI Approved :: Apache Software License',
            'Programming Language :: Python :: 3.6',
            'Programming Language :: Python :: 3.7',
            'Programming Language :: Python :: 3.8',
            'Programming Language :: Python :: 3.9',
            'Topic :: Software Development :: Libraries :: Python Modules',
            "Operating System :: OS Independent",
            "Operating System :: POSIX",
            "Operating System :: Microsoft :: Windows",
            "Operating System :: MacOS :: MacOS X",
            ]
)
# setup.py
from os import path
from setuptools import setup, find_packages

# Read normal dependencies
with open('requirements.txt') as reqs_file:
    requirements = reqs_file.read().splitlines()

# Read test dependencies
with open('test-requirements.txt') as reqs_file:
    test_requirements = reqs_file.read().splitlines()

long_description = (
    "This is the PyDriller-based Automated Git Security Monitor project, "
    "providing continuous scanning, commit classification, OWASP/CVE detection, "
    "and generating structured security reports."
)

# Optionally, parse version from security_analysis/__init__.py if you track it there
def get_version():
    version_file = path.join(path.dirname(__file__), 'security_analysis', '__init__.py')
    try:
        with open(version_file, 'r', encoding='utf-8') as f:
            for line in f:
                if line.startswith('__version__'):
                    delim = '"' if '"' in line else "'"
                    return line.split(delim)[1]
    except FileNotFoundError:
        pass
    return "0.1.0"  # fallback version

setup(
    name='SecurityAnalysis',  # distribution/package name
    version=get_version(),
    description='PyDriller-based Automated Git Security Monitor',
    long_description=long_description,
    author='Your Team',
    author_email='your.team@example.com',
    url='https://github.com/yourorg/my_security_tool',
    license='Apache License 2.0',

    packages=find_packages(exclude=['tests*']),
    python_requires='>=3.6',
    install_requires=requirements,
    tests_require=requirements + test_requirements,

    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache Software License',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        "Operating System :: OS Independent",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
)

