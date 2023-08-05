__author__ = 'Shyue Ping Ong'
__copyright__ = 'Copyright 2014, The Materials Virtual Lab'
__version__ = '0.1'
__maintainer__ = 'Shyue Ping Ong'
__email__ = 'ongsp@ucsd.edu'
__date__ = '1/24/14'


import unittest
import os

from monty.collections import frozendict, NotOverwritableDict, AttrDict

test_dir = os.path.join(os.path.dirname(__file__), 'test_files')

class FrozenDictTest(unittest.TestCase):

    def test_frozen_dict(self):
        d = frozendict({"hello": "world"})
        self.assertRaises(KeyError, d.__setitem__, "k", "v")
        self.assertEqual(d["hello"], "world")

    def test_notoverwritable_dict(self):
        d = NotOverwritableDict(foo="bar")
        d["hello"] = "world"
        self.assertEqual(d["foo"], "bar")
        self.assertRaises(KeyError, d.__setitem__, "foo", "spam")

    def test_attr_dict(self):
        d = AttrDict(foo=1, bar=2)
        self.assertEqual(d.bar, 2)
        self.assertEqual(d["foo"], d.foo)
        d.bar = "hello"
        self.assertEqual(d["bar"], "hello")


if __name__ == "__main__":
    unittest.main()
