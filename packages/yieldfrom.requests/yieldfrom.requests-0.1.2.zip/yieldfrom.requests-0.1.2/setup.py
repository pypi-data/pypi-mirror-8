#!/usr/bin/env python

import os
import sys

from codecs import open

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

if sys.argv[-1] == 'publish':
    os.system('python setup.py sdist upload')
    sys.exit()

packages = [
    'yieldfrom',
    'yieldfrom.requests',
]

requires = ['chardet>=2.2.1', 'yieldfrom.http.client', 'yieldfrom.urllib3', 'setuptools']

with open('README.rst', 'r', 'utf-8') as f:
    readme = f.read()
with open('HISTORY.rst', 'r', 'utf-8') as f:
    history = f.read()

setup(
    name='yieldfrom.requests',
    version='0.1.2',
    description='asyncio port of Requests: "Python HTTP for Humans".',
    long_description=readme + '\n\n' + history,

    author='Kenneth Reitz',
    author_email='me@kennethreitz.com',
    maintainer='David Keeney',
    maintainer_email='dkeeney@rdbhost.com',

    url='http://github.com/rdbhost/yieldfromrequests',

    packages=packages,
    package_data={'': ['LICENSE', 'NOTICE'],
                  'yieldfrom.requests': ['*.pem', 'requests/*.pem'],
                  'yieldfrom': ['requests/*.pem', '*.pem']},
    package_dir={'yieldfrom': 'yieldfrom'},
    include_package_data=True,
    namespace_packages=['yieldfrom'],
    install_requires=requires,

    license='Apache 2.0',
    zip_safe=False,
    classifiers=(
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'License :: OSI Approved :: Apache Software License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
    ),
)
