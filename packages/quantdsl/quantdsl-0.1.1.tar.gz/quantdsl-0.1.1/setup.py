#!/usr/bin/env python
import os
import sys
from setuptools import setup, find_packages

long_description = """
Quant DSL is a functional programming language for modelling derivative instruments.

At the heart of Quant DSL is a set of built-in elements (e.g. "Market", "Choice", "Wait") that encapsulate maths used in finance and trading (i.e. models of market dynamics, the least-squares Monte Carlo approach, time value of money calculations) and which can be composed into executable expressions of value.

User defined functions are supported, and can be used to generate massive expressions. The syntax of Quant DSL expressions has been formally defined, and the semantic model is supported with mathematical proofs. The Python package quantdsl is an implementation in Python of the Quant DSL syntax and semantics.

An extensive `README file is available on GitHub <https://github.com/johnbywater/quantdsl/blob/master/README.md>`_.
"""

from quantdsl import __version__


setup(
    name='quantdsl',
    version=__version__,
    packages=find_packages(),
    # just use auto-include and specify special items in MANIFEST.in
    zip_safe = False,
    install_requires = [
        'argh',
        'mock',
        'numpy',
        'python-dateutil',
        'scipy',
        'six',
    ],
    scripts = [
        os.path.join('scripts', 'quant-dsl.py'),
    ],
    author='John Bywater',
    author_email='john.bywater@appropriatesoftware.net',
    license='BSD',
    url='https://github.com/johnbywater/quantdsl',
    description='Domain specific language for quantitative analytics in finance.',
    long_description = long_description,
    classifiers = [
        'Development Status :: 4 - Beta',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'Intended Audience :: Education',
        'Intended Audience :: Financial and Insurance Industry',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Office/Business :: Financial',
        'Topic :: Office/Business :: Financial :: Investment',
        'Topic :: Office/Business :: Financial :: Spreadsheet',
        'Topic :: Scientific/Engineering :: Information Analysis',
        'Topic :: Scientific/Engineering :: Mathematics',
        'Topic :: Software Development :: Libraries :: Python Modules',
   ],
)
