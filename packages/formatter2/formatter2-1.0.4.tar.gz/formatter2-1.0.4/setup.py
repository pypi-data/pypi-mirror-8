import os
import formatter2 as metadata
from setuptools import setup, find_packages

if os.path.isfile('README.rst'):
    long_description = open('README.rst').read()
else:
    long_description = 'See http://pypi.python.org/pypi/formatter2/'

setup(
    name=metadata.__package_name__,
    version=metadata.__version__,
    author=metadata.__author__,
    author_email=metadata.__author_email__,
    description=metadata.__description__,
    url=metadata.__url__,
    license='BSD',
    packages=find_packages(),
    long_description=long_description,
    test_suite='nose.collector',
    install_requires=[
        'pep8',
    ],
    setup_requires=['nose', 'mock', 'coverage', 'tissue'],
    py_modules=['formatter2.formatter'],
    classifiers=[
        'License :: OSI Approved :: BSD License',
    ],
    entry_points={
        'console_scripts': [
            'python-formatter = formatter2.main:main',
            'format-python = formatter2.main:main',
        ],
    },
)
