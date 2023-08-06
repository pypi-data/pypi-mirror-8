Degu
====

`Degu`_ is an embedded HTTP server and client library for Python3.

It can be used to build network-transparent services, whether the other endpoint
is in the cloud, on the local network, on the localhost, or even on the
localhost using HTTP over ``AF_UNIX``.

Degu is especially well suited for implementing REST APIs for device-to-device
communication.  It's a building block for future stuff, your vehicle into bold,
uncharted territory.

.. note::

    Degu is now *tentatively* API-stable.  So it's a great time to jump in and
    `give feedback!`_  But there's still a chance that there will be minor
    breaking changes on the way to the API-stable 1.0 release.

Degu includes:

    *   **A lightweight HTTP server** that's easy to embed within applications

    *   **A matching HTTP client** carefully designed to harmonize with the
        server

    *   **IO abstractions** used by the server and client for HTTP request and
        response bodies

    *   **Test fixtures** for creating throw-away Degu servers for unit testing,
        illustration, and play

Degu server applications are implemented according to the :doc:`rgi`, which is
very much in the spirit of `WSGI`_ but does not attempt to be compatible with
`CGI`_, nor necessarily to be compatible with any existing HTTP servers.

Degu is being developed as part of the `Novacut`_ project. Packages are
available for `Ubuntu`_ in the `Novacut Stable Releases PPA`_ and the `Novacut
Daily Builds PPA`_.

If you have questions or need help getting started with Degu, please stop by the
`#novacut`_ IRC channel on freenode.

Degu is licensed `LGPLv3+`_, and requires `Python 3.4`_ or newer.

Contents:

.. toctree::
    :maxdepth: 3

    install
    tutorial
    degu
    degu.server
    degu.client
    degu.base
    degu.misc
    degu.util
    degu.rgi
    rgi
    security
    changelog


.. _`Degu`: https://launchpad.net/degu
.. _`http.client`: https://docs.python.org/3/library/http.client.html
.. _`WSGI`: http://www.python.org/dev/peps/pep-3333/
.. _`CGI`: http://en.wikipedia.org/wiki/Common_Gateway_Interface

.. _`LGPLv3+`: http://www.gnu.org/licenses/lgpl-3.0.html
.. _`Novacut`: https://wiki.ubuntu.com/Novacut
.. _`Novacut Stable Releases PPA`: https://launchpad.net/~novacut/+archive/stable
.. _`Novacut Daily Builds PPA`: https://launchpad.net/~novacut/+archive/daily
.. _`#novacut`: http://webchat.freenode.net/?channels=novacut
.. _`Ubuntu`: http://www.ubuntu.com/
.. _`Python 3.4`: https://docs.python.org/3/
.. _`give feedback!`: https://bugs.launchpad.net/degu

