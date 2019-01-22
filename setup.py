from setuptools import setup, find_packages


def read_reqs(filename: str):
    req = []
    with open(filename, 'r') as f:
        for line in f:
            if line.strip() and not line.startswith('-r'):
                req.append(line.strip())

    return req


install_requires = read_reqs("requirements.txt")
test_requires = read_reqs("test-requirements.txt")


# Get the long description from the relevant file
long_description = 'PyDriller is a Python framework that helps developers on mining software repositories. ' \
                   'With PyDriller' \
                   ' you can easily extract information from any Git repository, such as commits, developers, ' \
                   'modifications, diffs, and source codes, and quickly export CSV files.'

setup(
    name='PyDriller',
    description='Framework for MSR',
    long_description = long_description,
    author='Davide Spadini',
    author_email='spadini.davide@gmail.com',
    version='1.7',
    packages=find_packages('.'),
    url='https://github.com/ishepard/pydriller',
    license='Apache License',
    package_dir={'pydriller': 'pydriller'},
    python_requires='>=3.4',
    install_requires=install_requires,
    test_requirements=test_requires + install_requires,
    classifiers=[
            # How mature is this project? Common values are
            #   3 - Alpha
            #   4 - Beta
            #   5 - Production/Stable
            'Development Status :: 4 - Beta',
            'Environment :: Console',
            'Intended Audience :: Developers',
            'Intended Audience :: Science/Research',
            'License :: OSI Approved :: Apache Software License',
            'Programming Language :: Python :: 3.4',
            'Programming Language :: Python :: 3.5',
            'Programming Language :: Python :: 3.6',
            'Programming Language :: Python :: 3.7',
            'Topic :: Software Development :: Libraries :: Python Modules',
            "Operating System :: OS Independent",
            "Operating System :: POSIX",
            "Operating System :: Microsoft :: Windows",
            "Operating System :: MacOS :: MacOS X",
            ]
)
