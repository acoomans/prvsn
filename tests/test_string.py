import unittest

from prvsnlib.utils.string import replace_all


class TestFile(unittest.TestCase):

    def testReplacements(self):
        s = 'abc ab abcd'
        r = replace_all(s, {
            'abc': 'xyz',
            'ab': 'rs'
        })
        self.assertEqual('xyz rs xyzd', r)
