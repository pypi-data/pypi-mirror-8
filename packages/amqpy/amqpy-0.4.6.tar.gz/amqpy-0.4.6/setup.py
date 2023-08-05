#!/usr/bin/env python3

import sys
import codecs

from setuptools import setup, find_packages

import amqpy

NAME = 'amqpy'
DESCRIPTION = 'AMQP 0.9.1 client library for Python >= 3.2.0'

if sys.version_info < (3, 2):
    raise Exception('amqpy requires Python 3.2 or higher')

classifiers = [
    'Development Status :: 3 - Alpha',
    'Programming Language :: Python',
    'Programming Language :: Python :: 3.2',
    'Programming Language :: Python :: 3.3',
    'Programming Language :: Python :: 3.4',
    'License :: OSI Approved :: GNU Lesser General Public License v2 or later (LGPLv2+)',
    'Intended Audience :: Developers',
]

keywords = ['amqp', 'rabbitmq', 'qpid']

is_pypy = hasattr(sys, 'pypy_version_info')

setup(
    name=NAME,
    description=DESCRIPTION,
    version=amqpy.__version__,
    author=amqpy.__author__,
    author_email=amqpy.__contact__,
    maintainer=amqpy.__maintainer__,
    url=amqpy.__homepage__,
    platforms=['any'],
    license='LGPL',
    packages=find_packages(exclude=['ez_setup', 'tests', 'tests.*']),
    tests_require=['pytest>=2.6'],
    classifiers=classifiers,
    keywords=keywords
)
