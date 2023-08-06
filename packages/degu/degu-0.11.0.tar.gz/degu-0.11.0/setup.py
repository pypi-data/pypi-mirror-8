#!/usr/bin/env python3

# degu: an embedded HTTP server and client library
# Copyright (C) 2014 Novacut Inc
#
# This file is part of `degu`.
#
# `degu` is free software: you can redistribute it and/or modify it under
# the terms of the GNU Lesser General Public License as published by the Free
# Software Foundation, either version 3 of the License, or (at your option) any
# later version.
#
# `degu` is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE.  See the GNU Lesser General Public License for more
# details.
#
# You should have received a copy of the GNU Lesser General Public License along
# with `degu`.  If not, see <http://www.gnu.org/licenses/>.
#
# Authors:
#   Jason Gerard DeRose <jderose@novacut.com>

"""
Install `degu`.
"""

import sys
if sys.version_info < (3, 4):
    sys.exit('ERROR: degu requires Python 3.4 or newer')

import os
from os import path
import subprocess
from distutils.core import setup, Extension
from distutils.cmd import Command

import degu
from degu.tests.run import run_tests


TREE = path.dirname(path.abspath(__file__))
LONG_DESCRIPTION = """An embedded HTTP server and client library for Python3.

Degu can be used to build network-transparent services, whether the other
endpoint is in the cloud, on the local network, on the localhost, or even on the
localhost using HTTP over AF_UNIX.

Degu is especially well suited for implementing REST APIs for device-to-device
communication.  It's a building block for future stuff, your vehicle into bold,
uncharted territory."""


def run_under_same_interpreter(opname, script, args):
    print('\n** running: {}...'.format(script), file=sys.stderr)
    if not os.access(script, os.R_OK | os.X_OK):
        print('ERROR: cannot read and execute: {!r}'.format(script),
            file=sys.stderr
        )
        print('Consider running `setup.py test --skip-{}`'.format(opname),
            file=sys.stderr
        )
        sys.exit(3)
    cmd = [sys.executable, script] + args
    print('check_call:', cmd, file=sys.stderr)
    subprocess.check_call(cmd)
    print('** PASSED: {}\n'.format(script), file=sys.stderr)


def run_sphinx_doctest():
    script = '/usr/share/sphinx/scripts/python3/sphinx-build'
    doc = path.join(TREE, 'doc')
    doctest = path.join(TREE, 'doc', '_build', 'doctest')
    args = ['-EW', '-b', 'doctest', doc, doctest]
    run_under_same_interpreter('sphinx', script, args)


def run_pyflakes3():
    script = '/usr/bin/pyflakes3'
    names = [
        'degu',
        'setup.py',
        'benchmark.py',
        'benchmark-parsing.py',
        'benchmark-ssl.py',
    ]
    args = [path.join(TREE, name) for name in names]
    run_under_same_interpreter('flakes', script, args)


class Test(Command):
    description = 'run unit tests and doctests'

    user_options = [
        ('skip-sphinx', None, 'do not run Sphinx doctests'),
        ('skip-flakes', None, 'do not run pyflakes static checks'),
        ('skip-slow', None, 'skip the rather slow socket timeout tests'),
    ]

    def initialize_options(self):
        self.skip_sphinx = 0
        self.skip_flakes = 0
        self.skip_slow = 0

    def finalize_options(self):
        pass

    def run(self):
        if self.skip_slow:
            os.environ['DEGU_TEST_SKIP_SLOW'] = 'true'
        if not run_tests():
            sys.exit(2)
        if not self.skip_sphinx:
            run_sphinx_doctest()
        if not self.skip_flakes:
            run_pyflakes3()


setup(
    name='degu',
    description='Embedded HTTP server and client library',
    long_description=LONG_DESCRIPTION,
    url='https://launchpad.net/degu',
    version=degu.__version__,
    author='Jason Gerard DeRose',
    author_email='jderose@novacut.com',
    license='LGPLv3+',
    packages=[
        'degu',
        'degu.tests',
    ],
    ext_modules=[
        Extension('degu._base',
            sources=['degu/_base.c'],
            extra_compile_args=[
                '-Werror',  # Make all warnings into errors
                '-std=gnu11',  # Soon to be gcc default
            ],
        ),
    ],
    cmdclass={
        'test': Test,
    },
    platforms=['POSIX'],
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU Lesser General Public License v3 or later (LGPLv3+)',
        'Natural Language :: English',
        'Operating System :: POSIX :: Linux',
        'Programming Language :: C',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3 :: Only',
        'Programming Language :: Python :: Implementation :: CPython',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Internet :: WWW/HTTP :: HTTP Servers',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
)

