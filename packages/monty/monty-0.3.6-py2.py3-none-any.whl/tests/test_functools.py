__author__ = 'Shyue Ping Ong'
__copyright__ = 'Copyright 2013, The Materials Project'
__version__ = '0.1'
__maintainer__ = 'Shyue Ping Ong'
__email__ = 'ongsp@ucsd.edu'
__date__ = '8/29/14'

import unittest

from monty.functools import lru_cache


class TestLRUCache(unittest.TestCase):
    def test_function(self):
        @lru_cache(2)
        def cached_func(a, b):
            return a + b

        #call a few times to get some stats
        self.assertEqual(cached_func(1, 2), 3)
        self.assertEqual(cached_func(3, 2), 5)
        self.assertEqual(cached_func(3, 2), 5)
        self.assertEqual(cached_func(1, 2), 3)
        self.assertEqual(cached_func(4, 2), 6)
        self.assertEqual(cached_func(4, 2), 6)
        self.assertEqual(cached_func(3, 2), 5)
        self.assertEqual(cached_func(1, 2), 3)

        self.assertEqual(cached_func.cache_info().hits, 3)
        self.assertEqual(cached_func.cache_info().misses, 5)

    def test_class_method(self):
        class TestClass():
            @lru_cache(10)
            def cached_func(self, x):
                return x

        a = TestClass()
        b = TestClass()

        self.assertEqual(a.cached_func(1), 1)
        self.assertEqual(b.cached_func(2), 2)
        self.assertEqual(b.cached_func(3), 3)
        self.assertEqual(a.cached_func(3), 3)
        self.assertEqual(a.cached_func(1), 1)

        self.assertEqual(a.cached_func.cache_info().hits, 1)
        self.assertEqual(a.cached_func.cache_info().misses, 4)

if __name__ == '__main__':
    unittest.main()
