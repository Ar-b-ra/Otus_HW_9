import unittest

from abs_implementation.implementation import Vector, RealVelocity, RealPosition
from abs_implementation.move import Move
from abstracts.rotate import Rotate
from abstracts.vector import Position, Velocity
from commands.burn_fuel_command import BurnFuelCommand
from commands.check_fuel_command import CheckFuelCommand
from commands.macro_comand import MacroCommand
from commands.move_command import MoveCommand
from commands.rotate_command import ChangeVelocityCommand
from ship import Ship, CommandException, RotatableShip


class CheckRotateCommandTest(unittest.TestCase):
    def setUp(self):
        position = RealPosition()
        velocity = RealVelocity()
        vector = Vector(position, velocity)
        self.ship = Ship(vector)

    def test_execute(self):
        rotatable_ship_to_test = RotatableShip(Vector(RealPosition(1, 2), RealVelocity(3, -4)), Rotate(90))
        fuel_to_burn = 70
        macro_command_with_rotate = MacroCommand()
        macro_command_with_rotate.add_command(CheckFuelCommand(rotatable_ship_to_test, fuel_to_burn))
        macro_command_with_rotate.add_command(ChangeVelocityCommand(rotatable_ship_to_test, 25))
        macro_command_with_rotate.add_command(MoveCommand(rotatable_ship_to_test))
        macro_command_with_rotate.add_command(BurnFuelCommand(rotatable_ship_to_test, fuel_to_burn))
        macro_command_with_rotate.execute()
        self.assertEqual(rotatable_ship_to_test.get_position(), (4, -2))
        self.assertEqual(rotatable_ship_to_test.fuel_level, 30)

    def test_move_object(self):
        self.ship.set_position(RealPosition(12, 5))
        self.ship.set_velocity(RealVelocity(-7, 3))
        self.ship.move()
        self.assertEqual(self.ship.get_position(), (5, 8))

    def test_no_velocity(self):
        with self.assertRaises(CommandException):
            position = RealPosition()
            velocity = Velocity()
            vector = Vector(position, velocity)
            unmovable_ship = Ship(vector)
            command_to_execute = ChangeVelocityCommand(unmovable_ship, 100)
            command_to_execute.execute()

    def test_no_position(self):
        with self.assertRaises(CommandException):
            position = Position()
            velocity = RealVelocity()
            vector = Vector(position, velocity)
            unmovable_ship = Ship(vector)
            command_to_execute = ChangeVelocityCommand(unmovable_ship, 100)
            command_to_execute.execute()

    def test_move_with_immutable_vector(self):
        # Create a mock Vector class with an immutable position
        class ImmutableVector(Vector):

            def __add__(self, other):
                return ImmutableVector(self.x + other.x, self.y + other.y)

            def move(self, coords):
                raise NotImplementedError

        # Create an instance of the Move class with an immutable vector
        ship = Ship(ImmutableVector(RealPosition(), RealVelocity()))

        # Attempt to move the object
        command_to_execute = ChangeVelocityCommand(ship, 100)
        with self.assertRaises(CommandException):
            command_to_execute.execute()


if __name__ == '__main__':
    unittest.main()
