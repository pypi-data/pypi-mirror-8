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
Pure-Python equivalent of the `degu._base` C extension.

Although `degu._basepy` is automatically imported as a fall-back when the
`degu._base` C extension isn't available, this Python implementation really
isn't meant for production use (mainly because it's much, much slower).

This is a reference implementation whose purpose is only to help enforce the
correctness of the C implementation.

Note that the Python implementation is quite different in how it decodes and
validates the HTTP preamble.  Using a lookup table is very fast in C, but is
quite slow in Python.

For *VALUES*, the Python implementation:

    1. Uses ``bytes.decode('ascii')`` to prevent bytes whose high-bit is set

    2. Uses ``str.isprintable()`` to further restrict down to the same 95 byte
       values allowed by the C ``_VALUES`` table

For *KEYS*, the Python implementation:

    1. Uses ``bytes.decode('ascii')`` to prevent bytes whose high-bit is set

    2. Uses ``str.lower()`` to case-fold the header key

    3. Uses ``re.match()`` to further restrict down to the same 63 byte values
       allowed by the C ``_KEYS`` table

Although it might seem a bit hodge-podge, this approach is much faster than
doing lookup tables in pure-Python.

However, aside from the glaring performance difference, the Python and C
implementations should always behave *exactly* the same, and we have oodles of
unit tests to back this up.

By not using lookup tables in the Python implementation, we can better verify
the correctness of the C lookup tables.  Otherwise we could have two
implementations correctly using the same incorrect tables.

``str.isprintable()`` is an especially handy gem in this respect.
"""

import re

__all__ = (
    '_MAX_LINE_SIZE',
    '_MAX_HEADER_COUNT',
    '_read_preamble',
    'EmptyPreambleError',
)

_MAX_LINE_SIZE = 4096  # Max length of line in HTTP preamble, including CRLF
_MAX_HEADER_COUNT = 20

MAX_PREAMBLE_BYTES = 65536  # 64 KiB

_RE_KEYS = re.compile('^[-0-9a-z]+$')
_RE_CONTENT_LENGTH = re.compile(b'^[0-9]+$')

_URI = frozenset(
    b'%&+-./0123456789:=?ABCDEFGHIJKLMNOPQRSTUVWXYZ_abcdefghijklmnopqrstuvwxyz~'
)

GET = 'GET'
PUT = 'PUT'
POST = 'POST'
HEAD = 'HEAD'
DELETE = 'DELETE'
OK = 'OK'


def parse_method(method):
    if isinstance(method, str):
        method = method.encode()
    if method == b'GET':
        return GET
    if method == b'PUT':
        return PUT
    if method == b'POST':
        return POST
    if method == b'HEAD':
        return HEAD
    if method == b'DELETE':
        return DELETE
    raise ValueError('bad HTTP method: {!r}'.format(method))


def _decode_value(src, message):
    """
    Used to decode and validate header values, plus the preamble first line.
    """
    text = None
    try:
        text = src.decode('ascii')
    except ValueError:
        pass
    if text is None or not text.isprintable():
        raise ValueError(message.format(src))
    return text


def _decode_key(src, message):
    """
    Used to decode, validate, and case-fold header keys.
    """
    text = None
    try:
        text = src.decode('ascii').lower()
    except ValueError:
        pass
    if text is None or not _RE_KEYS.match(text):
        raise ValueError(message.format(src))
    return text


def _decode_uri(src):
    if _URI.issuperset(src):
        return src.decode()
    raise ValueError(
        'bad uri in request line: {!r}'.format(src)
    )


class EmptyPreambleError(ConnectionError):
    pass


def _READLINE(readline, maxsize):
    """
    Matches error checking semantics of the _READLINE() macro in degu/_base.c.

    It makes sense to focus on making the pure-Python implementation a very
    correct and easy to understand reference implementation, even when at the
    expense of performance.

    So although using this _READLINE() function means a rather hefty performance
    hit for the pure-Python implementation, it helps define the correct behavior
    of the dramatically higher-performance C implementation (aka, the
    implementation you actually want to use).
    """
    assert isinstance(maxsize, int) and maxsize in (_MAX_LINE_SIZE, 2)
    line = readline(maxsize)
    if type(line) is not bytes:
        raise TypeError(
            'rfile.readline() returned {!r}, should return {!r}'.format(
                type(line), bytes
            )
        )
    if len(line) > maxsize:
        raise ValueError(
            'rfile.readline() returned {} bytes, expected at most {}'.format(
                len(line), maxsize
            )
        )
    return line


def parse_response_line(line):
    if isinstance(line, str):
        line = line.encode()

    if len(line) < 15:
        raise ValueError('response line too short: {!r}'.format(line))
    if line[0:9] != b'HTTP/1.1 ' or line[12:13] != b' ':
        raise ValueError('bad response line: {!r}'.format(line))

    # status:
    status = None
    try:
        status = int(line[9:12])
    except ValueError:
        pass
    if status is None or not (100 <= status <= 599):
        raise ValueError('bad status in response line: {!r}'.format(line))

    # reason:
    if line[13:] == b'OK':
        reason = OK
    else:
        reason = _decode_value(line[13:], 'bad reason in response line: {!r}')

    # Return (status, reason) 2-tuple:
    return (status, reason)


def parse_request_line(line):
    if isinstance(line, str):
        line = line.encode()
    if len(line) < 14:
        raise ValueError('request line too short: {!r}'.format(line))
    if line[-9:] != b' HTTP/1.1':
        raise ValueError('bad protocol in request line: {!r}'.format(line))
    line = line[:-9]
    items = line.split(b' /', 1)
    if len(items) < 2:
        raise ValueError('bad inner request line: {!r}'.format(line))
    return (
        parse_method(items[0]),
        _decode_uri( b'/' + items[1])
    )


def parse_preamble(preamble):
    (first_line, *header_lines) = preamble.split(b'\r\n')
    first_line = _decode_value(first_line, 'bad bytes in first line: {!r}')
    headers = {}
    for line in header_lines:
        (key, value) = line.split(b': ')
        key = _decode_key(key, 'bad bytes in header name: {!r}')
        value = _decode_value(value, 'bad bytes in header value: {!r}')
        if headers.setdefault(key, value) is not value:
            raise ValueError(
                'duplicate header: {!r}'.format(line)
            )
    cl = headers.get('content-length')
    if cl is not None:
        if len(cl) > 16:
            raise ValueError(
                'content-length too long: {!r}...'.format(cl[:16].encode())
            )
        try:
            value = int(cl)
        except ValueError:
            value = None
        if value is None or value < 0:
            raise ValueError(
                'bad bytes in content-length: {!r}'.format(cl)
            )
        if value > 9007199254740992:
            raise ValueError(
                'content-length value too large: {!r}'.format(value)
            )
        headers['content-length'] = value
        if 'transfer-encoding' in headers:
            raise ValueError(
                'cannot have both content-length and transfer-encoding headers'
            )
    elif 'transfer-encoding' in headers:
        if headers['transfer-encoding'] != 'chunked':
            raise ValueError(
                'bad transfer-encoding: {!r}'.format(headers['transfer-encoding'])
            )
    return (first_line, headers)


def __read_headers(readline):
    headers = {}
    for i in range(_MAX_HEADER_COUNT):
        line = _READLINE(readline, _MAX_LINE_SIZE)
        crlf = line[-2:]
        if crlf != b'\r\n':
            raise ValueError('bad header line termination: {!r}'.format(crlf))
        if line == b'\r\n':  # Stop on the first empty CRLF terminated line
            return headers
        if len(line) < 6:
            raise ValueError('header line too short: {!r}'.format(line))
        assert line[-2:] == b'\r\n'
        line = line[:-2]
        try:
            (key, value) = line.split(b': ', 1)
        except ValueError:
            key = None
            value = None
        if not (key and value):
            raise ValueError('bad header line: {!r}'.format(line))
        if key.lower() == b'content-length':
            cl = None
            if _RE_CONTENT_LENGTH.match(value):
                try:
                    cl = int(value)
                except ValueError:
                    pass
            if cl is None or cl < 0:
                raise ValueError(
                    'bad bytes in content-length: {!r}'.format(value)
                )
            if cl > 9007199254740992:
                raise ValueError(
                    'content-length value too large: {!r}'.format(cl)
                )
            key = 'content-length'
            value = cl
        elif key.lower() == b'transfer-encoding':
            if value != b'chunked':
                raise ValueError(
                    'bad transfer-encoding: {!r}'.format(value)
                )
            key = 'transfer-encoding'
            value = 'chunked'
        else:
            key = _decode_key(key, 'bad bytes in header name: {!r}')
            value = _decode_value(value, 'bad bytes in header value: {!r}')
        if headers.setdefault(key, value) is not value:
            raise ValueError(
                'duplicate header: {!r}'.format(line)
            )
    if _READLINE(readline, 2) != b'\r\n':
        raise ValueError('too many headers (> {})'.format(_MAX_HEADER_COUNT))
    return headers


def __read_preamble(rfile):
    readline = rfile.readline
    if not callable(readline):
        raise TypeError('rfile.readline is not callable')
    line = _READLINE(readline, _MAX_LINE_SIZE)
    if not line:
        raise EmptyPreambleError('HTTP preamble is empty')
    if line[-2:] != b'\r\n':
        raise ValueError('bad line termination: {!r}'.format(line[-2:]))
    if len(line) == 2:
        raise ValueError('first preamble line is empty')
    first_line = _decode_value(line[:-2], 'bad bytes in first line: {!r}')
    headers = __read_headers(readline)
    return (first_line, headers)


def _read_preamble(rfile):
    (first_line, headers) = __read_preamble(rfile)
    if 'content-length' in headers and 'transfer-encoding' in headers:
        raise ValueError(
            'cannot have both content-length and transfer-encoding headers'
        )
    return (first_line, headers)


def _read_response_preamble(rfile):
    readline = rfile.readline
    if not callable(readline):
        raise TypeError('rfile.readline is not callable')
    line = _READLINE(readline, _MAX_LINE_SIZE)
    if not line:
        raise EmptyPreambleError('HTTP preamble is empty')
    if line[-2:] != b'\r\n':
        raise ValueError('bad line termination: {!r}'.format(line[-2:]))
    if len(line) == 2:
        raise ValueError('first preamble line is empty')
    (status, reason) = parse_response_line(line[:-2])
    headers = __read_headers(readline)
    if 'content-length' in headers and 'transfer-encoding' in headers:
        raise ValueError(
            'cannot have both content-length and transfer-encoding headers'
        )
    return (status, reason, headers)


def _read_request_preamble(rfile):
    readline = rfile.readline
    if not callable(readline):
        raise TypeError('rfile.readline is not callable')
    line = _READLINE(readline, _MAX_LINE_SIZE)
    if not line:
        raise EmptyPreambleError('HTTP preamble is empty')
    if line[-2:] != b'\r\n':
        raise ValueError('bad line termination: {!r}'.format(line[-2:]))
    if len(line) == 2:
        raise ValueError('first preamble line is empty')
    (method, uri) = parse_request_line(line[:-2])
    headers = __read_headers(readline)
    if 'content-length' in headers and 'transfer-encoding' in headers:
        raise ValueError(
            'cannot have both content-length and transfer-encoding headers'
        )
    return (method, uri, headers)


class Reader:
    def __init__(self, raw):
        self.raw = raw
        self._buf = bytearray(MAX_PREAMBLE_BYTES)
        self._view = memoryview(self._buf)
        self._tell = 0
        self._size = 0

    def tell(self):
        assert isinstance(self._tell, int) and self._tell >= 0
        return self._tell

    def _consume_buffer(self, size):
        """
        Consume first *size* bytes in buffer.
        """
        assert 0 <= size <= self._size <= MAX_PREAMBLE_BYTES
        ret = self._view[:size].tobytes()
        self._tell += size
        remaining = self._size - size
        self._view[:remaining] = self._view[size:size+remaining]
        self._size = remaining
        return ret

    def _fill_buffer(self):
        assert 0 <= self._size <= len(self._buf)
        added = self.raw.readinto(self._view[self._size:])
        self._size += added
        return added

    def read_preamble(self):
        self._fill_buffer()
        index = self.buf.find(b'\r\n\r\n')
        if 0 < index < self.stop:
            pass


def format_request_preamble(method, uri, headers):
    lines = ['{} {} HTTP/1.1\r\n'.format(method, uri)]
    if headers:
        header_lines = ['{}: {}\r\n'.format(*kv) for kv in headers.items()]
        header_lines.sort()
        lines.extend(header_lines)
    lines.append('\r\n')
    return ''.join(lines).encode()


def format_response_preamble(status, reason, headers):
    lines = ['HTTP/1.1 {} {}\r\n'.format(status, reason)]
    if headers:
        header_lines = ['{}: {}\r\n'.format(*kv) for kv in headers.items()]
        header_lines.sort()
        lines.extend(header_lines)
    lines.append('\r\n')
    return ''.join(lines).encode()

