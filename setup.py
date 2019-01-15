#!/usr/bin/env python

import sys
from setuptools import setup
import reflectivity


if sys.version_info > (2, 8) or 'PyPy' not in sys.copyright:
    sys.exit('Sorry, Reflectivity is only for Pypy 2.7 at the moment!')


packages = ['reflectivity',
            'reflectivity.wrappers']

setup(
    name='reflectivity',
    version=reflectivity.__version__,
    description=('A Python Implementation of the Reflectivity API from '
                 'the Pharo language'),
    long_description=open('README.rst').read(),
    keywords='object-centric partial-behavior-reflection metaprogramming',
    url='https://github.com/.../...',
    author='Steven Coustiou',
    author_email='steven.coustiou@inria.fr',

    packages=packages,
    package_data={'': ['README.rst']},
    include_package_data=True,
    tests_require=['pytest'],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: Implementation :: PyPy'
        'Operating System :: OS Independent',
        'Intended Audience :: Developers',
        'Topic :: Software Development',
        'Topic :: Software Development :: Libraries',
        'Topic :: Software Development :: Code generators',
        'Topic :: Software Development :: Debuggers'
    ]
)
