from setuptools import setup, find_packages

install_requires = ['gitpython']
test_requires = ['pytest', 'python-dateutil', 'psutil']


setup(
    author_email='spadini.davide@gmail.com',
    description='Framework for MSR',
    name='pydriller',
    version='1.0',
    packages=find_packages(),
    url='https://github.com/ishepard/pydriller',
    package_dir={'pydriller': 'pydriller'},
    license='BSD License',
    author='Davide Spadini',
    python_requires='>=3.6',
    install_requires=install_requires,
    test_requirements=test_requires + install_requires
)
