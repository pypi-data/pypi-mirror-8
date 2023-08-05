# Copyright 2011-2014 GRNET S.A. All rights reserved.
#
# Redistribution and use in source and binary forms, with or
# without modification, are permitted provided that the following
# conditions are met:
#
#   1. Redistributions of source code must retain the above
#      copyright notice, this list of conditions and the following
#      disclaimer.
#
#   2. Redistributions in binary form must reproduce the above
#      copyright notice, this list of conditions and the following
#      disclaimer in the documentation and/or other materials
#      provided with the distribution.
#
# THIS SOFTWARE IS PROVIDED BY GRNET S.A. ``AS IS'' AND ANY EXPRESS
# OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR
# PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL GRNET S.A OR
# CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
# SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
# LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF
# USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED
# AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT
# LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN
# ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.
#
# The views and conclusions contained in the software and
# documentation are those of the authors and should not be
# interpreted as representing official policies, either expressed
# or implied, of GRNET S.A.

from . import ObjectPool, PooledObject
from select import select

from httplib import (
    HTTPConnection as http_class,
    HTTPSConnection as https_class,
    ResponseNotReady, BadStatusLine,
)

from threading import Lock

import logging

log = logging.getLogger(__name__)

_pools = {}
_pools_mutex = Lock()

default_pool_size = 100
USAGE_LIMIT = 1000


def init_http_pooling(size):
    """Initializes default pool size and clears the pool registry.

    Call before any other calls in the http pool library.
    When forking call again for each new process.

    """
    global default_pool_size
    default_pool_size = size
    _pools.clear()


def _patch_connection(conn):
    """Patch connection object to retry in case of BadStatusLine

    Sometimes, when Apache is used as proxy, HTTP get response may raise a
    BadStatusLine exception. This race condition occurs when the Apache proxy
    module is being used with HTTP keepalive requests. The backend server may
    close the keepalive connection right after httpd has checked the state of
    this TCP connection, so httpd sends the request and waits for a response on
    a connection that is in fact dead.

    Solve the above error by re-sending the request when receiving a
    BadStatusLine exception with empty line ('').

    """
    def _patch_request(*args, **kwargs):
        """Save request parameters and call actual request function"""
        conn._request_args = args
        conn._request_kwargs = kwargs
        conn._old_request(*args, **kwargs)

    def _patch_getresponse():
        """Retry in case of BadStatusLine"""
        tries = 3
        i = 0
        while True:
            i += 1
            try:
                return conn._old_getresponse()
            except BadStatusLine as err:
                if err.line == "''" and i <= tries:
                    # Retry only in case line was empty ('')
                    log.debug("HTTP-RESPONSE: BadStatusLine exception."
                              " Retrying (try %d of %d)" % (i, tries))
                    # Close the old connection
                    conn.close()
                    conn._old_request(*conn._request_args,
                                      **conn._request_kwargs)
                    continue
                else:
                    raise

    # Save original functions
    conn._old_request = conn.request
    conn._old_getresponse = conn.getresponse

    # Create new 'patched' functions
    conn.request = _patch_request
    conn.getresponse = _patch_getresponse


class HTTPConnectionPool(ObjectPool):

    _scheme_to_class = {
        'http': http_class,
        'https': https_class,
    }

    def __init__(self, scheme, netloc, size=None):
        log.debug("INIT-POOL: Initializing pool of size %d, scheme: %s, "
                  "netloc: %s", size, scheme, netloc)
        ObjectPool.__init__(self, size=size)

        connection_class = self._scheme_to_class.get(scheme, None)
        if connection_class is None:
            m = 'Unsupported scheme: %s' % (scheme,)
            raise ValueError(m)

        self.connection_class = connection_class
        self.scheme = scheme
        self.netloc = netloc

    def _pool_create(self):
        log.debug("CREATE-HTTP-BEFORE from pool %r", self)
        conn = self.connection_class(self.netloc)
        conn._pool_use_counter = USAGE_LIMIT
        # Patch connection object to retry in case of BadStatusLine
        _patch_connection(conn)
        return conn

    def _pool_verify(self, conn):
        log.debug("VERIFY-HTTP")
        if conn is None:
            return False
        sock = conn.sock
        if sock is None:
            return True
        if select((conn.sock,), (), (), 0)[0]:
            return False
        return True

    def _pool_cleanup(self, conn):
        log.debug("CLEANUP-HTTP")
        # every connection can be used a finite number of times
        conn._pool_use_counter -= 1

        # see httplib source for connection states documentation
        conn_state = conn._HTTPConnection__state
        if (conn._pool_use_counter > 0 and conn_state == "Idle"):
            try:
                conn.getresponse()
            except ResponseNotReady:
                log.debug("CLEANUP-HTTP: Not closing connection. Will reuse.")
                return False

        log.debug("CLEANUP-HTTP: Closing connection. Will not reuse.")
        conn.close()
        return True


class PooledHTTPConnection(PooledObject):

    _pool_log_prefix = "HTTP"
    _pool_class = HTTPConnectionPool
    _pool_key = __name__

    def __init__(self, netloc, scheme='http', pool=None, pool_key=None, **kw):
        kw['netloc'] = netloc
        kw['scheme'] = scheme
        kw['pool'] = pool
        if pool_key is not None:
            kw['pool_key'] = pool_key
        super(PooledHTTPConnection, self).__init__(**kw)

    def get_pool(self):
        kwargs = self._pool_kwargs
        pool = kwargs.pop('pool', None)
        if pool is not None:
            return pool

        # pool was not given, find one from the global registry
        scheme = kwargs['scheme']
        netloc = kwargs['netloc']
        size = kwargs.get('size', default_pool_size)
        pool_key = kwargs.get('pool_key', self._pool_key)
        # ensure distinct pools for every (scheme, netloc) combination
        key = (pool_key, scheme, netloc)
        with _pools_mutex:
            if key not in _pools:
                log.debug("HTTP-GET: Creating pool for key %s", key)
                pool = HTTPConnectionPool(scheme, netloc, size=size)
                _pools[key] = pool
            else:
                pool = _pools[key]

        return pool
