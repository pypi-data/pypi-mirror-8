import unittest
import random

from . import CacheTestMixin, DecoratorTestMixin
from cachetools import RRCache, rr_cache


class RRCacheTest(unittest.TestCase, CacheTestMixin, DecoratorTestMixin):

    def cache(self, maxsize, choice=random.choice, getsizeof=None):
        return RRCache(maxsize, choice=choice, getsizeof=getsizeof)

    def decorator(self, maxsize, choice=random.choice, typed=False, lock=None):
        return rr_cache(maxsize, choice=choice, typed=typed, lock=lock)

    def test_choice(self):
        cache = self.cache(maxsize=2, choice=min)

        cache[1] = 1
        cache[2] = 2
        cache[3] = 3

        self.assertEqual(2, len(cache))
        self.assertEqual(2, cache[2])
        self.assertEqual(3, cache[3])
        self.assertNotIn(1, cache)

        cache[0] = 0
        self.assertEqual(2, len(cache))
        self.assertEqual(0, cache[0])
        self.assertEqual(3, cache[3])
        self.assertNotIn(2, cache)

        cache[4] = 4
        self.assertEqual(2, len(cache))
        self.assertEqual(3, cache[3])
        self.assertEqual(4, cache[4])
        self.assertNotIn(0, cache)
