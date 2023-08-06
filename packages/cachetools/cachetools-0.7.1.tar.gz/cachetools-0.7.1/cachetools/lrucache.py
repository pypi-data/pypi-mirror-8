from .cache import Cache
from .decorators import cachedfunc
from .lock import RLock


class Link(object):

    __slots__ = 'key', 'value', 'prev', 'next'

    def unlink(self):
        next = self.next
        prev = self.prev
        prev.next = next
        next.prev = prev


class LRUCache(Cache):
    """Least Recently Used (LRU) cache implementation.

    This class discards the least recently used items first to make
    space when necessary.

    """

    def __init__(self, maxsize, getsizeof=None):
        if getsizeof is not None:
            Cache.__init__(self, maxsize, lambda link: getsizeof(link.value))
            self.getsizeof = getsizeof
        else:
            Cache.__init__(self, maxsize)
        self.__root = root = Link()
        root.prev = root.next = root

    def __repr__(self, cache_getitem=Cache.__getitem__):
        # prevent item reordering
        return '%s(%r, maxsize=%d, currsize=%d)' % (
            self.__class__.__name__,
            [(key, cache_getitem(self, key).value) for key in self],
            self.maxsize,
            self.currsize,
        )

    def __getitem__(self, key, cache_getitem=Cache.__getitem__):
        link = cache_getitem(self, key)
        next = link.next
        prev = link.prev
        prev.next = next
        next.prev = prev
        link.next = root = self.__root
        link.prev = tail = root.prev
        tail.next = root.prev = link
        return link.value

    def __setitem__(self, key, value,
                    cache_getitem=Cache.__getitem__,
                    cache_setitem=Cache.__setitem__):
        try:
            oldlink = cache_getitem(self, key)
        except KeyError:
            oldlink = None
        link = Link()
        link.key = key
        link.value = value
        cache_setitem(self, key, link)
        if oldlink:
            oldlink.unlink()
        link.next = root = self.__root
        link.prev = tail = root.prev
        tail.next = root.prev = link

    def __delitem__(self, key,
                    cache_getitem=Cache.__getitem__,
                    cache_delitem=Cache.__delitem__):
        link = cache_getitem(self, key)
        cache_delitem(self, key)
        link.unlink()

    def popitem(self):
        """Remove and return the `(key, value)` pair least recently used."""
        root = self.__root
        link = root.next
        if link is root:
            raise KeyError('cache is empty')
        key = link.key
        Cache.__delitem__(self, key)
        link.unlink()
        return (key, link.value)


def lru_cache(maxsize=128, typed=False, getsizeof=None, lock=RLock):
    """Decorator to wrap a function with a memoizing callable that saves
    up to `maxsize` results based on a Least Recently Used (LRU)
    algorithm.

    """
    return cachedfunc(LRUCache(maxsize, getsizeof), typed, lock)
