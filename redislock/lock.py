# -*- coding: utf-8 -*-

from contextlib import contextmanager
from redis import Redis

class Lock(object):
    """Lock implemented on top of redis."""

    def __init__(self, name, timeout=60, db=0):
        """
        Create, if necessary the lock variable in redis.

        We utilize the ``blpop`` command and its blocking behavior.

        The ``_key`` variable is used to check, whether the mutex exists or not,
        while the ``_mutex`` variable is the actual mutex.
        """
        self._key = 'lock:name:%s' % name
        self._mutex = 'lock:mutex:%s' % name
        self._timeout = timeout
        self._r = Redis(db=1)
        self._init_mutex()

    @property
    def mutex_key(self):
        return self._mutex

    def lock(self):
        """
        Lock and block.

        Raises:
            RuntimeError, in case of synchronization issues.
        """
        res = self._r.blpop(self._mutex, self._timeout)
        if res is None:
            raise RuntimeError

    def unlock(self):
        self._r.rpush(self._mutex, 1)

    def _init_mutex(self):
        """
        Initialize the mutex, if necessary.

        Use a separate key to check for the existence of the "mutex",
        so that we can utilize ``getset``, which is atomic.
        """
        exists = self._r.getset(self._key, 1)
        if exists is None:
            self._r.lpush(self._mutex, 1)


@contextmanager
def lock(name, timeout=60):
    """Lock on name using redis."""
    l = Lock(name, timeout)
    try:
        l.lock()
        yield
    finally:
        l.unlock()
