#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
import re

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup


version = None
for line in open('./solve360/__init__.py'):
    m = re.search('__version__\s*=\s*(.*)', line)
    if m:
        version = m.group(1).strip()[1:-1]
        break
assert version

try:
    os.system('pandoc --from=markdown --to=rst --output=README.rst README.md')
except IOError:
    pass

long_description = open(('README.rst' if os.path.exists('README.rst') else 'README.md')).read() 

setup(
    name='solve360',
    version=version,
    description='Solve360 API Python wrapper',
    long_description=long_description,
    author='Daniel Nibon',
    author_email='daniel@nibon.se',
    url='https://github.com/nibon/solve360',
    install_requires=['requests>=1.0.0', 'iso8601>=0.1.10'],
    tests_require=['pytest>=2.0.0', 'httpretty>=0.6.1'],
    packages=['solve360'],
    package_data={'': ['*.rst', '*.md']},
    license='The MIT Licence',
    keywords='norada solve360 api wrapper',
    classifiers=(
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.4',
    ),
)
