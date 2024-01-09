import unittest

from abs_implementation.implementation import RealPosition, RealVelocity, Vector
from abs_implementation.move import Velocity, Position, Move
from commands.check_fuel_command import CheckFuelCommand
from commands.macro_comand import MacroCommand
from ship import Ship, CommandException


class MovingObjectTest(unittest.TestCase):
    def setUp(self):
        position = RealPosition()
        velocity = RealVelocity()
        vector = Vector(position, velocity)
        self.ship = Ship(vector)

    def test_move_object(self):
        self.ship.set_position(RealPosition(12, 5))
        self.ship.set_velocity(RealVelocity(-7, 3))
        self.ship.move()
        self.assertEqual(self.ship.get_position(), (5, 8))

    def test_no_velocity(self):
        with self.assertRaises(NotImplementedError):
            position = RealPosition()
            velocity = Velocity()
            vector = Vector(position, velocity)
            unmovable_ship = Ship(vector)
            unmovable_ship.move()

    def test_no_position(self):
        with self.assertRaises(NotImplementedError):
            position = Position()
            velocity = RealVelocity()
            vector = Vector(position, velocity)
            unmovable_ship = Ship(vector)
            unmovable_ship.move()

    def test_move_with_immutable_vector(self):
        # Create a mock Vector class with an immutable position
        class ImmutableVector(Vector):

            def __add__(self, other):
                return ImmutableVector(self.x + other.x, self.y + other.y)

            def move(self, coords):
                raise NotImplementedError

        # Create an instance of the Move class with an immutable vector
        move = Move(ImmutableVector(RealPosition(), RealVelocity()))

        # Attempt to move the object
        with self.assertRaises(Exception):
            move.move()


if __name__ == '__main__':
    unittest.main()
