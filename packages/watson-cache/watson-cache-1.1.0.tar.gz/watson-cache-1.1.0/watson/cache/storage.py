# -*- coding: utf-8 -*-
import collections
from datetime import datetime, timedelta
import os
import pickle
from tempfile import gettempdir
from watson.common.imports import get_qualified_name
from watson.common.contextmanagers import suppress
with suppress(ImportError):
    import memcache
with suppress(ImportError):
    import redis


class BaseStorage(object):

    """Base class for all cache storage classes.

    Cache storage classes are designed to act similar to a dict, however get and
    set methods can be used when a timeout is required on a set, or when a default
    value is to be specified on a get.

    Attributes:
        config (dict): The relevant configuration settings for the storage.
    """
    config = None

    def __init__(self, config=None):
        self.config = config or {}

    def __setitem__(self, key, value, timeout=0):
        """See set()
        """
        raise NotImplementedError('__setitem__ must be implemented')

    def __getitem__(self, key, default=None):
        """See get()
        """
        raise NotImplementedError('__getitem__ must be implemented')

    def __delitem__(self, key):
        """Delete a key from the cache.

        Args:
            key (string): The key to delete

        Example:

        .. code-block:: python

            del cache['key'] # deletes 'key' from the cache
        """
        raise NotImplementedError('__delitem__ must be implemented')

    def __contains__(self, key):
        """Determine whether or not a key exists in the cache.

        Args:
            key (string): The key to find

        Returns:
            Boolean: True/False depending on if the key exists.

        Example:

        .. code-block:: python

            if 'key' in cache:
                print('exists!')
        """
        raise NotImplementedError('__contains__ must be implemented')

    def flush(self):
        """Clears all items from the cache.
        """
        raise NotImplementedError('flush must be implemented')

    def expired(self, key):
        """Determine if a key has expired or not.

        Args:
            key (string): The key to find

        Returns:
            Boolean: True/False depending on expiration
        """
        raise NotImplementedError('expired must be implemented')

    def __repr__(self):
        return '<{0}>'.format(get_qualified_name(self))

    # Convenience methods

    def set(self, key, value, timeout=0):
        """Sets a key in the cache.

        Args:
            key (string): The key to be used as a reference
            value (mixed): The value to store in the key
            timeout (int): The amount of time in seconds a key is valid for.

        Example:

        .. code-block:: python

            cache['key'] = 'value'
        """
        self.__setitem__(key, value, timeout)

    def get(self, key, default=None):
        """Gets a key from the cache, returns the default if not set.

        Args:
            key (string): The key to be retrieved

        Returns:
            The value stored within the cache

        Example:

        .. code-block:: python

            value = cache['key']
        """
        return self.__getitem__(key, default)


class Memory(BaseStorage):

    """A cache storage mechanism for storing items in memory.

    Memory cache storage will maintain the cache while the application is being
    run. This is usually best used in instances when you don't want to keep
    the cached items after the application has finished running.
    """

    def __init__(self):
        self._cache = {}

    def __setitem__(self, key, value, timeout=0):
        expires = datetime.now() + timedelta(
            seconds=int(timeout)) if timeout else None
        self._cache.__setitem__(key, (value, expires))

    def __getitem__(self, key, default=None):
        if self.expired(key):
            return default
        else:
            value, expires = self._stored(key, default)
            return value

    def __delitem__(self, key):
        self._cache.__delitem__(key)

    def flush(self):
        self._cache.clear()
        return True

    def expired(self, key):
        value, expires = self._stored(key)
        if expires is not None and expires < datetime.now():
            return True
        return False

    def __contains__(self, key):
        return self._cache.__contains__(key)

    def _stored(self, key, default=None):
        (value, expires) = self._cache.get(key, (default, None))
        return value, expires


class File(BaseStorage):

    """A cache storage mechanism for storing items on the local filesystem.

    File cache storage will persist the data to the filesystem in whichever
    directory has been specified in the configuration options. If no
    directory is specified then the system temporary folder will be used.
    """

    def __init__(self, config=None):
        """
        Initializes the cache.

        Args:
            config (dict): The config for the cache

        Example:

        .. code-block:: python

            cache = File({'dir': '/tmp', 'prefix': 'my-cache'})
            # all cached items will be saved to /tmp
            # and will be prefixed with my-cache
            cache['key'] = 'value' # /tmp/my-cache-key contains a serialized 'value'
        """
        settings = {'dir': gettempdir(), 'prefix': 'cache'}
        self.config = collections.ChainMap(config or {}, settings)

    def __setitem__(self, key, value, timeout=0):
        expires = datetime.now() + timedelta(
            seconds=int(timeout)) if timeout else None
        with open(self.__file_path(key), 'wb') as file:
            with suppress(Exception):
                pickle.dump((value, expires), file, pickle.HIGHEST_PROTOCOL)

    def __getitem__(self, key, default=None):
        if self.expired(key):
            return default
        else:
            value, expires = self._stored(key, default)
            return value

    def __delitem__(self, key):
        with suppress(OSError):
            os.unlink(self.__file_path(key))

    def expired(self, key):
        value, expires = self._stored(key)
        if expires is not None and expires < datetime.now():
            return True
        return False

    def __contains__(self, key):
        return os.path.exists(self.__file_path(key))

    def flush(self):
        storage_dir = self.config['dir']
        index = len(self.config['prefix']) + 1
        files = [f for f in os.listdir(storage_dir) if self.__is_cache_file(f)]
        for file in files:
            del self[file[index:]]
        return True

    def _stored(self, key, default=None):
        value, expires = default, None
        with suppress(OSError):
            with open(self.__file_path(key), 'rb') as file:
                with suppress(Exception):
                    (value, expires) = pickle.load(file)
        return value, expires

    def __cache_file(self, file):
        storage_dir = self.config['dir']
        return os.path.abspath(os.path.join(storage_dir, file))

    def __is_cache_file(self, file):
        if not file.startswith(self.config['prefix']):
            return False
        return os.path.isfile(self.__cache_file(file))

    def __file_path(self, key):
        return (
            os.path.join(
                self.config['dir'],
                '{0}-{1}'.format(self.config['prefix'],
                                 key))
        )

    def __repr__(self):
        return (
            '<{0} dir:{1}>'.format(
                get_qualified_name(self),
                self.config['dir'])
        )


class Memcached(BaseStorage):

    """A cache storage mechanism for storing items in memcached.

    Memcached cache storage will utilize python3-memcached to maintain the cache
    across multiple servers.
    Python3-memcached documentation can be found at http://pypi.python.org/pypi/python3-memcached/
    """
    client = None

    def __init__(self, config=None):
        """
        Initializes the cache.

        Args:
            config (dict): The config for the cache

        Example:

        .. code-block:: python

            cache = Memcached({'servers': ['127.0.0.1:11211', '192.168.100.1:11211']})
        """
        settings = {'servers': ['127.0.0.1:11211']}
        if not config:
            config = {}
        settings.update(config)
        self.config = settings

    def __setitem__(self, key, value, timeout=0):
        self.open()
        self.client.set(key, value, timeout)

    def __getitem__(self, key, default=None):
        self.open()
        value = self.client.get(key)
        if not value:
            return default
        return value

    def __delitem__(self, key):
        self.open()
        return self.client.delete(key)

    def flush(self):
        self.open()
        self.client.flush_all()
        return True

    def open(self):
        if not self.client:
            try:
                self.client = memcache.Client(self.config['servers'])
            except:
                raise ImportError('You must have python3-memcached installed.')

    def close(self):
        self.open()
        self.client.disconnect_all()
        return True

    def __contains__(self, key):
        return True if self.get(key) else False

    def expired(self, key):
        return key not in self

    def __repr__(self):
        return '<{0} servers:{1}>'.format(get_qualified_name(self),
                                          len(self.config['servers']))


class Redis(BaseStorage):

    """A cache storage mechanism for storing items in redis.

    Redis cache storage will utilize redis to maintain the cache
    across multiple servers.
    redis documentation can be found at https://github.com/andymccurdy/redis-py
    """
    client = None

    def __init__(self, config=None):
        """
        Initializes the cache.

        Args:
            config (dict): The config for the cache

        Example:

        .. code-block:: python

            cache = Redis
        """
        settings = {'host': 'localhost', 'port': 6379, 'db': 0}
        if not config:
            config = {}
        settings.update(config)
        self.config = settings

    def __setitem__(self, key, value, timeout=0):
        self.open()
        if timeout < 0:
            del self[key]
        self.client.set(key, value, timeout)

    def __getitem__(self, key, default=None):
        self.open()
        value = self.client.get(key)
        if not value:
            return default
        return value

    def __delitem__(self, key):
        self.open()
        return self.client.delete(key)

    def flush(self):
        self.open()
        self.client.flushdb()
        return True

    def open(self):
        if not self.client:
            try:
                self.client = redis.StrictRedis(**self.config)
            except:
                raise ImportError('You must have redis installed.')

    def close(self):
        self.open()
        self.client.connection_pool.disconnect()
        self.client = None
        return True

    def __contains__(self, key):
        return self.client.exists(key)

    def expired(self, key):
        return key not in self

    def __repr__(self):
        return '<{0} db:{1}>'.format(get_qualified_name(self),
                                     self.config['db'])
