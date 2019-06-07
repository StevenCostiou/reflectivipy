#!/usr/bin/env python

from setuptools import setup
import reflectivipy


packages = ["reflectivipy", "reflectivipy.wrappers"]

setup(
    name="reflectivipy",
    version=reflectivipy.__version__,
    description=(
        "A Python Implementation of the Reflectivity API from " "the Pharo language"
    ),
    long_description=open("README.rst").read(),
    keywords="object-centric partial-behavior-reflection metaprogramming",
    url="https://github.com/StevenCostiou/reflectivipy",
    author="Steven Costiou",
    author_email="steven.costiou@abc.fr",
    packages=packages,
    package_data={"": ["README.rst", "LICENCE"]},
    include_package_data=True,
    tests_require=["pytest"],
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: Implementation :: PyPy",
        "Programming Language :: Python :: Implementation :: CPython",
        "Operating System :: OS Independent",
        "Intended Audience :: Developers",
        "Topic :: Software Development",
        "Topic :: Software Development :: Libraries",
        "Topic :: Software Development :: Code Generators",
        "Topic :: Software Development :: Debuggers",
    ],
)
