#!/usr/bin/env python

import sys
from setuptools import setup
import reflectivipy


if sys.version_info > (2, 8) or 'PyPy' not in sys.copyright:
    sys.exit('Sorry, Reflectivipy is only for Pypy 2.7 at the moment!')


packages = ['reflectivipy',
            'reflectivipy.wrappers']

setup(
    name='reflectivipy',
    version=reflectivipy.__version__,
    description=('A Python Implementation of the Reflectivity API from '
                 'the Pharo language'),
    long_description=open('README.rst').read(),
    keywords='object-centric partial-behavior-reflection metaprogramming',
    url='https://github.com/StevenCostiou/reflectivipy',
    author='Steven Costiou',
    author_email='steven.costiou@abc.fr',

    packages=packages,
    package_data={'': ['README.rst', 'LICENCE']},
    include_package_data=True,
    tests_require=['pytest'],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: Implementation :: PyPy',
        'Operating System :: OS Independent',
        'Intended Audience :: Developers',
        'Topic :: Software Development',
        'Topic :: Software Development :: Libraries',
        'Topic :: Software Development :: Code generators',
        'Topic :: Software Development :: Debuggers'
    ]
)
