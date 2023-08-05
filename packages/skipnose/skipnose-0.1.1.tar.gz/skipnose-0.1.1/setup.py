#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import unicode_literals, print_function
import os
from setuptools import setup, find_packages

from skipnose import __author__, __email__, __version__


def read(fname):
    return (open(os.path.join(os.path.dirname(__file__), fname), 'rb')
            .read().decode('utf-8'))


authors = read('AUTHORS.rst')
history = read('HISTORY.rst').replace('.. :changelog:', '')
licence = read('LICENSE.rst')
readme = read('README.rst')

requirements = read('requirements.txt').splitlines() + [
    'setuptools',
]

test_requirements = (
    read('requirements.txt').splitlines()
    + read('requirements-dev.txt').splitlines()[1:]
)

setup(
    name='skipnose',
    version=__version__,
    author=__author__,
    description='Nose plugin which allows to include/exclude directories '
                'for testing by their glob pattern.',
    long_description='\n\n'.join([readme, history, authors, licence]),
    url='https://github.com/Dealertrack/skipnose',
    packages=find_packages(exclude=['test', 'test.*']),
    install_requires=requirements,
    test_suite='tests',
    tests_require=test_requirements,
    entry_points={
        'nose.plugins.0.10': [
            'NOSETESTS_SKIPNOSE = skipnose:SkipNose'
        ]
    },
    keywords=' '.join([
        'skipnose',
        'test',
        'nosetests',
        'nose',
        'nosetest',
    ]),
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Software Development :: Testing",
    ],
)
