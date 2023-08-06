REST Gateway Interface
======================

The *REST Gateway Interface* (RGI) is a thought experiment in what you could do
with something like `WSGI`_ assuming you didn't need `CGI`_ compatibility, and
likewise didn't necessarily need to be compatible with any existing HTTP
servers.

Note that this design is done with deep respect for, and takes untold
inspiration from, the `WSGI`_ standard.  Considering the delicate balance needed
for backward compatibility on multiple fronts, WSGI is an *exceedingly* good
design.

RGI aims to be a worthy interpretation of what WSGI *might* be were it done
today without concern for backward compatibility, and with a rather narrow focus
on REST APIs in particular.


Big picture
-----------

As `WSGI`_ is a refined and well understood specification, it's helpful to
introduce RGI by comparing and contrasting it with WSGI.

WSGI applications are callable objects that accept two arguments when handling
a request, for example:

>>> def tiny_wsgi_app(environ, start_response):
...     start_response('200 OK', [('Content-Length', '12')])
...     return [b'hello, world']
...

The *enivron* argument will be a ``dict`` instance something like this::

    environ = {
        'wsgi.version': (1, 0),
        'wsgi.url_scheme': 'http',
        'SERVER_PROTOCOL': 'HTTP/1.1',
        'SERVER_NAME': '192.168.1.2',
        'SERVER_PORT': '2345',
        'REMOTE_ADDR': '192.168.1.3',
        'REMOTE_PORT': '3456',
        'REQUEST_METHOD': 'PUT',
        'SCRIPT_NAME': '/foo',
        'PATH_INFO': '/bar/baz',
        'QUERY_STRING': 'stuff=junk',
        'CONTENT_TYPE': 'application/json',
        'CONTENT_LENGTH': '1776',
        'HTTP_ACCEPT': 'application/json',
        'wsgi.input': <file-like request body>,
        'wsgi.file_wrapper': <file-like wrapper class>,
    }

The WSGI *environ* contains information from three distinct domains:

    1. Server-wide information that will be the same throughout the server
       process lifetime (for example, the server IP and port)

    2. Per-connection information that will be the same throughout all HTTP
       requests handled by a specific TCP connection (for example, the client IP
       and port)

    3. Per-request information used only for the single HTTP request being
       handled (for example, the HTTP request method and request headers)

For each request, the WSGI application will be called with a unique *environ*
instance used only for that request, which is (generally) built by copying the
server-wide information, adding in the per-connection information, and finally
adding in the per-request information.

The *start_response* argument is callable object accepting two arguments::

    start_response(status, headers)

WSGI applications convey their response status and response headers by calling
``start_response()``, and then separately convey their response body via their
return value.  (Or optionally applications convey their response body by making
successive calls to a ``write()`` method returned by ``start_response()``.)

Although an elegant solution considering the broad backward compatibility
requirements of WSGI, ``start_response()`` is the most problematic aspect of the
design as it adds considerable complexity to the response flow control.

In contrast, RGI applications convey their entire response via a 4-tuple return
value::

    (status, reason, headers, body)

RGI applications are called with three arguments when handling a request:

>>> def tiny_rgi_app(session, request, bodies):
...     return (200, 'OK', {'content-length': 12}, b'hello, world')
...

The *session* is a ``dict`` containing server-wide(1) and per-connection(2)
information.

The *request* is a ``dict`` containing only per-request(3) information.

Finally, the *bodies* argument is a ``namedtuple`` exposing four wrapper classes
that RGI applications can use when building their HTTP response body:

    ==========================  ==================================
    Exposed via                 Degu implementation
    ==========================  ==================================
    ``bodies.Body``             :class:`degu.base.Body`
    ``bodies.BodyIter``         :class:`degu.base.BodyIter`
    ``bodies.ChunkedBody``      :class:`degu.base.ChunkedBody`
    ``bodies.ChunkedBodyIter``  :class:`degu.base.ChunkedBodyIter`
    ==========================  ==================================

Combined, the RGI *session*, *request*, and *bodies* arguments contain the same
information as the WSGI *environ* argument.

There is a simple one-to-one mapping from WSGI to RGI in this respect.  For
example, this WSGI *environ*.

Would translate into this RGI *session* and *request*::

    session = {
        'rgi.version': (0, 1),
        'scheme': 'http',
        'protocol': 'HTTP/1.1',
        'server': ('192.168.1.2', 2345)
        'client': ('192.168.1.3', 3456),
    }

    request = {
        'method': 'PUT',
        'script': ['foo'],
        'path': ['bar', 'baz'],
        'query': 'stuff=junk',
        'headers': {
            'content-type': 'application/json',
            'content-length': 1776,
            'accept': 'application/json',
        },
        'body': <file-like request body>,
    }

.. note::

    ``bodies.Body`` is the equivalent of ``environ['wsgi.file_wrapper']``

A *session* instance is created for each new connection, and then RGI
applications are called with this exact same *session* instance for each request
made throughout the lifetime of the connection.

As such, RGI applications can use the *session* to store per-connection
resources that will persist from one request to the next.  For example, an RGI
reverse-proxy application could use this to lazily create its upstream HTTP
client connection, and then reuse it on subsequent requests.

However, as expected, RGI applications are called with a unique *request*
instance for each request.

In addition to the traditional request handler, RGI also allows applications to
specify a connection handler that will be called after a new connection is
received, but before any requests are handled.  The connection handler can store
application-specific information in the *session*, which will then be available
to the request handler for each request handled during the lifetime of the
connection.

In particular, the connection handler is aimed at allowing RGI applications to
do application-specific extended per-connection authentication when using SSL
with client certificates.

RGI applications specify the connection handler via a callable
``app.on_connect()`` attribute, for example:

>>> class TinyRGIApp:
...     def __call__(self, session, request, bodies):
...         if '__hello' not in session:
...             session['__hello'] = b'hello, world'
...         body = session['__hello']
...         return (200, 'OK', {'content-length': len(body)}, body)
...
...     def on_connect(self, session, sock):
...         session['_user'] = '<special per-connection authentication result>'
...         return True
... 

(Note that storing ``b'hello, world'`` in ``session['__body']`` is just a silly
example to illustrate the API, not something you'd want to do in real-life.) 

To further compare and contrast, this more realistically complex WSGI
application:

>>> def wsgi_app(environ, start_response):
...     if environ['REQUEST_METHOD'] not in {'GET', 'HEAD'}:
...         start_response('405 Method Not Allowed', [])
...         return []
...     body = b'hello, world'
...     headers = [
...         ('Content-Length', str(len(body))),
...         ('Content-Type', 'text/plain'),
...     ]
...     start_response('200 OK', headers)
...     if environ['REQUEST_METHOD'] == 'GET':
...         return [body]
...     return []  # No response body for HEAD
... 

Would translate into this RGI application:

>>> def rgi_app(session, request, bodies):
...     if request['method'] not in {'GET', 'HEAD'}:
...         return (405, 'Method Not Allowed', {}, None)
...     body = b'hello, world'
...     headers = {
...         'content-length': len(body),
...         'content-type': 'text/plain',
...     }
...     if request['method'] == 'GET':
...         return (200, 'OK', headers, body)
...     return (200, 'OK', headers, None)  # No response body for HEAD
... 



Handling requests
-----------------

RGI applications take two arguments when handling requests: a *session* and a
*request*.

Both are ``dict`` instances that together provide the equivalent of the WSGI
*environ* argument (note that there is no RGI equivalent of the WSGI
``start_response()`` callable).

The difference is that the *session* argument contains only per-connection
information, and the *request* argument contains only per-request information. 
Additionally, applications can use the *session* argument to store persistent
per-connection state (for example, a lazily created database connection or a
connection to an upstream HTTP server in the case of a `reverse-proxy`_
application).

As noted above, the *session* argument will look something like this::

    session = {
        'scheme': 'https',
        'protocol': 'HTTP/1.1',
        'server': ('0.0.0.0', 2345),
        'client': ('192.168.0.3', 3456),
        'ssl_compression': None,
        'ssl_cipher': ('ECDHE-RSA-AES256-GCM-SHA384', 'TLSv1/SSLv3', 256),
    }

When needed, the RGI request-handler can add additional information to the
*session* ``dict``, and this same connection ``dict`` instance will be
persistent throughout all request handled during the connection's lifetime.

In order to avoid conflicts with additional *session* information that may be
added by future RGI servers, and to avoid conflicts with information added by a
possible ``on_connect()`` handler, there is a simple, pythonic name-spacing
rule: the request handler should only add keys that start with ``'__'`` (double
underscore).

On the other hand, the *request* argument will look something like this::

    request = {
        'method': 'POST',
        'script': ['foo'],
        'path': ['bar', 'baz'],
        'query': 'stuff=junk',
        'headers': {
            'accept': 'application/json',
            'content-length': 1776,
            'content-type': 'application/json',
        },
        'body': <file-like request body>,
    }

As RGI does not aim for CGI compatibility, it uses shorter, lowercase keys,
(eg, ``'method'`` instead of ``'REQUEST_METHOD'``).  Note that the ``'script'``
and ``'path'`` values are lists rather than strings.  This avoids complicated
(and error prone) re-parsing to shift the path, or to otherwise interpret the
path.

Importantly, the request headers are in a sub-dictionary.  The request header
names (keys) will have been case-folded (lowercased) by the server, regardless
of the case used in the client request.  If the request headers include a
``'content-length'``, its value will have been validated and converted into an
``int`` by the server.

The ``request['headers']`` sub-dictionary was designed to be directly usable by
a reverse-proxy application when making its HTTP client request.  For example,
we can implement a simple reverse-proxy with the help of the the
:func:`degu.util.relative_uri()` functions:

>>> from degu.util import relative_uri
>>> class ReverseProxyApp:
...     def __init__(self, client):
...         self.client = client
... 
...     def __call__(self, session, request, bodies):
...         if '__conn' not in session:
...             session['__conn'] = self.client.connect()
...         conn = session['__conn']
...         return conn.request(
...             request['method'],
...             relative_uri(request),
...             request['headers'],
...             request['body']
...         )
...

An RGI application must return a ``(status, reason, headers, body)`` response
tuple, for example::

    response = (200, 'OK', {'content-length': 12}, b'hello, world')

RGI doesn't use anything like the WSGI ``start_response()`` callable.  Instead,
applications and middleware convey the HTTP response in total via a single
return value (the above response tuple).

This allows middleware to easily inspect (or even modify) any aspect of the
request or response all within a single call to their ``__call__()`` method.
This design also makes it easier to unit test applications, middleware, and even
servers.

Note that the HTTP *status* code is returned as an integer, and the *reason* is
returned as a separate string value (whereas in WSGI, both are provided together
via a single *status* string).  A general design theme in RGI is that values
should be kept in their most useful and native form for as long as possible, so
that re-parsing isn't needed.  For example, the server might want to verify that
a ``'content-range'`` header is present when the *status* is ``206`` (Partial
Content).

Also note that the response headers are a dictionary instead of a WSGI-style
list of pairs.  The response header names must be casefolded with
``str.casefold()``, and the ``'content-length'``, if present, must be a
non-negative ``int``.



Handling connections
--------------------

If an RGI application has a callable ``on_connect`` attribute, it will be
passed two arguments when handling connections: a *session* and a *sock*.

The *session* will be a ``dict`` containing the per-connection environment
already created by the server, which will be a subset of the equivalent
information in the WSGI *environ*.  Importantly, ``on_connect()`` is called
before any requests have been handled, and the *session* argument will not
contain any request related information.

The *session* argument will look something like this::

    session = {
        'scheme': 'https',
        'protocol': 'HTTP/1.1',
        'server': ('0.0.0.0', 2345),
        'client': ('192.168.0.3', 3456),
        'ssl_compression': None,
        'ssl_cipher': ('ECDHE-RSA-AES256-GCM-SHA384', 'TLSv1/SSLv3', 256),
    }

The *sock* will be either a ``socket.socket`` instance or an ``ssl.SSLSocket``
instance.

When needed, the ``on_connect()`` connection-handler can add additional
information to the *session* ``dict``, and this same *session* ``dict``
instance will be passed to the main ``application.__call__()`` method when
handling each request within the lifetime of that connection.

This was motivated by the somewhat specialized way in which `Dmedia`_ uses SSL,
where *authentication* is done per-connection, and only *authorization* is done
per-request.  This allows Dmedia to do extended per-connection authentication,
in particular to verify the intrinsic machine and user identities behind the
connection, based on the SSL certificate and SSL certificate authority under
which the connection was made, respectively.

In order to avoid conflicts with additional *session* information that may be
added by future RGI servers, there is a simple, pythonic name-spacing rule: the
``on_connect()`` callable should only add keys that start with ``'_'``
(underscore).

For example:

>>> import ssl
>>> class MyApp:
...     def __call__(self, session, request, bodies):
...         return (200, 'OK', {'content-length': 12}, b'hello, world')
... 
...     def on_connect(self, session, sock):
...         if not isinstance(sock, ssl.SSLSocket):  # Require SSL 
...             return False
...         session['_user'] = '<User public key hash>'
...         session['_machine'] = '<Machine public key hash>'
...         return True
...



Chunked encoding
----------------

RGI fully exposes the semantics of HTTP `chunked transfer encoding`_ to server
applications, including use of the optional per-chunk extension.

This gives RGI applications full access to chunk-encoding semantics in the
incoming request body, and also gives RGI applications full control over
chunk-encoding semantics in their outgoing response body.

RGI represents a single chunk with a ``(extension, data)`` tuple.  When no
extension is present for that chunk, the *extension* will be ``None``::

    (b'hello', None)

Which would be encoded like this in the HTTP request or response stream::

    b'5\r\nhello\r\n'

Or when an extension is present, *extension* will be a ``(key, value)`` tuple::

    (b'hello', ('foo', 'bar'))

Which would be encoded like this in the HTTP request or response stream::

    b'5;foo=bar\r\nhello\r\n'

RGI doesn't treat chunked-transfer encoding as merely an alternate way of
transferring the same content, but instead as a wholly different mechanism with
specific meaning that must be exposed and preserved.

The exact data boundaries of each chunk is meaningful, and the optional chunk
extension must be associated with only the data in that chunk.

This is extremely useful for `CouchDB`_ style continuous structured data
replication.  For example, each chunk *data* might be a fully self-contained
JSON encoded object, and the chunk *extension* could be used for conveying
global database state at the event corresponding to that chunk.



Request body
------------

RGI is unambiguous about the nature of the incoming HTTP request body,
specifically about three conditions:

    1. When there is no request body

    2. When the request body has a content-length

    3. When the request body is chunk-encoded

When there is no request body, ``request['body']`` will be ``None``.

Otherwise applications can test the ``request['body'].chunked`` attribute, which
will be ``True`` when the request body is chunk-encoded, and will be ``False``
when the request body has a content-length.

The ``chunked`` attribute allows applications to easily determine whether the
body is chunk-encoded, even in lower level code that may not have access to the
request headers.

For example, an RGI application that handles POST requests might look something
like this:

>>> def rgi_post_app(session, request, bodies):
...     if request['method'] != 'POST':
...         return (405, 'Method Not Allowed', {}, None)
...     if request['body'] is None:
...         return (400, 'Bad Request', {}, None)
...     if request['body'].chunked:
...         for (extension, data) in request['body']:
...             pass  # Do something useful
...     else:
...         for data in request['body']:
...             pass  # Do something useful
...     return (200, 'OK', {}, None)

When the request body has a content-length, ``request['body']`` will be an
instance of the ``bodies.Body`` class.

When the request body is chunk-encoded, ``request['body']`` will be an instance
of the ``bodies.ChunkedBody`` class.

Details of the standard API for these RGI request body objects is still being
finalized, so for now, please see the reference implementations in Degu:

    * :class:`degu.base.Body`

    * :class:`degu.base.ChunkedBody`



Response body
-------------  

Similar to the request body, RGI allows applications to unambiguously
communicate the nature of their outgoing response body, specifically about three
conditions:

    1. When there is no response body

    2. When the response body has a content-length

    3. When the response body is chunk-encoded

Very much in the spirit of the WSGI ``environ['wsgi.file_wrapper']``, there are
four specialized wrapper classes exposed in the RGI *bodies* argument:

    ==========================  =====================================
    Exposed via                 Degu reference implementation
    ==========================  =====================================
    ``bodies.Body``             :class:`degu.base.Body`
    ``bodies.BodyIter``         :class:`degu.base.BodyIter`
    ``bodies.ChunkedBody``      :class:`degu.base.ChunkedBody`
    ``bodies.ChunkedBodyIter``  :class:`degu.base.ChunkedBodyIter`
    ==========================  =====================================

Although four distinct wrapper classes might seem excessive, granularity here
eliminates ambiguity and needless magic elsewhere.

When reading this section, keep in mind the 4-tuple response returned by RGI
applications::

    (status, reason, headers, body)

Because of this single, comprehensive response return value, RGI has a much
simpler response flow control compared to WSGI.

Yet the ``bodies.BodyIter`` and ``bodies.ChunkedBodyIter`` classes allow RGI to
maintain an important and elegant WSGI feature: the ability of the response body
to be an arbitrary iterable that yields the response body one piece at a time,
as generated on-the-fly by the application.


**1. No response body:**

To indicate no response body, RGI applications should return ``None`` for the
*body* in their response 4-tuple.

When responding to a HEAD request, RGI applications should included a
``'content-length'`` or a ``{'transfer-encoding': 'chunked'}`` response header
(but not both).

For all other request methods, when there is no response body, RGI applications
should include neither a ``'content-length'`` nor a ``'transfer-encoding'``
response header.

The response body of ``None`` addresses a subtle ambiguity in WSGI: the ability
to express *no* response body vs merely an *empty* response body (which implies
that the server should set a ``{'content-length': 0}`` response header if not
already present).


**2. Response body with content-length:**

There are four types that can be used to indicate a response body with a
content-length:

    1. A native Python3 ``bytes`` instance

    2. A native Python3 ``bytearray`` instance

    3. A ``bodies.Body`` instance (:class:`degu.base.Body`)

    4. A ``bodies.BodyIter`` instance (:class:`degu.base.BodyIter`)

When the response body is understood as having a content-length, RGI
applications can never include a ``'transfer-encoding'`` in their response
headers.  Likewise, if applications include a ``'content-length'`` in their
response headers, it must match the specific (or claimed) length of their
response body.  Otherwise the ``'content-length'`` header will be set by the
RGI server based on the specific (or claimed) length of the returned response
body.

``bytes`` and ``bytearray`` instances give RGI applications a simple, performant
way of returning a response body that is relatively small and easily built all
at once.  Arguably, most responses from typical server applications fit this
niche.

Not to mention that ``bytes`` in particular are the most illustrative, which
helps RGI be an inviting specification.  For example:

>>> def rgi_hello_world_app(session, request, bodies):
...     return (200, 'OK', {'content-type': 'text/plain'}, b'hello, world')
... 

The ``bodies.Body`` class (:class:`degu.base.Body`) is used to provide
HTTP content-length based framing atop an arbitrary file-like object with a
``read()`` method that accepts a *size* argument and returns ``bytes``.

For example, you would use a ``bodies.Body`` instance to return a response body
read from a regular file:

>>> def rgi_file_app(session, request, bodies):
...     fp = open('/ultimate/answer', 'rb')
...     body = bodies.Body(fp, 42)
...     return (200, 'OK', {'content-length': 42}, body)
... 

(Note that for clarity, the above RGI application redundantly specifies the
response ``'content-length'``.)

You can likewise use ``bodies.Body`` to frame an *rfile* returned by
`socket.socket.makefile()`_, which is especially useful for RGI reverse-proxy
applications.

On the other hand, the ``bodies.BodyIter`` class (:class:`degu.base.BodyIter`)
is used to wrap an arbitrary iterable that yields the response body one piece at
a time as generated by the application, yet sill with an explicit agreement as
to the ultimate content-length.

For example:

>>> def generate_body():
...     yield b'hello'
...     yield b', world'
... 
>>> def rgi_generator_app(session, request, bodies):
...     body = bodies.BodyIter(generate_body(), 12)
...     return (200, 'OK', {'content-length': 12}, body)
... 

(Note that for clarity, the above RGI application redundantly specifies the
response ``'content-length'``.)


**3. Chunk-encoded response body:**

There are two types that can be used to indicate a chunked-encoded response
body:

    1. A ``session['ChunkedBody']`` instance (:class:`degu.base.ChunkedBody`)

    2. A ``session['ChunkedBodyIter']`` instance
       (:class:`degu.base.ChunkedBodyIter`)

When the response body is understood as being chunk-encoded, RGI applications
can never include a ``'content-length'`` in their response headers.  Likewise,
if applications include a ``'transfer-encoding'`` in their response headers,
its value must be ``'chunked'``.  Otherwise a
``{'transfer-encoding': 'chunked'}`` header will be set by the RGI server.

The ``bodies.ChunkedBody`` class (:class:`degu.base.ChunkedBody`) is used to
provide HTTP chunked-encoding based framing atop an arbitrary file-like object
with ``readline()`` and ``read()`` methods that accept a *size* argument and
return ``bytes``.

This is especially useful for RGI reverse-proxy applications that want to frame
a chunk-encoded HTTP client response from an *rfile* returned by
`socket.socket.makefile()`_.

But you can likewise use ``bodies.ChunkedBody`` to frame a regular file that
happens to be chunk-encoded, for example:

>>> def rgi_chunked_file_app(session, request, bodies):
...     fp = open('/chunky/delight', 'rb')
...     body = bodies.ChunkedBody(fp)
...     return (200, 'OK', {'transfer-encoding': 'chunked'}, body)
...

(Note that for clarity, the above RGI application redundantly specifies the
response ``'transfer-encoding'``.) 

It's important to understand that ``bodies.ChunkedBody`` expects the content
read from the provided *rfile* to itself be properly HTTP chunk-encoded.  It
will stop yielding ``(extension, data)`` items after the first chunk with an
empty data ``b''`` is encountered.  The *rfile* must always contain at least one
empty chunk.

On the other hand, the ``bodies.ChunkedBodyIter`` class
(:class:`degu.base.ChunkedBodyIter`) is used to wrap an arbitrary iterable that
yields the response body as a series of ``(extension, data)`` tuples for each
chunk in the response.

The *source* iterable must always produce at least one item, and the last (and
only the last) item must have have empty ``b''`` *data*.

For example:

>>> def generate_chunked_body():
...     yield (b'hello', ('key1', 'value1'))
...     yield (b', world', ('key2', 'value2'))
...     yield (b'', ('key3', 'value3'))
... 
>>> def rgi_chunked_generator_app(session, request, bodies):
...     body = bodies.ChunkedBodyIter(generate_chunked_body())
...     return (200, 'OK', {'transfer-encoding': 'chunked'}, body)
... 

(Note that for clarity, the above RGI application redundantly specifies the
response ``'transfer-encoding'``.)



Examples
--------

A few more examples will help make this all clearer, and should especially help
make it clear why RGI is very middleware-friendly (and proxy-friendly) compared
to WSGI.

For example, consider this simple RGI application:

>>> def demo_app(session, request, bodies):
...     if request['method'] not in ('GET', 'HEAD'):
...         return (405, 'Method Not Allowed', {}, None)
...     body = b'hello, world'
...     headers = {'content-length': len(body)}
...     return (200, 'OK', headers, body)
...

Here's what ``demo_app()`` returns for a suitable GET request:

>>> demo_app({}, {'method': 'GET', 'path': []}, None)
(200, 'OK', {'content-length': 12}, b'hello, world')

However, note that ``demo_app()`` isn't actually HTTP/1.1 compliant as it should
not return a response body for a HEAD request:

>>> demo_app({}, {'method': 'HEAD', 'path': []}, None)
(200, 'OK', {'content-length': 12}, b'hello, world')

Now consider this example middleware that checks for just such a faulty
application and overrides its response:

>>> class Middleware:
...     def __init__(self, app):
...         self.app = app
...
...     def __call__(self, session, request, bodies):
...         (status, reason, headers, body) = self.app(session, request, bodies)
...         if request['method'] == 'HEAD' and body is not None:
...             return (500, 'Internal Server Error', {}, None)
...         return (status, reason, headers, body)
...

``Middleware`` will let the response to a GET request pass through unchanged: 

>>> middleware = Middleware(demo_app)
>>> middleware({}, {'method': 'GET', 'path': []}, None)
(200, 'OK', {'content-length': 12}, b'hello, world')

But ``Middleware`` will intercept the faulty response to a HEAD request:

>>> middleware({}, {'method': 'HEAD', 'path': []}, None)
(500, 'Internal Server Error', {}, None)



WSGI to RGI
-----------

Here's a table of common `WSGI`_ to RGI equivalents when handling requests:

================================  ========================================
WSGI                              RGI
================================  ========================================
``environ['wsgi.file_wrapper']``  ``bodies.Body``
``environ['wsgi.version']``       ``session['rgi.version']``
``environ['wsgi.url_scheme']``    ``session['scheme']``
``environ['SERVER_PROTOCOL']``    ``session['protocol']``
``environ['SERVER_NAME']``        ``session['server'][0]``
``environ['SERVER_PORT']``        ``session['server'][1]``
``environ['REMOTE_ADDR']``        ``session['client'][0]``
``environ['REMOTE_PORT']``        ``session['client'][1]``
``environ['REQUEST_METHOD']``     ``request['method']``
``environ['SCRIPT_NAME']``        ``request['script']``
``environ['PATH_INFO']``          ``request['path']``
``environ['QUERY_STRING']``       ``request['query']``
``environ['CONTENT_TYPE']``       ``request['headers']['content-type']``
``environ['CONTENT_LENGTH']``     ``request['headers']['content-length']``
``environ['HTTP_FOO']``           ``request['headers']['foo']``
``environ['HTTP_BAR_BAZ']``       ``request['headers']['bar-baz']``
``environ['wsgi.input']``         ``request['body']``
================================  ========================================

Note that the above RGI equivalents for these *environ* variables:

    * ``environ['SERVER_NAME']``
    * ``environ['SERVER_PORT']``
    * ``environ['REMOTE_ADDR']``
    * ``environ['REMOTE_PORT']``

...will *only* be true when the socket family is ``AF_INET`` or ``AF_INET6``,
but will *not* be true when the socket family is ``AF_UNIX``.

An important distinction in the RGI specification, and in Degu as an
implementation, is that they directly expose (and use) the *address* from the
underlying Python3 `socket API`_.


.. _`WSGI`: http://www.python.org/dev/peps/pep-3333/
.. _`CGI`: http://en.wikipedia.org/wiki/Common_Gateway_Interface
.. _`reverse-proxy`: https://en.wikipedia.org/wiki/Reverse_proxy
.. _`Dmedia`: https://launchpad.net/dmedia
.. _`socket API`: https://docs.python.org/3/library/socket.html
.. _`chunked transfer encoding`: https://en.wikipedia.org/wiki/Chunked_transfer_encoding
.. _`CouchDB`: http://couchdb.apache.org/
.. _`socket.socket.makefile()`: https://docs.python.org/3/library/socket.html#socket.socket.makefile
