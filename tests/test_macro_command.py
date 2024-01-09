import unittest
from unittest.mock import MagicMock

from abs_implementation.implementation import RealPosition, RealVelocity, Vector
from commands.burn_fuel_command import BurnFuelCommand
from commands.check_fuel_command import CheckFuelCommand
from commands.macro_comand import MacroCommand
from commands.move_command import MoveCommand
from ship import Ship, CommandException


class TestExecute(unittest.TestCase):
    def setUp(self):
        self.ship = Ship(Vector(RealPosition(1, 2), RealVelocity(3, -4)))

    def test_check_fuel_with_valid_amount(self):
        # Arrange
        fuel_to_burn = 70
        macro_command = MacroCommand()
        macro_command.add_command(CheckFuelCommand(self.ship, fuel_to_burn))
        macro_command.add_command(MoveCommand(self.ship))
        macro_command.add_command(BurnFuelCommand(self.ship, fuel_to_burn))

        macro_command.execute()

        # Assert
        self.assertEqual(self.ship.get_position(), (4, -2))

    def test_check_fuel_with_invalid_amount(self):
        fuel_to_burn = 70
        macro_command = MacroCommand()
        macro_command.add_command(CheckFuelCommand(self.ship, fuel_to_burn))
        macro_command.add_command(MoveCommand(self.ship))
        macro_command.add_command(BurnFuelCommand(self.ship, fuel_to_burn))
        macro_command.add_command(BurnFuelCommand(self.ship, fuel_to_burn))

        with self.assertRaises(CommandException) as cm:
            macro_command.execute()
        self.assertEqual(str(cm.exception), "Unable to execute command: Unable to burn fuel: Not enough fuel for burn")
        self.assertEqual(self.ship.get_position(), (4, -2))
        self.assertEqual(self.ship.fuel_level, 30)
