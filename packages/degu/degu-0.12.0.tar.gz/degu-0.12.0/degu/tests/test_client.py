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
Unit tests for the `degu.server` module`
"""

from unittest import TestCase
import os
import io
import socket
import ssl

from .helpers import DummySocket, FuzzTestCase
from degu.base import _TYPE_ERROR
from degu.sslhelpers import random_id
from degu.misc import TempPKI
from degu import base, client


# Good type and value permutations for the CLient *address*:
GOOD_ADDRESSES = (

    # 2-tuple for AF_INET or AF_INET6:
    ('www.wikipedia.org', 80),
    ('208.80.154.224', 80),
    ('2620:0:861:ed1a::1', 80),

    # 4-tuple for AF_INET6:
    ('2620:0:861:ed1a::1', 80, 0, 0),
    ('fe80::e8b:fdff:fe75:402c', 80, 0, 3),  # Link-local

    # str for AF_UNIX:
    '/tmp/my.socket',

    # bytes for AF_UNIX (Linux abstract name):
    b'\x0000022',
)


# Some bad address permutations:
BAD_TUPLE_ADDRESSES = (
    ('::1',),
    ('127.0.0.1',),
    ('::1', 5678, 0),
    ('127.0.0.1', 5678, 0),
    ('::1', 5678, 0, 0, 0),
    ('127.0.0.1', 5678, 0, 0, 0),
)


class TestNamedTuples(TestCase):
    def test_Response(self):
        tup = client.Response('da status', 'da reason', 'da headers', 'da body')
        self.assertIsInstance(tup, tuple)
        self.assertEqual(tup.status, 'da status')
        self.assertEqual(tup.reason, 'da reason')
        self.assertEqual(tup.headers, 'da headers')
        self.assertEqual(tup.body, 'da body')


class TestClosedConnectionError(TestCase):
    def test_init(self):
        conn = random_id()
        exc = client.ClosedConnectionError(conn)
        self.assertIs(exc.conn, conn)
        self.assertEqual(str(exc),
            'cannot use request() when connection is closed: {!r}'.format(conn)
        )


class TestUnconsumedResponseError(TestCase):
    def test_init(self):
        body = random_id()
        exc = client.UnconsumedResponseError(body)
        self.assertIs(exc.body, body)
        self.assertEqual(str(exc),
            'previous response body not consumed: {!r}'.format(body)
        )


class FuzzTestFunctions(FuzzTestCase):
    def test__read_response(self):
        for method in ('GET', 'HEAD', 'DELETE', 'PUT', 'POST'):
            self.fuzz(client._read_response, base.bodies, method)


class TestFunctions(TestCase):
    def test_build_client_sslctx(self):
        # Bad sslconfig type:
        with self.assertRaises(TypeError) as cm:
            client.build_client_sslctx('bad')
        self.assertEqual(str(cm.exception),
            _TYPE_ERROR.format('sslconfig', dict, str, 'bad')
        )
 
        # The remaining test both build_client_sslctx() directly, and the
        # pass-through from _validate_client_sslctx():
        client_sslctx_funcs = (
            client.build_client_sslctx,
            client._validate_client_sslctx,
        )

        # Bad sslconfig['check_hostname'] type:
        for func in client_sslctx_funcs:
            with self.assertRaises(TypeError) as cm:
                func({'check_hostname': 0})
            self.assertEqual(str(cm.exception),
                _TYPE_ERROR.format("sslconfig['check_hostname']", bool, int, 0)
            )

        # sslconfig['key_file'] without sslconfig['cert_file']:
        for func in client_sslctx_funcs:
            with self.assertRaises(ValueError) as cm:
                func({'key_file': '/my/client.key'})
            self.assertEqual(str(cm.exception), 
                "sslconfig['key_file'] provided without sslconfig['cert_file']"
            )

        # Non absulute, non normalized paths:
        good = {
            'ca_file': '/my/sever.ca',
            'ca_path': '/my/sever.ca.dir',
            'cert_file': '/my/client.cert',
            'key_file': '/my/client.key',
        }
        for key in good.keys():
            # Relative path:
            for func in client_sslctx_funcs:
                bad = good.copy()
                value = 'relative/path'
                bad[key] = value
                with self.assertRaises(ValueError) as cm:
                    func(bad)
                self.assertEqual(str(cm.exception),
                    'sslconfig[{!r}] is not an absulute, normalized path: {!r}'.format(key, value)
                )

            # Non-normalized path with directory traversal:
            for func in client_sslctx_funcs:
                bad = good.copy()
                value = '/my/../secret/path'
                bad[key] = value
                with self.assertRaises(ValueError) as cm:
                    func(bad)
                self.assertEqual(str(cm.exception),
                    'sslconfig[{!r}] is not an absulute, normalized path: {!r}'.format(key, value)
                )

            # Non-normalized path with trailing slash:
            for func in client_sslctx_funcs:
                bad = good.copy()
                value = '/sorry/very/strict/'
                bad[key] = value
                with self.assertRaises(ValueError) as cm:
                    func(bad)
                self.assertEqual(str(cm.exception),
                    'sslconfig[{!r}] is not an absulute, normalized path: {!r}'.format(key, value)
                )

        # Empty sslconfig, will verify against system-wide CAs, and
        # check_hostname should default to True:
        for func in client_sslctx_funcs:
            sslctx = func({})
            self.assertIsInstance(sslctx, ssl.SSLContext)
            self.assertEqual(sslctx.protocol, ssl.PROTOCOL_TLSv1_2)
            self.assertEqual(sslctx.verify_mode, ssl.CERT_REQUIRED)
            self.assertIs(sslctx.check_hostname, True)

        # We don't not allow check_hostname to be False when verifying against
        # the system-wide CAs:
        for func in client_sslctx_funcs:
            with self.assertRaises(ValueError) as cm:
                func({'check_hostname': False})
            self.assertEqual(str(cm.exception),
                'check_hostname must be True when using default verify paths'
            )

        # Should work fine when explicitly providing {'check_hostname': True}:
        for func in client_sslctx_funcs:
            sslctx = func({'check_hostname': True})
            self.assertIsInstance(sslctx, ssl.SSLContext)
            self.assertEqual(sslctx.protocol, ssl.PROTOCOL_TLSv1_2)
            self.assertEqual(sslctx.verify_mode, ssl.CERT_REQUIRED)
            self.assertIs(sslctx.check_hostname, True)

        # Authenticated client sslconfig:
        pki = TempPKI()
        sslconfig = pki.client_sslconfig
        self.assertEqual(set(sslconfig),
            {'ca_file', 'cert_file', 'key_file', 'check_hostname'}
        )
        self.assertIs(sslconfig['check_hostname'], False)
        for func in client_sslctx_funcs:
            sslctx = func(sslconfig)
            self.assertIsInstance(sslctx, ssl.SSLContext)
            self.assertEqual(sslctx.protocol, ssl.PROTOCOL_TLSv1_2)
            self.assertEqual(sslctx.verify_mode, ssl.CERT_REQUIRED)
            self.assertIs(sslctx.check_hostname, False)

        # check_hostname should default to True:
        del sslconfig['check_hostname']
        for func in client_sslctx_funcs:
            sslctx = func(sslconfig)
            self.assertIsInstance(sslctx, ssl.SSLContext)
            self.assertEqual(sslctx.protocol, ssl.PROTOCOL_TLSv1_2)
            self.assertEqual(sslctx.verify_mode, ssl.CERT_REQUIRED)
            self.assertIs(sslctx.check_hostname, True)

        # Anonymous client sslconfig:
        sslconfig = pki.anonymous_client_sslconfig
        self.assertEqual(set(sslconfig), {'ca_file', 'check_hostname'})
        self.assertIs(sslconfig['check_hostname'], False)
        for func in client_sslctx_funcs:
            sslctx = func(sslconfig)
            self.assertIsInstance(sslctx, ssl.SSLContext)
            self.assertEqual(sslctx.protocol, ssl.PROTOCOL_TLSv1_2)
            self.assertEqual(sslctx.verify_mode, ssl.CERT_REQUIRED)
            self.assertIs(sslctx.check_hostname, False)

        # check_hostname should default to True:
        del sslconfig['check_hostname']
        for func in client_sslctx_funcs:
            sslctx = func(sslconfig)
            self.assertIsInstance(sslctx, ssl.SSLContext)
            self.assertEqual(sslctx.protocol, ssl.PROTOCOL_TLSv1_2)
            self.assertEqual(sslctx.verify_mode, ssl.CERT_REQUIRED)
            self.assertIs(sslctx.check_hostname, True)

    def test__validate_request(self):
        # Pre-build all valid types of length-encoded bodies:
        data = os.urandom(17)
        length_bodies = (
            data,
            bytearray(data),
            base.Body(io.BytesIO(data), 17),
            base.BodyIter([data], 17),
        )

        # Pre-build all valid types of chunk-encoded bodies:
        chunked_bodies = (
            base.ChunkedBody(io.BytesIO()),
            base.ChunkedBodyIter([])
        )

        # Bad method:
        with self.assertRaises(ValueError) as cm:
            client._validate_request(base.bodies, 'get', '/foo', {}, None)
        self.assertEqual(str(cm.exception), "invalid method: 'get'")

        # Non-casefolded header name:
        headers = {'Content-Type': 'text/plain', 'X-Stuff': 'hello'}
        with self.assertRaises(ValueError) as cm:
            client._validate_request(base.bodies, 'GET', '/foo', headers, None)
        self.assertEqual(str(cm.exception),
            "non-casefolded header name: 'Content-Type'"
        )

        # Body is None but content-length header included:
        headers = {'content-length': 17}
        with self.assertRaises(ValueError) as cm:
            client._validate_request(base.bodies, 'POST', '/foo', headers, None)
        self.assertEqual(str(cm.exception),
            "headers['content-length'] included when body is None"
        )

        # Body is None but transfer-encoding header included:
        headers = {'transfer-encoding': 'chunked'}
        with self.assertRaises(ValueError) as cm:
            client._validate_request(base.bodies, 'POST', '/foo', headers, None)
        self.assertEqual(str(cm.exception),
            "headers['transfer-encoding'] included when body is None"
        )

        # Bad body type:
        headers = {'content-type': 'text/plain'}
        with self.assertRaises(TypeError) as cm:
            client._validate_request(base.bodies, 'GET', '/foo', headers, 'hello')
        self.assertEqual(str(cm.exception),
            "bad request body type: <class 'str'>"
        )

        # 'transfer-encoding' header with a length-encoded body:
        for body in length_bodies:
            headers = {'transfer-encoding': 'chunked'}
            with self.assertRaises(ValueError) as cm:
                client._validate_request(base.bodies, 'POST', '/foo', headers, body)
            self.assertEqual(str(cm.exception),
                "headers['transfer-encoding'] with length-encoded body"
            )
            self.assertEqual(headers,
                {'content-length': 17, 'transfer-encoding': 'chunked'}
            )

        # headers['content-length'] != len(body):
        for body in length_bodies:
            headers = {'content-length': 16}
            with self.assertRaises(ValueError) as cm:
                client._validate_request(base.bodies, 'POST', '/foo', headers, body)
            self.assertEqual(str(cm.exception),
                "headers['content-length'] != len(body): 16 != 17"
            )
            self.assertEqual(headers, {'content-length': 16})

        # 'content-length' header with a chunk-encoded body:
        for body in chunked_bodies:
            headers = {'content-length': 5}
            with self.assertRaises(ValueError) as cm:
                client._validate_request(base.bodies, 'POST', '/foo', headers, body)
            self.assertEqual(str(cm.exception),
                "headers['content-length'] with chunk-encoded body"
            )
            self.assertEqual(headers,
                {'content-length': 5, 'transfer-encoding': 'chunked'}
            )

        # headers['transfer-encoding'] != 'chunked':
        for body in chunked_bodies:
            headers = {'transfer-encoding': 'clumped'}
            with self.assertRaises(ValueError) as cm:
                client._validate_request(base.bodies, 'POST', '/foo', headers, body)
            self.assertEqual(str(cm.exception),
                "headers['transfer-encoding'] is invalid: 'clumped'"
            )
            self.assertEqual(headers, {'transfer-encoding': 'clumped'})

        # Cannot include body when method is GET, HEAD, or DELETE:
        for body in (length_bodies + chunked_bodies):
            for method in ('GET', 'HEAD', 'DELETE'):
                with self.assertRaises(ValueError) as cm:
                    client._validate_request(base.bodies, method, '/foo', {}, body)
                self.assertEqual(str(cm.exception),
                    'cannot include body in a {} request'.format(method)
                )

        # No in-place header modification should happen when body is None:
        for method in ('GET', 'HEAD', 'DELETE', 'PUT', 'POST'):
            headers = {}
            self.assertIsNone(
                client._validate_request(base.bodies, method, '/foo', headers, None)
            )
            self.assertEqual(headers, {})

        # Test with all the length-encoded body types:
        for method in ('PUT', 'POST'):
            for body in length_bodies:
                headers = {}
                self.assertIsNone(
                    client._validate_request(base.bodies, method, '/foo', headers, body)
                )
                self.assertEqual(headers, {'content-length': 17})

        # Test with all the chunk-encoded body types:
        for method in ('PUT', 'POST'):
            for body in chunked_bodies:
                headers = {}
                self.assertIsNone(
                    client._validate_request(base.bodies, method, '/foo', headers, body)
                )
                self.assertEqual(headers, {'transfer-encoding': 'chunked'})

    def test__write_request(self):
        # Empty headers, no body:
        wfile = io.BytesIO()
        self.assertEqual(
            client._write_request(wfile, 'GET', '/', {}, None),
            18
        )
        self.assertEqual(wfile.tell(), 18)
        self.assertEqual(wfile.getvalue(), b'GET / HTTP/1.1\r\n\r\n')

        # One header:
        headers = {'foo': 17}  # Make sure to test with int header value
        wfile = io.BytesIO()
        self.assertEqual(
            client._write_request(wfile, 'GET', '/', headers, None),
            27
        )
        self.assertEqual(wfile.tell(), 27)
        self.assertEqual(wfile.getvalue(),
            b'GET / HTTP/1.1\r\nfoo: 17\r\n\r\n'
        )

        # Two headers:
        headers = {'foo': 17, 'bar': 'baz'}
        wfile = io.BytesIO()
        self.assertEqual(
            client._write_request(wfile, 'GET', '/', headers, None),
            37
        )
        self.assertEqual(wfile.tell(), 37)
        self.assertEqual(wfile.getvalue(),
            b'GET / HTTP/1.1\r\nbar: baz\r\nfoo: 17\r\n\r\n'
        )

        # body is bytes:
        wfile = io.BytesIO()
        self.assertEqual(
            client._write_request(wfile, 'GET', '/', headers, b'hello'),
            42
        )
        self.assertEqual(wfile.tell(), 42)
        self.assertEqual(wfile.getvalue(),
            b'GET / HTTP/1.1\r\nbar: baz\r\nfoo: 17\r\n\r\nhello'
        )

        # body is bytearray:
        body = bytearray(b'hello')
        wfile = io.BytesIO()
        self.assertEqual(
            client._write_request(wfile, 'GET', '/', headers, body),
            42
        )
        self.assertEqual(wfile.tell(), 42)
        self.assertEqual(wfile.getvalue(),
            b'GET / HTTP/1.1\r\nbar: baz\r\nfoo: 17\r\n\r\nhello'
        )

        # body is base.Body:
        rfile = io.BytesIO(b'hello')
        body = base.Body(rfile, 5)
        wfile = io.BytesIO()
        self.assertEqual(
            client._write_request(wfile, 'GET', '/', headers, body),
            42
        )
        self.assertEqual(rfile.tell(), 5)
        self.assertEqual(wfile.tell(), 42)
        self.assertEqual(wfile.getvalue(),
            b'GET / HTTP/1.1\r\nbar: baz\r\nfoo: 17\r\n\r\nhello'
        )

        # body is base.ChunkedBody:
        rfile = io.BytesIO(b'5\r\nhello\r\n0\r\n\r\n')
        body = base.ChunkedBody(rfile)
        wfile = io.BytesIO()
        self.assertEqual(
            client._write_request(wfile, 'GET', '/', headers, body),
            52
        )
        self.assertEqual(rfile.tell(), 15)
        self.assertEqual(wfile.tell(), 52)
        self.assertEqual(wfile.getvalue(),
            b'GET / HTTP/1.1\r\nbar: baz\r\nfoo: 17\r\n\r\n5\r\nhello\r\n0\r\n\r\n'
        )

    def test__read_response(self):
        # No headers, no body:
        lines = ''.join([
            'HTTP/1.1 200 OK\r\n',
            '\r\n',
        ]).encode('latin_1')
        rfile = io.BytesIO(lines)
        r = client._read_response(rfile, base.bodies, 'GET')
        self.assertIsInstance(r, client.Response)
        self.assertEqual(r, (200, 'OK', {}, None))

        # Content-Length, body should be base.Body:
        lines = ''.join([
            'HTTP/1.1 200 OK\r\n',
            'Content-Length: 17\r\n',
            '\r\n',
        ]).encode('latin_1')
        data = os.urandom(17)
        rfile = io.BytesIO(lines + data)
        r = client._read_response(rfile, base.bodies, 'GET')
        self.assertIsInstance(r, client.Response)
        self.assertEqual(r.status, 200)
        self.assertEqual(r.reason, 'OK')
        self.assertEqual(r.headers, {'content-length': 17})
        self.assertIsInstance(r.body, base.Body)
        self.assertIs(r.body.rfile, rfile)
        self.assertIs(r.body.closed, False)
        self.assertEqual(r.body._remaining, 17)
        self.assertEqual(rfile.tell(), len(lines))
        self.assertEqual(r.body.read(), data)
        self.assertEqual(rfile.tell(), len(lines) + len(data))
        self.assertIs(r.body.closed, True)
        self.assertEqual(r.body._remaining, 0)

        # Like above, except this time for a HEAD request:
        rfile = io.BytesIO(lines + data)
        r = client._read_response(rfile, base.bodies, 'HEAD')
        self.assertIsInstance(r, client.Response)
        self.assertEqual(r, (200, 'OK', {'content-length': 17}, None))

        # Transfer-Encoding, body should be base.ChunkedBody:
        lines = ''.join([
            'HTTP/1.1 200 OK\r\n',
            'Transfer-Encoding: chunked\r\n',
            '\r\n',
        ]).encode('latin_1')
        chunk1 = os.urandom(21)
        chunk2 = os.urandom(17)
        chunk3 = os.urandom(19)
        rfile = io.BytesIO()
        total = rfile.write(lines)
        for chunk in [chunk1, chunk2, chunk3, b'']:
            total += base.write_chunk(rfile, (None, chunk))
        self.assertEqual(rfile.tell(), total)
        rfile.seek(0)
        r = client._read_response(rfile, base.bodies, 'GET')
        self.assertIsInstance(r, client.Response)
        self.assertEqual(r.status, 200)
        self.assertEqual(r.reason, 'OK')
        self.assertEqual(r.headers, {'transfer-encoding': 'chunked'})
        self.assertIsInstance(r.body, base.ChunkedBody)
        self.assertIs(r.body.rfile, rfile)
        self.assertEqual(rfile.tell(), len(lines))
        self.assertIs(r.body.closed, False)
        self.assertEqual(list(r.body),
            [
                (None, chunk1),
                (None, chunk2),
                (None, chunk3),
                (None, b''),
            ]
        )
        self.assertIs(r.body.closed, True)
        self.assertEqual(rfile.tell(), total)


class TestConnection(TestCase):
    def test_init(self):
        sock = DummySocket()
        base_headers = {'host': 'www.example.com:80'}
        inst = client.Connection(sock, base_headers, base.bodies)
        self.assertIsInstance(inst, client.Connection)
        self.assertIs(inst.sock, sock)
        self.assertIs(inst.base_headers, base_headers)
        self.assertEqual(inst.base_headers, {'host': 'www.example.com:80'})
        self.assertIs(inst.bodies, base.bodies)
        self.assertIs(inst._rfile, sock._rfile)
        self.assertIs(inst._wfile, sock._wfile)
        self.assertIsNone(inst._response_body)
        self.assertIs(inst.closed, False)
        self.assertEqual(sock._calls, [
            ('makefile', 'rb', {'buffering': base.STREAM_BUFFER_SIZE}),
            ('makefile', 'wb', {'buffering': base.STREAM_BUFFER_SIZE}),
        ])

    def test_del(self):
        class ConnectionSubclass(client.Connection):
            def __init__(self):
                self._calls = 0

            def close(self):
                self._calls += 1

        inst = ConnectionSubclass()
        self.assertEqual(inst._calls, 0)
        self.assertIsNone(inst.__del__())
        self.assertEqual(inst._calls, 1)
        self.assertIsNone(inst.__del__())
        self.assertEqual(inst._calls, 2)

    def test_close(self):
        sock = DummySocket()
        inst = client.Connection(sock, None, base.bodies)
        sock._calls.clear()

        # When Connection.closed is False:
        self.assertIsNone(inst.close())
        self.assertEqual(sock._calls, [('shutdown', socket.SHUT_RDWR)])
        self.assertIsNone(inst.sock)
        self.assertIsNone(inst._response_body)
        self.assertIs(inst.closed, True)

        # Now when Connection.closed is True:
        self.assertIsNone(inst.close())
        self.assertEqual(sock._calls, [('shutdown', socket.SHUT_RDWR)])
        self.assertIsNone(inst.sock)
        self.assertIsNone(inst._response_body)
        self.assertIs(inst.closed, True)

    def test_request(self):
        # Test when the connection has already been closed:
        sock = DummySocket()
        conn = client.Connection(sock, None, base.bodies)
        sock._calls.clear()
        conn.sock = None
        with self.assertRaises(client.ClosedConnectionError) as cm:
            conn.request('GET', '/', {}, None)
        self.assertIs(cm.exception.conn, conn)
        self.assertEqual(str(cm.exception),
            'cannot use request() when connection is closed: {!r}'.format(conn)
        )
        self.assertEqual(sock._calls, [])
        self.assertIsNone(conn.sock)
        self.assertIsNone(conn._response_body)
        self.assertIs(conn.closed, True)

        # Test when the previous response body wasn't consumed:
        class DummyBody:
            closed = False

        sock = DummySocket()
        conn = client.Connection(sock, None, base.bodies)
        sock._calls.clear()
        conn._response_body = DummyBody
        with self.assertRaises(client.UnconsumedResponseError) as cm:
            conn.request('GET', '/', {}, None)
        self.assertIs(cm.exception.body, DummyBody)
        self.assertEqual(str(cm.exception),
            'previous response body not consumed: {!r}'.format(DummyBody)
        )
        # Make sure Connection.close() was called:
        self.assertEqual(sock._calls, [('shutdown', socket.SHUT_RDWR)])
        self.assertIsNone(conn.sock)
        self.assertIsNone(conn._response_body)
        self.assertIs(conn.closed, True)

    def get_subclass(self, marker):
        class Subclass(client.Connection):
            def __init__(self, marker):
                self._marker = marker
                self._args = None
                self._kw = None

            def request(self, *args, **kw):
                assert self._args is None
                assert self._kw is None
                self._args = args
                self._kw = kw
                return self._marker

        return Subclass(marker)

    def test_put(self):
        marker = random_id()
        inst = self.get_subclass(marker)
        uri = random_id()
        key = random_id().lower()
        value = random_id()
        headers = {key: value}
        body = os.urandom(16)
        self.assertIs(inst.put(uri, headers, body), marker)
        self.assertEqual(inst._args, ('PUT', uri, {key: value}, body))
        self.assertEqual(inst._kw, {})

    def test_post(self):
        marker = random_id()
        inst = self.get_subclass(marker)
        uri = random_id()
        key = random_id().lower()
        value = random_id()
        headers = {key: value}
        body = os.urandom(16)
        self.assertIs(inst.post(uri, headers, body), marker)
        self.assertEqual(inst._args, ('POST', uri, {key: value}, body))
        self.assertEqual(inst._kw, {})

    def test_get(self):
        marker = random_id()
        inst = self.get_subclass(marker)
        uri = random_id()
        key = random_id().lower()
        value = random_id()
        headers = {key: value}
        self.assertIs(inst.get(uri, headers), marker)
        self.assertEqual(inst._args, ('GET', uri, {key: value}, None))
        self.assertEqual(inst._kw, {})

    def test_head(self):
        marker = random_id()
        inst = self.get_subclass(marker)
        uri = random_id()
        key = random_id().lower()
        value = random_id()
        headers = {key: value}
        self.assertIs(inst.head(uri, headers), marker)
        self.assertEqual(inst._args, ('HEAD', uri, {key: value}, None))
        self.assertEqual(inst._kw, {})

    def test_delete(self):
        marker = random_id()
        inst = self.get_subclass(marker)
        uri = random_id()
        key = random_id().lower()
        value = random_id()
        headers = {key: value}
        self.assertIs(inst.delete(uri, headers), marker)
        self.assertEqual(inst._args, ('DELETE', uri, {key: value}, None))
        self.assertEqual(inst._kw, {})   


class TestClient(TestCase):
    def test_init(self):
        # Bad address type:
        with self.assertRaises(TypeError) as cm:
            client.Client(1234)
        self.assertEqual(str(cm.exception),
            _TYPE_ERROR.format('address', (tuple, str, bytes), int, 1234)
        )

        # Wrong number of items in address tuple:
        for address in BAD_TUPLE_ADDRESSES:
            self.assertIn(len(address), {1, 3, 5})
            with self.assertRaises(ValueError) as cm:
                client.Client(address)
            self.assertEqual(str(cm.exception),
                'address: must have 2 or 4 items; got {!r}'.format(address)
            )

        # Non-absolute/non-normalized AF_UNIX filename:
        with self.assertRaises(ValueError) as cm:
            client.Client('foo')
        self.assertEqual(str(cm.exception),
            "address: bad socket filename: 'foo'"
        )

        # Good address type and value permutations:
        for address in GOOD_ADDRESSES:
            inst = client.Client(address)
            self.assertIs(inst.address, address)
            self.assertEqual(inst.options, {})
            if isinstance(address, tuple):
                self.assertEqual(inst.host, client._build_host(80, *address))
            else:
                self.assertIsNone(inst.host)
            self.assertEqual(inst.timeout, 60)
            self.assertIs(inst.bodies, base.bodies)
            self.assertIsNone(inst.on_connect)

            # Test overriding the `host` option:
            my_host = '.'.join([random_id() for i in range(3)])
            inst = client.Client(address, host=my_host)
            self.assertIs(inst.address, address)
            self.assertEqual(inst.options, {'host': my_host})
            self.assertIs(inst.host, my_host)
            self.assertEqual(inst.timeout, 60)
            self.assertIs(inst.bodies, base.bodies)
            self.assertIsNone(inst.on_connect)

            # Test overriding `host` option with `None`:
            inst = client.Client(address, host=None)
            self.assertIs(inst.address, address)
            self.assertEqual(inst.options, {'host': None})
            self.assertIsNone(inst.host)
            self.assertEqual(inst.timeout, 60)
            self.assertIs(inst.bodies, base.bodies)
            self.assertIsNone(inst.on_connect)

            # Test overriding the `timeout` option:
            inst = client.Client(address, timeout=17)
            self.assertIs(inst.address, address)
            self.assertEqual(inst.options, {'timeout': 17})
            if isinstance(address, tuple):
                self.assertEqual(inst.host, client._build_host(80, *address))
            else:
                self.assertIsNone(inst.host)
            self.assertEqual(inst.timeout, 17)
            self.assertIs(inst.bodies, base.bodies)
            self.assertIsNone(inst.on_connect)

            # Test overriding the `bodies` option:
            my_bodies = base.BodiesAPI('foo', 'bar', 'stuff', 'junk')
            inst = client.Client(address, bodies=my_bodies)
            self.assertIs(inst.address, address)
            self.assertEqual(inst.options, {'bodies': my_bodies})
            if isinstance(address, tuple):
                self.assertEqual(inst.host, client._build_host(80, *address))
            else:
                self.assertIsNone(inst.host)
            self.assertEqual(inst.timeout, 60)
            self.assertIs(inst.bodies, my_bodies)
            self.assertIsNone(inst.on_connect)

            # Test overriding the `on_connect` option:
            inst = client.Client(address, on_connect=None)
            if isinstance(address, tuple):
                self.assertEqual(inst.host, client._build_host(80, *address))
            else:
                self.assertIsNone(inst.host)
            self.assertEqual(inst.timeout, 60)
            self.assertIs(inst.bodies, base.bodies)
            self.assertIsNone(inst.on_connect)

            with self.assertRaises(TypeError) as cm:
                client.Client(address, on_connect='hello')
            self.assertEqual(str(cm.exception),
                "on_connect: not callable: 'hello'"
            )

            def my_on_connect(conn):
                return True
            inst = client.Client(address, on_connect=my_on_connect)
            if isinstance(address, tuple):
                self.assertEqual(inst.host, client._build_host(80, *address))
            else:
                self.assertIsNone(inst.host)
            self.assertEqual(inst.timeout, 60)
            self.assertIs(inst.bodies, base.bodies)
            self.assertIs(inst.on_connect, my_on_connect)

            # Test overriding all the options together:
            options = {
                'host': my_host,
                'timeout': 16.9,
                'bodies': my_bodies,
                'on_connect': my_on_connect,
            }
            inst = client.Client(address, **options)
            self.assertIs(inst.address, address)
            self.assertEqual(inst.options, options)
            self.assertIs(inst.host, my_host)
            self.assertEqual(inst.timeout, 16.9)
            self.assertIs(inst.bodies, my_bodies)
            self.assertIs(inst.on_connect, my_on_connect)

    def test_repr(self):
        class Custom(client.Client):
            pass

        for address in GOOD_ADDRESSES:
            inst = client.Client(address)
            self.assertEqual(repr(inst), 'Client({!r})'.format(address))
            inst = Custom(address)
            self.assertEqual(repr(inst), 'Custom({!r})'.format(address))

    def test_connect(self):
        class ClientSubclass(client.Client):
            def __init__(self, sock, host, on_connect=None):
                self.__sock = sock
                self._base_headers = {'host': host}
                self.bodies = base.bodies
                self.on_connect = on_connect

            def create_socket(self):
                return self.__sock

        sock = DummySocket()
        host = random_id().lower()
        inst = ClientSubclass(sock, host)
        self.assertIsNone(inst.on_connect)
        conn = inst.connect()
        self.assertIsInstance(conn, client.Connection)
        self.assertIs(conn.sock, sock)
        self.assertIs(conn.base_headers, inst._base_headers)
        self.assertIs(conn.bodies, base.bodies)
        self.assertIs(conn._rfile, sock._rfile)
        self.assertIs(conn._wfile, sock._wfile)
        self.assertEqual(sock._calls, [
            ('makefile', 'rb', {'buffering': base.STREAM_BUFFER_SIZE}),
            ('makefile', 'wb', {'buffering': base.STREAM_BUFFER_SIZE}),
        ])

        # Should return a new Connection instance each time:
        conn2 = inst.connect()
        self.assertIsNot(conn2, conn)
        self.assertIsInstance(conn2, client.Connection)
        self.assertIs(conn2.sock, sock)
        self.assertIs(conn.base_headers, inst._base_headers)
        self.assertIs(conn.bodies, base.bodies)
        self.assertIs(conn2._rfile, sock._rfile)
        self.assertIs(conn2._wfile, sock._wfile)
        self.assertEqual(sock._calls, [
            ('makefile', 'rb', {'buffering': base.STREAM_BUFFER_SIZE}),
            ('makefile', 'wb', {'buffering': base.STREAM_BUFFER_SIZE}),
            ('makefile', 'rb', {'buffering': base.STREAM_BUFFER_SIZE}),
            ('makefile', 'wb', {'buffering': base.STREAM_BUFFER_SIZE}),
        ])

        # on_connect() returns True:
        def on_connect_true(conn):
            return True
        sock = DummySocket()
        host = random_id().lower()
        inst = ClientSubclass(sock, host, on_connect_true)
        self.assertIs(inst.on_connect, on_connect_true)
        conn = inst.connect()
        self.assertIsInstance(conn, client.Connection)
        self.assertIs(conn.sock, sock)
        self.assertIs(conn.base_headers, inst._base_headers)
        self.assertIs(conn.bodies, base.bodies)
        self.assertIs(conn._rfile, sock._rfile)
        self.assertIs(conn._wfile, sock._wfile)
        self.assertEqual(sock._calls, [
            ('makefile', 'rb', {'buffering': base.STREAM_BUFFER_SIZE}),
            ('makefile', 'wb', {'buffering': base.STREAM_BUFFER_SIZE}),
        ])

        # on_connect() does not return True:
        def on_connect_false(conn):
            return 1
        sock = DummySocket()
        host = random_id().lower()
        inst = ClientSubclass(sock, host, on_connect_false)
        self.assertIs(inst.on_connect, on_connect_false)
        with self.assertRaises(ValueError) as cm:
            conn = inst.connect()
        self.assertEqual(str(cm.exception), 'on_connect() did not return True')


class TestSSLClient(TestCase):
    def test_init(self):
        # sslctx is not an ssl.SSLContext:
        with self.assertRaises(TypeError) as cm:
            client.SSLClient('foo', None)
        self.assertEqual(str(cm.exception), 'sslctx must be an ssl.SSLContext')

        # Bad SSL protocol version:
        sslctx = ssl.SSLContext(ssl.PROTOCOL_SSLv3)
        with self.assertRaises(ValueError) as cm:
            client.SSLClient(sslctx, None)
        self.assertEqual(str(cm.exception),
            'sslctx.protocol must be ssl.PROTOCOL_TLSv1_2'
        )

        # Note: Python 3.3.4 (and presumably 3.4.0) now disables SSLv2 by
        # default (which is good); Degu enforces this (also good), but because
        # we cannot unset the ssl.OP_NO_SSLv2 bit, we can't unit test to check
        # that Degu enforces this, so for now, we set the bit here so it works
        # with Python 3.3.3 still; see: http://bugs.python.org/issue20207
        sslctx = ssl.SSLContext(ssl.PROTOCOL_TLSv1_2)
        sslctx.options |= ssl.OP_NO_SSLv2

        # not (options & ssl.OP_NO_COMPRESSION)
        sslctx.options |= ssl.OP_NO_SSLv2
        with self.assertRaises(ValueError) as cm:
            client.SSLClient(sslctx, None)
        self.assertEqual(str(cm.exception),
            'sslctx.options must include ssl.OP_NO_COMPRESSION'
        )

        # verify_mode is not ssl.CERT_REQUIRED:
        sslctx.options |= ssl.OP_NO_COMPRESSION
        with self.assertRaises(ValueError) as cm:
            client.SSLClient(sslctx, None)
        self.assertEqual(str(cm.exception),
            'sslctx.verify_mode must be ssl.CERT_REQUIRED'
        )

        #############################
        # Good sslctx from here on...
        sslctx.verify_mode = ssl.CERT_REQUIRED

        # Bad address type:
        with self.assertRaises(TypeError) as cm:
            client.SSLClient(sslctx, 1234)
        self.assertEqual(str(cm.exception),
            _TYPE_ERROR.format('address', (tuple, str, bytes), int, 1234)
        )

        # Wrong number of items in address tuple:
        for address in BAD_TUPLE_ADDRESSES:
            self.assertIn(len(address), {1, 3, 5})
            with self.assertRaises(ValueError) as cm:
                client.SSLClient(sslctx, address)
            self.assertEqual(str(cm.exception),
                'address: must have 2 or 4 items; got {!r}'.format(address)
            )

        # Non-absolute/non-normalized AF_UNIX filename:
        with self.assertRaises(ValueError) as cm:
            client.SSLClient(sslctx, 'foo')
        self.assertEqual(str(cm.exception),
            "address: bad socket filename: 'foo'"
        )

        # Good address type and value permutations:
        for address in GOOD_ADDRESSES:
            inst = client.SSLClient(sslctx, address)
            self.assertIs(inst.address, address)
            self.assertEqual(inst.options, {})
            if isinstance(address, tuple):
                self.assertEqual(inst.host, client._build_host(443, *address))
                self.assertIs(inst.ssl_host, address[0])
            else:
                self.assertIsNone(inst.host)
                self.assertIsNone(inst.ssl_host)
            self.assertEqual(inst.timeout, 60)
            self.assertIs(inst.bodies, base.bodies)
            self.assertIsNone(inst.on_connect)

            # Test overriding the `host` option:
            my_host = '.'.join([random_id() for i in range(3)])
            inst = client.SSLClient(sslctx, address, host=my_host)
            self.assertIs(inst.address, address)
            self.assertEqual(inst.options, {'host': my_host})
            self.assertIs(inst.host, my_host)
            self.assertEqual(inst.timeout, 60)
            self.assertIs(inst.bodies, base.bodies)
            self.assertIsNone(inst.on_connect)

            # Test overriding the `host` option with `None`:
            inst = client.SSLClient(sslctx, address, host=None)
            self.assertIs(inst.address, address)
            self.assertEqual(inst.options, {'host': None})
            self.assertIsNone(inst.host)
            self.assertEqual(inst.timeout, 60)
            self.assertIs(inst.bodies, base.bodies)
            self.assertIsNone(inst.on_connect)

            # Test overriding the `ssl_host` options:
            my_ssl_host = '.'.join([random_id(10) for i in range(4)])
            inst = client.SSLClient(sslctx, address, ssl_host=my_ssl_host)
            self.assertIs(inst.address, address)
            self.assertEqual(inst.options, {'ssl_host': my_ssl_host})
            self.assertIs(inst.ssl_host, my_ssl_host)
            self.assertEqual(inst.timeout, 60)
            self.assertIs(inst.bodies, base.bodies)
            self.assertIsNone(inst.on_connect)

            # Test overriding the `ssl_host` option with `None`:
            inst = client.SSLClient(sslctx, address, ssl_host=None)
            self.assertIs(inst.address, address)
            self.assertEqual(inst.options, {'ssl_host': None})
            self.assertIsNone(inst.ssl_host)
            self.assertEqual(inst.timeout, 60)
            self.assertIs(inst.bodies, base.bodies)
            self.assertIsNone(inst.on_connect)

            # Test overriding the `timeout` option:
            inst = client.SSLClient(sslctx, address, timeout=17)
            self.assertIs(inst.address, address)
            self.assertEqual(inst.options, {'timeout': 17})
            if isinstance(address, tuple):
                self.assertEqual(inst.host, client._build_host(443, *address))
                self.assertIs(inst.ssl_host, address[0])
            else:
                self.assertIsNone(inst.host)
                self.assertIsNone(inst.ssl_host)
            self.assertEqual(inst.timeout, 17)
            self.assertIs(inst.bodies, base.bodies)
            self.assertIsNone(inst.on_connect)

            # Test overriding the `bodies` option:
            my_bodies = base.BodiesAPI('foo', 'bar', 'stuff', 'junk')
            inst = client.SSLClient(sslctx, address, bodies=my_bodies)
            self.assertIs(inst.address, address)
            self.assertEqual(inst.options, {'bodies': my_bodies})
            if isinstance(address, tuple):
                self.assertEqual(inst.host, client._build_host(443, *address))
                self.assertIs(inst.ssl_host, address[0])
            else:
                self.assertIsNone(inst.host)
                self.assertIsNone(inst.ssl_host)
            self.assertEqual(inst.timeout, 60)
            self.assertIs(inst.bodies, my_bodies)
            self.assertIsNone(inst.on_connect)

            # Test overriding the `on_connect` option:
            with self.assertRaises(TypeError) as cm:
                client.SSLClient(sslctx, address, on_connect='hello')
            self.assertEqual(str(cm.exception),
                "on_connect: not callable: 'hello'"
            )
            def my_on_connect(conn):
                return True
            inst = client.SSLClient(sslctx, address, on_connect=my_on_connect)
            if isinstance(address, tuple):
                self.assertEqual(inst.host, client._build_host(443, *address))
                self.assertIs(inst.ssl_host, address[0])
            else:
                self.assertIsNone(inst.host)
                self.assertIsNone(inst.ssl_host)
            self.assertEqual(inst.timeout, 60)
            self.assertIs(inst.bodies, base.bodies)
            self.assertIs(inst.on_connect, my_on_connect)

            # Test overriding the `on_connect` option with `None`:
            inst = client.SSLClient(sslctx, address, on_connect=None)
            if isinstance(address, tuple):
                self.assertEqual(inst.host, client._build_host(443, *address))
                self.assertIs(inst.ssl_host, address[0])
            else:
                self.assertIsNone(inst.host)
                self.assertIsNone(inst.ssl_host)
            self.assertEqual(inst.timeout, 60)
            self.assertIs(inst.bodies, base.bodies)
            self.assertIsNone(inst.on_connect)

            # Test overriding all the options together:
            options = {
                'host': my_host,
                'ssl_host': my_ssl_host,
                'timeout': 16.9,
                'bodies': my_bodies,
                'on_connect': my_on_connect,
            }
            inst = client.SSLClient(sslctx, address, **options)
            self.assertIs(inst.address, address)
            self.assertEqual(inst.options, options)
            self.assertIs(inst.host, my_host)
            self.assertIs(inst.ssl_host, my_ssl_host)
            self.assertEqual(inst.timeout, 16.9)
            self.assertIs(inst.bodies, my_bodies)
            self.assertIs(inst.on_connect, my_on_connect)

    def test_repr(self):
        class Custom(client.SSLClient):
            pass

        pki = TempPKI()
        sslctx = client.build_client_sslctx(pki.client_sslconfig)

        for address in GOOD_ADDRESSES:
            inst = client.SSLClient(sslctx, address)
            self.assertEqual(repr(inst),
                'SSLClient({!r}, {!r})'.format(sslctx, address)
            )
            inst = Custom(sslctx, address)
            self.assertEqual(repr(inst),
                'Custom({!r}, {!r})'.format(sslctx, address)
            )
