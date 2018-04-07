from setuptools import setup, find_packages

install_requires = ['gitpython']
test_requires = ['pytest', 'python-dateutil', 'psutil']


setup(
    name='pydriller',
    description='Framework for MSR',
    author='Davide Spadini',
    author_email='spadini.davide@gmail.com',
    version='1.0',
    packages=find_packages('.'),
    url='https://github.com/ishepard/pydriller',
    license='Apache License',
    package_dir={'pydriller': 'pydriller'},
    python_requires='>=3.6',
    install_requires=install_requires,
    test_requirements=test_requires + install_requires
)
