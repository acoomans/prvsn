import unittest

from prvsnlib.utils.list import unique


class TestList(unittest.TestCase):

    def test_unique(self):
        self.assertListEqual(unique([1, 2, 1]), [1, 2])
