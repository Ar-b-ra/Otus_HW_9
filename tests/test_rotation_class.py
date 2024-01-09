import unittest
from math import cos, sin

from abs_implementation.implementation import (
    RealVelocity,
    RealPosition,
    RealRotate,
    Vector,
)
from ship import RotatableShip


class TestGetNewVelocity(unittest.TestCase):
    def setUp(self):
        angle = 30
        self.ship = RotatableShip(
            Vector(RealPosition(), RealVelocity()), RealRotate(angle)
        )

    def test_positive_velocity(self):
        current_velocity = RealVelocity(10, 5)
        expected_velocity = RealVelocity(10 * cos(30), 5 * sin(30))
        new_velocity = self.ship.get_new_velocity(current_velocity)
        self.assertEqual(new_velocity, expected_velocity)

    def test_negative_velocity(self):
        current_velocity = RealVelocity(-10, -5)
        expected_velocity = RealVelocity(-10 * cos(30), -5 * sin(30))
        new_velocity = self.ship.get_new_velocity(current_velocity)
        self.assertEqual(new_velocity, expected_velocity)

    def test_zero_velocity(self):
        current_velocity = RealVelocity(0, 0)
        expected_velocity = RealVelocity(0, 0)
        new_velocity = self.ship.get_new_velocity(current_velocity)
        self.assertEqual(new_velocity, expected_velocity)


if __name__ == "__main__":
    unittest.main()
