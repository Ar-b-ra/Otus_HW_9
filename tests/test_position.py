import unittest

from abs_implementation.implementation import RealPosition


class TestChangePosition(unittest.TestCase):
    def setUp(self):
        self.position1 = RealPosition(1, 2)
        self.position2 = RealPosition(3, 4)
        self.position3 = RealPosition(5, 6)
        self.position4 = RealPosition(0, 0)
        self.position5 = RealPosition(1, -2)
        self.position6 = RealPosition(-3, 4)

    def test_add(self):
        self.assertEqual(self.position1 + self.position2, RealPosition(4, 6))
        self.assertEqual(self.position1 + self.position3, RealPosition(6, 8))
        self.assertEqual(self.position2 + self.position3, RealPosition(8, 10))
        self.assertEqual(self.position1 + self.position4, RealPosition(1, 2))
        self.assertEqual(self.position1 + self.position5, RealPosition(2, 0))
        self.assertEqual(self.position1 + self.position6, RealPosition(-2, 6))

    def test_position(self):
        self.position1 += RealPosition(1, 2)
        self.assertEqual(self.position1.get_position(), (2, 4))


if __name__ == '__main__':
    unittest.main()
