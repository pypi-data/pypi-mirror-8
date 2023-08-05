# -*- coding: utf-8 -*-

import os

from codecs import open

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

desc = "A Python implementation of Google's Encoded Polyline Algorithm Format."

with open('README.rst', 'r') as f:
    long_desc = f.read()
with open(os.path.join('requirements', 'base.txt'), 'r') as f:
    base_reqs = f.readlines()
with open(os.path.join('requirements', 'test.txt'), 'r') as f:
    test_reqs = f.readlines()

setup(
    name='polyline',
    version='1.1',
    description=desc,
    long_description=long_desc,
    author='Bruno M. Custódio',
    author_email='bruno@brunomcustodio.com',
    url='http://pypi.python.org/pypi/polyline/',
    packages=['polyline'],
    install_requires=base_reqs,
    tests_require=test_reqs,
    test_suite='nose.collector',
    license='MIT',
    zip_safe=False,
    classifiers=(
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Topic :: Software Development :: Libraries',
        'Topic :: Utilities',
    ),
)
