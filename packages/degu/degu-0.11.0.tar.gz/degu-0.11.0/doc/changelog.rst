Changelog
=========

0.11 (November)
---------------

`Download Degu 0.11`_

Degu is now *tentatively* API-stable.

Although no further backward incompatible changes are currently expected on the
way to the 1.0 release, it seems prudent to allow another release or two for
feedback and refinement, and for potential breaking API changes if deemed
absolutely essential.

If you were waiting for the API-stable release to experiment with Degu, now is
definitely the time to jump in, as `your feedback`_ can help better tune Degu
for your use-case.

It's quite possible that there will be no breaking API changes whatsoever
between Degu 0.11 and Degu 1.0, but even if there are, and even if those
breaking changes happen to effect your application, they will be subtle changes
that require only minimal porting effort.

Breaking API changes:

    *   Flip order of items in a single chunk (in an HTTP body using chunked
        transfer-encoding) from::

            (data, extension)

        To::

            (extension, data)

        This was the one place where the Degu API wasn't faithful to the order
        in the HTTP wire format (the chunk *extension*, when present, is
        contained in the chunk size line, prior to the actual chunk *data*).

        As before, the *extension* will be ``None`` when there is no extension
        for a specific chunk::

            (None, b'hello, world')

        And the *extension* will be a ``(key, value)`` tuple when a specific
        chunk does contain an optional per-chunk extension::

            (('foo', 'bar'), b'hello, world')

    *   Change :func:`degu.base.write_chunk()` signature from::

            write_chunk(wfile, data, extension=None)

        To::

            write_chunk(wfile, chunk)

        Where the *chunk* is an ``(extension, data)`` tuple.  This harmonizes
        with the above change, and also means that you can treat the *chunk* as
        an opaque data structure when passing it between
        :func:`degu.base.read_chunk()` and :func:`degu.base.write_chunk()`, for
        example::

            chunk = read_chunk(rfile)
            write_chunk(wfile, chunk)

    *   :meth:`degu.base.Body.read()` will now raise a ``ValueError`` if the
        resulting read would exceed :attr:`degu.base.MAX_READ_SIZE` (currently
        16 MiB); this is to prevent unbounded resource usage when no *size* is
        provided, a common pattern when a relatively small input body is
        expected, for example::

            doc = json.loads(body.read().decode())

    *   :meth:`degu.base.ChunkedBody.read()` will likewise now raise a
        ``ValueError`` when the accumulated size of chunks read thus far exceeds
        :attr:`degu.base.MAX_READ_SIZE`; this is to prevent unbounded resource
        usage for the same pattern above, which is especially important as the
        total size of a chunk-encoded input body can't be determined in advance.

        Note that in the near future :meth:`degu.base.ChunkedBody.read()` will
        accept an optional *size* argument, which can be done without breaking
        backward compatibility.  Once this happens, it will exactly match the
        semantics of of :meth:`degu.base.Body.read()`, and will meet standard
        Python file-like API exceptions.

    *   :meth:`degu.base.ChunkedBody.read()` now returns a ``bytes`` instance
        instead of a ``bytearray``, to match standard Python file-like API
        expectations.

    *   Fix ambiguity in RGI ``request['query']`` so that it can represent the
        difference between "no query" vs merely an "empty query".

        When there is *no* query, ``request['query']`` will now be ``None``
        (whereas previously it would be ``''``).  For example::

            request = {
                'method': 'GET',
                'uri': '/foo/bar',
                'script': [],
                'path': ['foo', 'bar'],
                'query': None,
                'body': None,
            }

        As before, an *empty* query is still represented via an empty ``str``::

            request = {
                'method': 'GET',
                'uri': '/foo/bar?',
                'script': [],
                'path': ['foo', 'bar'],
                'query': '',
                'body': None,
            }

        This change means it's now possible to exactly reconstructed the
        original URI from the ``request['script']``, ``request['path']``, and
        ``request['query']`` components.

    *   :func:`degu.util.relative_uri()` and :func:`degu.util.absolute_uri()`
        now preserve the difference between *no* query vs merely an *empty*
        query, can always reconstruct a lossless relative URI, or a lossless
        absolute URI, respectively.

    *   :meth:`degu.rgi.Validator.__call__()` now requires that
        ``request['uri']`` be present and be a ``str`` instance; it also
        enforces an invariant condition between ``request['script']``,
        ``request['path']``, and ``request['query']`` on the one hand, and
        ``request['uri']`` on the other::

            _reconstruct_uri(request) == request['uri']

        This invariant condition is initially checked to ensure that the RGI
        server correctly parsed the URI and that any path shifting was done
        correctly by (possible) upstream middleware; then this invariant
        condition is again checked after calling the downstream ``app()``
        request handler, to make sure that any path shifting was done correctly
        by (possible) downstream middleware.

    *   Demote ``read_preamble()`` function in :mod:`degu.base` to internal,
        private use API, as it isn't expected to be part of the eventual public
        parsing API (it will be replaced by some other equivalent once the C
        backend is complete).

    *   :class:`degu.client.Client` no longer accepts the *Connection* keyword
        option, no longer has the ``Client.Connection`` attribute; the idea
        behind the *Connection* option was so that high-level, domain-specific
        APIs could be implemented via a :class:`degu.client.Connection`
        subclass, but subclassing severely limits composability; in contrast,
        the new approach is inspired by the `io`_ module in the Python standard
        library (see :ref:`high-level-client-API` for details).


Other changes:

    *   Clarify and document the preferred approach for implementing high-level,
        domain-specific wrappers atop the Degu client API; see
        :ref:`high-level-client-API` for details.

    *   :class:`degu.client.Connection` now has shortcuts for the five supported
        HTTP request methods:

            *   :meth:`degu.client.Connection.put()`
            *   :meth:`degu.client.Connection.post()`
            *   :meth:`degu.client.Connection.get()`
            *   :meth:`degu.client.Connection.head()`
            *   :meth:`degu.client.Connection.delete()`

        Previously these were avoided to prevent confusion with specialized
        methods of the same name that would likely be added in
        :class:`degu.client.Connection` subclasses, as sub-classing was the
        expected way to implement high-level, domain-specific APIs; however, the
        new wrapper class approach for high-level APIs is much cleaner, and it
        eliminates confusion about which implementation of a method you're
        getting (because unlike a subclass, a wrapper wont inherit anything from
        :class:`degu.client.Connection`); as such, there's no reason to avoid
        these shortcuts any longer, plus they make the
        :class:`degu.client.Connection` API more inviting to use directly, so
        there's no reason to use a higher-level wrapper just for the sake of
        this same brevity.

        Note that the generic :meth:`degu.client.Connection.request()` method
        remains unchanged, and should still be used whenever you need to specify
        an arbitrary HTTP request via arguments alone (for example, when
        implementing a reverse-proxy).

    *   :class:`degu.client.Connection` now internally uses the provided
        *bodies* API rather than directly importing the default wrapper classes
        from :mod:`degu.base`; this means the standard client and bodies APIs
        are now fully compossible, so you can use the Degu client with other
        implementations of the bodies API (for example, when using the Degu
        client in a reverse-proxy running on some other RGI compatible server).

        To maintain this composability when constructing HTTP request bodies,
        you should use the wrappers exposed via
        :attr:`degu.client.Connection.bodies` (rather than directly importing
        the same from :mod:`degu.base`).  For example:

        >>> from degu.client import Client
        >>> client = Client(('127.0.0.1', 56789))
        >>> conn = client.connect()  #doctest: +SKIP
        >>> fp = open('/my/file', 'rb')  #doctest: +SKIP
        >>> body = conn.bodies.Body(fp, 76)  #doctest: +SKIP
        >>> response = conn.request('POST', '/foo', {}, body)  #doctest: +SKIP

    *   :class:`degu.server.Server` now internally uses the provided *bodies*
        API rather than directly importing the default wrapper classes from
        :mod:`degu.base`; this means the standard server and bodies APIs are
        now fully compossible, so you can use the Degu server with other
        implementations of the bodies API.

    *   :meth:`degu.server.Server.serve_forever()` now uses a
        `BoundedSemaphore`_ to limit the active TCP connections (and therefore
        worker threads) to at most :attr:`degu.server.Server.max_connections`
        (this replaces the yucky ``threading.active_count()`` hack); when the
        *max_connections* limit has been reached, the new implementation also
        now rate-limits the handling of new connections to one attempt every 2
        seconds (to mitigate Denial of Service attacks).

    *   Build the ``degu._base`` `C extension`_ with "-std=gnu11" as this will
        soon be the GCC default and we don't necessarily want to make a
        commitment to it working with older standards (although it currently
        does and this wont likely change anytime soon).



0.10 (October 2014)
-------------------

`Download Degu 0.10`_


Breaking API changes:

    *   Change order of the RGI ``app.on_connect()`` arguments from::

            app.on_connect(sock, session)

        To::

            app.on_connect(session, sock)

        Especially when you look at the overall API structurally, this change
        makes it a bit easier to understand that the same *session* argument
        passed to your TCP connection handler is likewise passed to your HTTP
        request handler::

            app.on_connect(session, sock)

                       app(session, request, bodies)

        See the new ``Degu-API.svg`` diagram in the Degu source tree for a good
        structural view of the API.

    *   :meth:`degu.client.Connection.request()` now requires the *headers* and
        *body* arguments always to be provided; ie., the method signature has
        changed from::

            Connection.request(method, uri, headers=None, body=None)

        To::

            Connection.request(method, uri, headers, body)

        Although this means some code is a bit more verbose, it forces people to
        practice the full API and means that any given example someone
        encounters illustrates the full client request API; ie., this is always
        clear::

            conn.request('GET', '/', {}, None)

        Whereas this leaves a bit too much to the imagination when trying to
        figure out how to specify the request headers and request body::

            conn.request('GET', '/')

        This seems especially important as the order of the *headers* and *body*
        are flipped in Degu compared to `HTTPConnection.request()`_ in the
        Python standard library::

            HTTPConnection.request(method, url, body=None, headers={})

        The reason Degu flips the order is so that its API faithfully reflects
        the HTTP wire format... Degu arguments are always in the order that they
        are serialized in the TCP stream.  A goal has always been that if you
        know the HTTP wire format, it should be extremely easy to map that
        understanding into the Degu API.

        Post Degu 1.0, we could always again make the *headers* and *body*
        optional without breaking backword compatibility, but the reverse isn't
        true.  So we'll let this experiment run for a while, and then
        reevaluate.

    *   Drop the ``create_client()`` and ``create_sslclient()`` functions from
        the :mod:`degu.client` module; these convenience functions allowed you
        to create a :class:`degu.client.Client` or
        :class:`degu.client.SSLClient` from a URL, for example::

            client = create_client('http://example.com/')
            sslclient = create_sslclient(sslctx, 'https://example.com/')

        These functions were in part justified as an easy way to set the "host"
        request header when connecting to a server that always requires it (eg.,
        Apache2), but now :attr:`degu.client.Client.host` and the keyword-only
        *host* option provide a much better solution.

        Using a URL to specify a server is really a Degu anti-pattern that we
        don't want to invite, because there's no standard way to encoded the
        IPv6 *flowinfo* and *scopeid* in a URL, nor is there a standard way to
        represent ``AF_UNIX`` socket addresses in a URL.

        Whether by *url* or *address*, the way you specify a server location
        will tend to find its way into lots of 3rd-party code.  We want people
        to use the generic client :ref:`client-address` argument because that's
        the only way they can tranparently use link-local IPv6 addresses and
        ``AF_UNIX`` addresses, both of which you loose with a URL.

    *   :class:`degu.client.Client` and :class:`degu.client.SSLClient` no longer
        take a *base_headers* argument; at best it was an awkward way to set the
        "host" (a header that might truly be justified in every request), and at
        worst, *base_headers* invited another Degu anti-pattern (unconditionally
        including certain headers in every request); the "Degu way" is to do
        special authentication or negotiation per-connection rather than
        per-request (when possible), and to otherwise use request headers
        sparingly in order to minimize the HTTP protocol overhead

    *   If you create a :class:`degu.client.Client` with a 2-tuple or 4-tuple
        :ref:`client-address`, :meth:`degu.client.Connection.request()` will now
        by default include a "host" header in the HTTP request.  This means that
        the Degu client now works by default with servers that require the
        "host" header in every request (like Apache2).  However, you can still
        set the "host" header to ``None`` using the *host* keyword option.

        See :attr:`degu.client.Client.host` for details.

    *   :class:`degu.misc.TempServer` now takes the exact same arguments as
        :class:`degu.server.Server`, no longer uses a *build_func* to create
        the server :ref:`server-app`::

            TempServer(address, app, **options)
                Server(address, app, **options)

        Although the *build_func* and *build_args* in the previous API did
        capture an important pattern for embedding a Degu server in a production
        application, :class:`degu.misc.TempServer` isn't for production use,
        should just illustrate the :class:`degu.server.Server` API as clearly as
        possible.

    *   :class:`degu.misc.TempSSLServer` now takes (with one restiction) the
        exact same arguments as :class:`degu.server.SSLServer`, no longer uses a
        *build_func* to create the server :ref:`server-app`.

        The one restriction is that :class:`degu.misc.TempSSLServer` only
        accepts an *sslconfig* ``dict`` as its first argument, whereas
        :class:`degu.server.SSLServer` accepts either an *sslconfig* ``dict`` or
        an *sslctx* (pre-built ``ssl.SSLContext``)::

            TempSSLServer(sslconfig, address, app, **options)
                SSLServer(sslconfig, address, app, **options)
                SSLServer(sslctx,    address, app, **options)

        Although the *build_func* and *build_args* in the previous API did
        capture an important pattern for embedding a Degu server in a production
        application, :class:`degu.misc.TempSSLServer` isn't for production use,
        should just illustrate the :class:`degu.server.SSLServer` API as clearly
        as possible.

    *   In :mod:`degu`, demote ``start_server()`` and ``start_sslserver()``
        functions to private, internal-use API, replacing them with:

            * :class:`degu.EmbeddedServer`
            * :class:`degu.EmbeddedSSLServer`

        When garbage collected, instances of these classes will automatically
        terminate the process, similar to :class:`degu.misc.TempServer` and
        :class:`degu.misc.TempSSLServer`.

        Not only are these classes easier to use, they also make it much easier
        to add new functionality in the future without breaking backword
        compatability.

        The ``(process, address)`` 2-tuple returned by ``start_server()`` and
        ``start_sslserver()`` was a far too fragile API agreement.  For example,
        even just needing another value from the background process would mean
        using a 3-tuple, which would break the API.

    *   Rename *config* to *sslconfig* as used internally in the sslctx
        build functions:

            * :func:`degu.server.build_server_sslctx()`
            * :func:`degu.client.build_client_sslctx()`

        This is only a breaking API change if you have unit tests that check the
        the exact error strings used in TypeError and ValueError these functions
        raise.  In these messages, you'll now need to use ``sslconfig`` in place
        of ``config``.

    *   Replace previous :class:`degu.misc.TempPKI` *get_foo_config()* methods
        with *foo_sslconfig* properties, to be consistent with the above naming
        convention change, yet still be a bit less verbose::

            pki.get_server_config()
            pki.server_sslconfig

            pki.get_client_config()
            pki.client_sslconfig

            pki.get_anonymous_server_config()
            pki.anonymous_server_sslconfig

            pki.get_anonymous_server_config()
            pki.anonymous_server_sslconfig


Other changes:

    *   :class:`degu.client.Client` and :class:`degu.client.SSLClient` now
        accept generic and easily extensible keyword-only *options*::

                       Client(address, **options)
            SSLClient(sslctx, address, **options)

        *host*, *timeout*, *bodies*, and *Connection* are the currently
        supported keyword-only *options*, which are exposed via new attributes
        with the same name:

            * :attr:`degu.client.Client.host`
            * :attr:`degu.client.Client.timeout`
            * :attr:`degu.client.Client.bodies`
            * :attr:`degu.client.Client.Connection`

        See the client :ref:`client-options` for details.


    *   :class:`degu.server.Server` and :class:`degu.server.SSLServer` now also
        accepts generic and easily extensible keyword-only *options*::

                       Server(address, app, **options)
            SSLServer(sslctx, address, app, **options)

        See the server :ref:`server-options` for details.


    *   The RGI *request* argument now includes a ``uri`` item, which will be
        the complete, unparsed URI from the request line, for example::

            request = {
                'method': 'GET',
                'uri': '/foo/bar/baz?stuff=junk',
                'script': ['foo'],
                'path': ['bar', 'baz'],
                'query': 'stuff=junk',
                'headers': {'accept': 'text/plain'},
                'body': None,
            }

        ``request['uri']`` was added so that RGI validation middleware can check
        that the URI was properly parsed and that any path shifting was done
        correctly.  It's also handy for logging.


    *   :func:`degu.server.build_server_sslctx()` and
        :func:`degu.client.build_client_sslctx()` now unconditionally set the
        *ciphers* to::

            'ECDHE-RSA-AES128-GCM-SHA256:ECDHE-RSA-AES256-GCM-SHA384'

        Arguably AES128 is more secure than AES256 (especially because it's more
        resistant to timing attacks), plus it's faster.  However, SHA384 is
        certainly more secure than SHA256, both because it uses a 512-bit vs.
        256-bit internal state size, and because it's not vulnerable to message
        extension attacks (because the internal state is truncated to produce 
        the digest).  SHA384 is also faster than SHA256 on 64-bit hardware.

        If openssl supported it, this would be our default::

            'ECDHE-RSA-AES128-GCM-SHA384'

        However, on the balance, ``'ECDHE-RSA-AES128-GCM-SHA256'`` still feels
        like the best choice, especially because of the better performance it
        offers.

        Note that as ``'ECDHE-RSA-AES256-GCM-SHA384'`` is still supported as an
        option, Degu 0.10 remains network compatible with Degu 0.9 and earlier.

        Post Degu 1.0, we'll likely make it possible to specify the *ciphers*
        via your *sslconfig*, which can be done without breaking backward
        compatibility.



0.9 (September 2014)
--------------------

`Download Degu 0.9`_

Security fixes:

    *   :func:`degu.base.read_preamble()` now carefully restricts what bytes are
        allowed to exist in the first line, header names, and header values; in
        particular, this function now prevents the NUL byte (``b'\x00'``) from
        being included in any decoded ``str`` objects; for details, please see
        :doc:`security`

    *   :func:`degu.base.read_chunk()` likewise prevents the NUL byte
        (``b'\x00'``) from being included in the optional per-chunk extension

    *   :class:`degu.server.Server` now limits itself to 100 active threads (ie,
        100 concurrent connections) to prevent unbounded resource usage; this is
        hard-coded in 0.9 but will be configurable in 1.0


Breaking API changes:

    *   The RGI request signature is now ``app(session, request, bodies)``, and
        wrapper classes like ``session['rgi.Body']`` have moved to
        ``bodies.Body``, etc.

        For example, this Degu 0.8 RGI application::

            def my_file_app(session, request):
                myfile = open('/my/file', 'rb')
                body = session['rgi.Body'](myfile, 42)
                return (200, 'OK', {}, body)

        Is implemented like this in Degu 0.9::

            def my_file_app(session, request, bodies):
                myfile = open('/my/file', 'rb')
                body = bodies.Body(myfile, 42)
                return (200, 'OK', {}, body)

        The four HTTP body wrapper classes are now exposed as:

            ==========================  ==================================
            Exposed via                 Degu implementation
            ==========================  ==================================
            ``bodies.Body``             :class:`degu.base.Body`
            ``bodies.BodyIter``         :class:`degu.base.BodyIter`
            ``bodies.ChunkedBody``      :class:`degu.base.ChunkedBody`
            ``bodies.ChunkedBodyIter``  :class:`degu.base.ChunkedBodyIter`
            ==========================  ==================================

    *   The following four items have been dropped from the RGI *session*
        argument::

            session['rgi.version']  # eg, (0, 1)
            session['scheme']       # eg, 'https'
            session['protocol']     # eg, 'HTTP/1.1'
            session['server']       # eg, ('0.0.0.0', 12345)

        Although inspired by equivalent information in the WSGI *environ*, they
        don't seem particularly useful for the P2P REST API use case that Degu
        is focused on; in order to minimize the stable API commitments we're
        making for Degu 1.0, we're removing them for now, but we're open to
        adding any of them back post 1.0, assuming there is a good
        justification.


Other changes:

    *   Move ``_degu`` module to ``degu._base`` (the C extension)

    *   Rename ``degu.fallback`` module to ``degu._basepy`` (the pure-Python
        reference implementation)

    *   To keep memory usage flatter over time, :class:`degu.server.Server()`
        now unconditionally closes a connection after 5,000 requests have been
        handled; this is hard-coded in 0.9 but will be configurable in 1.0

    *   :class:`degu.base.Body()` now takes optional *iosize* kwarg; which
        defaults to :data:`degu.base.FILE_IO_BYTES`

    *   Add :meth:`degu.base.Body.write_to()` method to :class:`degu.base.Body`
        and its friends; this gives the HTTP body wrapper API greater
        composability, particularly useful should a Degu client or server use
        the *bodies* implementation from a other independent project


Performance improvements:

    *   The C implementation of :func:`degu.base.read_preamble()` is now around
        42% faster; this speed-up is thanks to decoding and case-folding the
        header keys in a single pass rather than using ``str.casefold()``, plus
        thanks to calling ``rfile.readline()`` using ``PyObject_Call()`` with
        pre-built argument tuples instead of ``PyObject_CallFunctionObjArgs()``
        with pre-built ``int`` objects

    *   :func:`degu.server.write_response()` is now around 8% faster, thanks to
        using a list comprehension for the headers, using a local variable for
        ``wfile.write``, and inlining the body writing

    *   Likewise, :func:`degu.client.write_request()` is also now around 8%
        faster, thanks to the same optimizations

    *   ``benchmark.py`` is now around 6% faster for ``AF_INET6`` and around 7%
        faster for ``AF_UNIX``

.. note::

    These benchmarks were done on an Intel® Core™ i5-4200M (2.5 GHz, dual-core,
    hyper-threaded) CPU running 64-bit Ubuntu 14.04.1, on AC power using the
    "performance" governor.

    To reproduce these results, you'll need to copy the ``benchmark.py`` and
    ``benchmark-parsing.py`` scripts from the Degu 0.9 source tree to the Degu
    0.8 source tree.



0.8 (August 2014)
-----------------

`Download Degu 0.8`_

Changes:

    * Add new :mod:`degu.rgi` module with :class:`degu.rgi.Validator` middleware
      for for verifying that servers, other middleware, and applications all
      comply with the :doc:`rgi` specification; this is a big step toward
      stabilizing both the RGI specification and the Degu API

    * Remove ``degu.server.Handler`` and ``degu.server.validate_response()``
      (unused since Degu 0.6)



0.7 (July 2014)
---------------

`Download Degu 0.7`_

Changes:

    * Rework :func:`degu.base.read_preamble()` to do header parsing itself; this
      combines the functionality of the previous ``read_preamble()`` function
      with the functionality of the now removed ``parse_headers()`` function
      (this is a breaking internal API change)

    * Add a C implementation of the new ``read_preamble()`` function, which
      provides around a 318% performance improvement over the pure-Python
      equivalent in Degu 0.6

    * The RGI server application used in the ``benchmark.py`` script now uses a
      static response body, which removes the noise from ``json.loads()``,
      ``json.dumps()``, and makes the ``benchmark.py`` results more consistent
      and more representative of true Degu performance

    * When using the new C version of ``read_preamble()``, ``benchmark.py`` is
      now around 20% faster for ``AF_INET6``, and around 26% faster for
      ``AF_UNIX`` (on an Intel® Core™ i7-4900MQ when using the *performance*
      governor); note that to verify this measurement, you need to copy the
      ``benchmark.py`` script from the Degu 0.7 tree back into the Degu 0.6 tree



0.6 (June 2014)
---------------

`Download Degu 0.6`_

Although Degu 0.6 brings a large number of breaking API changes, the high-level
server and client APIs are now (more or less) feature complete and can be (at
least cautiously) treated as API-stable; however, significant breakage and churn
should still be expected over the next few months in lower-level, internal, and
currently undocumented APIs.

Changes:

    * Consolidate previously scattered and undocumented RGI server application
      helper functions into the new :mod:`degu.util` module

    * Document some of the internal API functions in :mod:`degu.base` (note that
      none of these are API stable yet), plus document the new public IO
      abstraction classes:

        * :class:`degu.base.Body`

        * :class:`degu.base.BodyIter`

        * :class:`degu.base.ChunkedBody`

        * :class:`degu.base.ChunkedBodyIter`

    * As a result of the reworked IO abstraction classes (breaking change
      below), an incoming HTTP body can now be directly used as an outgoing HTTP
      body with no intermediate wrapper; this even further simplifies what it
      takes to implement an RGI reverse-proxy application

    * Degu and RGI now fully expose chunked transfer-encoding semantics,
      including the optional per-chunk extension; on both the input and output
      side of things, a chunk is now represented by a 2-tuple::

        (data, extension)

    * Largely rewrite the :doc:`rgi` specification to reflect the new
      connection-level semantics

    * Big update to the :doc:`tutorial` to cover request and response bodies,
      the IO abstraction classes, and chunked-encoding

    * Degu is now approximately 35% faster when it comes to writing an HTTP
      request or response preamble with 6 (or so) headers; the more headers, the
      bigger the performance improvement

    * Add ``./setup.py test --skip-slow`` option to skip the time-consuming (but
      important) live socket timeout tests... very handy for day-to-day
      development


Internal API changes:

    * ``read_lines_iter()`` has been replaced by
      :func:`degu.base.read_preamble()`

    * ``EmptyLineError`` has been renamed to :exc:`degu.base.EmptyPreambleError`

    * :func:`degu.base.read_chunk()` and :func:`degu.base.write_chunk()` now
      enforce a sane 16 MiB per-chunk data size limit

    * :func:`degu.base.read_preamble()` now allows up to 15 request or response
      headers (up from the previous 10 header limit)


Breaking public API changes:

    * If an RGI application object itself has an ``on_connect`` attribute, it
      must be a callable accepting two arguments (a *sock* and a *session*);
      when defined, ``app.on_connect()`` will be called whenever a new
      connection is recieved, before any requests have been handled for that
      connection; if ``app.on_connect()`` does not return ``True``, or if any
      unhandled exception occurs, the socket connection will be immediately
      shutdown without further processing; note that this is only a *breaking*
      API change if your application object happened to have an ``on_connect``
      attribute already used for some other purpose

    * RGI server applications now take two arguments when handling requests: a
      *session* and a *request*, both ``dict`` instances; the *request* argument
      now only contains strictly per-request information, whereas the
      server-wide and per-connection information has been moved into the new
      *session* argument

    * Replace previously separate input and output abstractions with new unified
      :class:`degu.base.Body` and :class:`degu.base.ChunkedBody` classes for
      wrapping file-like objects, plus :class:`degu.base.BodyIter` and
      :class:`degu.base.ChunkedBodyIter` classes for wrapping arbitrary iterable
      objects

    * As a result of the above two breaking changes, the names under which these
      wrappers classes are exposed to RGI applications have changed, plus
      they're now in the new RGI *session* argument instead of the existing
      *request* argument:

        ==================================  ==================================
        Exposed via                         Degu implementation
        ==================================  ==================================
        ``session['rgi.Body']``             :class:`degu.base.Body`
        ``session['rgi.BodyIter']``         :class:`degu.base.BodyIter`
        ``session['rgi.ChunkedBody']``      :class:`degu.base.ChunkedBody`
        ``session['rgi.ChunkedBodyIter']``  :class:`degu.base.ChunkedBodyIter`
        ==================================  ==================================

    * The previous ``make_input_from_output()`` function has been removed; there
      is no need for this now that you can directly use any HTTP input body as
      an HTTP output body (for, say, a reverse-proxy application)

    * Iterating through a chunk-encoded HTTP input body now yields a
      ``(data, extension)`` 2-tuple for each chunk; likewise,
      ``body.readchunk()`` now returns a ``(data, extension)`` 2-tuple; however,
      there has been no change in the behavior of ``body.read()`` on
      chunk-encoded bodies

    * Iterables used as the source for a chunk-encoded HTTP output body now must
      yield a ``(data, extension)`` 2-tuple for each chunk

In terms of the RGI request handling API, this is how you implemented a
*hello, world* RGI application in Degu 0.5 and earlier:

>>> def hello_world_app(request):
...     return (200, 'OK', {'content-length': 12}, b'hello, world')
...

As of Degu 0.6, it must now be implemented like this:

>>> def hello_world_app(session, request):
...     return (200, 'OK', {'content-length': 12}, b'hello, world')
...

Or here's a version that uses the connection-handling feature new in Degu 0.6:

>>> class HelloWorldApp:
... 
...     def __call__(self, session, request):
...         return (200, 'OK', {'content-length': 12}, b'hello, world')
... 
...     def on_connect(self, sock, session):
...         return True
... 

If the ``app.on_connect`` attribute exists, ``None`` is also a valid value.  If
needed, this allows you to entirely disable the connection handler in a
subclass.  For example:

>>> class HelloWorldAppSubclass(HelloWorldApp):
...     on_connect = None
... 

For more details, please see the :doc:`rgi` specification.



0.5 (May 2014)
--------------

`Download Degu 0.5`_

Changes:

    * Greatly expand and enhance documentation for the :mod:`degu.client` module

    * Modest update to the :mod:`degu.server` module documentation, in
      particular to cover HTTP over ``AF_UNIX``

    * Add a number of additional sanity and security checks in
      :func:`degu.client.build_client_sslctx()`, expand its unit tests
      accordingly

    * Likewise, add additional checks in
      :func:`degu.server.build_server_sslctx()`, expand its unit tests
      accordingly

    * :meth:`degu.client.Connection.close()` now only calls
      ``socket.socket.shutdown()``, which is more correct, and also eliminates
      annoying exceptions that could occur when a
      :class:`degu.client.Connection` (previously ``Client`` or ``SSLClient``)
      is garbage collected immediately prior to a script exiting

Breaking public API changes:

    * The ``Connection`` namedtuple has been replaced by the
      :class:`degu.client.Connection` class

    * ``Client.request()`` has been moved to
      :meth:`degu.client.Connection.request()`

    * ``Client.close()`` has been moved to
      :meth:`degu.client.Connection.close()`

Whereas previously you'd do something like this::

    from degu.client import Client
    client = Client(('127.0.0.1', 5984))
    client.request('GET', '/')
    client.close()

As of Degu 0.5, you now need to do this::

    from degu.client import Client
    client = Client(('127.0.0.1', 5984))
    conn = client.connect()
    conn.request('GET', '/')
    conn.close()

:class:`degu.client.Client` and :class:`degu.client.SSLClient` instances are
now stateless and thread-safe, do not themselves reference any socket resources.
On the other hand, :class:`degu.client.Connection` instances are stateful and
are *not* thread-safe.

Two things motivated these breaking API changes:

    * Justifiably, ``Client`` and ``SSLClient`` do rather thorough type and
      value checking on their constructor arguments; whereas previously you had
      to create a client instance per connection (eg, per thread), now you can
      create an arbitrary number of connections from a single client; this means
      that connections now are faster to create and have a lower per-connection
      memory footprint

    * In the near future, the Degu client API will support an  ``on_connect()``
      handler to allow 3rd party applications to do things like extended
      per-connection authentication; splitting the client creation out from the
      connection creation allows most 3rd party code to remain oblivious as to
      whether such an ``on_connect()`` handler is in use (as most code can
      merely create connections using the provided client, rather than
      themselves creating clients)



.. _`Download Degu 0.11`: https://launchpad.net/degu/+milestone/0.11
.. _`Download Degu 0.10`: https://launchpad.net/degu/+milestone/0.10
.. _`Download Degu 0.9`: https://launchpad.net/degu/+milestone/0.9
.. _`Download Degu 0.8`: https://launchpad.net/degu/+milestone/0.8
.. _`Download Degu 0.7`: https://launchpad.net/degu/+milestone/0.7
.. _`Download Degu 0.6`: https://launchpad.net/degu/+milestone/0.6
.. _`Download Degu 0.5`: https://launchpad.net/degu/+milestone/0.5

.. _`HTTPConnection.request()`: https://docs.python.org/3/library/http.client.html#http.client.HTTPConnection.request
.. _`io`: https://docs.python.org/3/library/io.html
.. _`BoundedSemaphore`: https://docs.python.org/3/library/threading.html#threading.BoundedSemaphore
.. _`C extension`: http://bazaar.launchpad.net/~dmedia/degu/trunk/view/head:/degu/_base.c
.. _`your feedback`: https://bugs.launchpad.net/degu
