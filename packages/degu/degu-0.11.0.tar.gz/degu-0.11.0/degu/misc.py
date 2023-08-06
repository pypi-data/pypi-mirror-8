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
Some tools for unit testing.

This module imports things that often wouldn't normally be needed except for
unit testing, so thus this separate module helps keep the baseline memory
footprint lower.
"""

import tempfile
import os
import shutil
import multiprocessing

from .base import _TYPE_ERROR
from .sslhelpers import PKI as _PKI
from .server import Server, SSLServer


class TempPKI(_PKI):
    def __init__(self, client_pki=True, bits=1024):
        # To make unit testing faster, we use 1024 bit keys by default, but this
        # is not the size you should use in production
        ssldir = tempfile.mkdtemp(prefix='TempPKI.')
        super().__init__(ssldir)
        self.server_ca_id = self.create_key(bits)
        self.create_ca(self.server_ca_id)
        self.server_id = self.create_key(bits)
        self.create_csr(self.server_id)
        self.issue_cert(self.server_id, self.server_ca_id)
        if client_pki:
            self.client_ca_id = self.create_key(bits)
            self.create_ca(self.client_ca_id)
            self.client_id = self.create_key(bits)
            self.create_csr(self.client_id)
            self.issue_cert(self.client_id, self.client_ca_id)

    def __del__(self):
        if os.path.isdir(self.ssldir):
            shutil.rmtree(self.ssldir)

    @property
    def server_sslconfig(self):
        return self.get_server_sslconfig(self.server_id, self.client_ca_id)

    @property
    def client_sslconfig(self):
        return self.get_client_sslconfig(self.server_ca_id, self.client_id)

    @property
    def anonymous_server_sslconfig(self):
        return self.get_anonymous_server_sslconfig(self.server_id)

    @property
    def anonymous_client_sslconfig(self):
        return self.get_anonymous_client_sslconfig(self.server_ca_id)


def _run_server(queue, address, app, **options):
    try:
        httpd = Server(address, app, **options)
        queue.put(httpd.address)
        httpd.serve_forever()
    except Exception as e:
        queue.put(e)
        raise e


def _run_sslserver(queue, sslconfig, address, app, **options):
    try:
        httpd = SSLServer(sslconfig, address, app, **options)
        queue.put(httpd.address)
        httpd.serve_forever()
    except Exception as e:
        queue.put(e)
        raise e


def _start_server(address, app, **options):
    import multiprocessing
    queue = multiprocessing.Queue()
    process = multiprocessing.Process(
        target=_run_server,
        args=(queue, address, app),
        kwargs=options,
        daemon=True,
    )
    process.start()
    address = queue.get()
    if isinstance(address, Exception):
        process.terminate()
        process.join()
        raise address
    return (process, address)


def _start_sslserver(sslconfig, address, app, **options):
    if not isinstance(sslconfig, dict):
        raise TypeError(
            _TYPE_ERROR.format('sslconfig', dict, type(sslconfig), sslconfig)
        )
    queue = multiprocessing.Queue()
    process = multiprocessing.Process(
        target=_run_sslserver,
        args=(queue, sslconfig, address, app),
        kwargs=options,
        daemon=True,
    )
    process.start()
    address = queue.get()
    if isinstance(address, Exception):
        process.terminate()
        process.join()
        raise address
    return (process, address)


class _TempProcess:
    def __del__(self):
        self.terminate()

    def terminate(self):
        if getattr(self, 'process', None) is not None:
            self.process.terminate()
            self.process.join()


class TempServer(_TempProcess):
    def __init__(self, address, app, **options):
        (self.process, self.address) = _start_server(address, app, **options)
        self.app = app
        self.options = options

    def __repr__(self):
        return '{}({!r}, {!r})'.format(
            self.__class__.__name__, self.address, self.app
        )


class TempSSLServer(_TempProcess):
    def __init__(self, sslconfig, address, app, **options):
        self.sslconfig = sslconfig
        (self.process, self.address) = _start_sslserver(
            sslconfig, address, app, **options
        )
        self.app = app
        self.options = options

    def __repr__(self):
        return '{}(<sslconfig>, {!r}, {!r})'.format(
            self.__class__.__name__, self.address, self.app
        )

