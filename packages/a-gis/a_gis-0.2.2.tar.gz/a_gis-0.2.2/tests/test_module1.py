import unittest

from a_gis.module1 import Number


class TestSimple(unittest.TestCase):

    def test_add(self):
        self.assertEqual((Number(5) + Number(6)).value, 11)


if __name__ == '__main__':
    unittest.main()
