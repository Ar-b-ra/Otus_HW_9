import unittest

from abs_implementation.implementation import Vector, RealVelocity, RealPosition
from commands.check_fuel_command import CheckFuelCommand
from ship import Ship, CommandException
from utility.custom_logger import root_logger


class CheckFuelTest(unittest.TestCase):
    def setUp(self):
        self.ship = Ship(Vector(RealPosition(1, 2), RealVelocity(3, -4)))

    def test_execute_with_enough_fuel(self):
        command_to_test = CheckFuelCommand(self.ship, 100)
        with self.assertLogs(logger=root_logger) as cm:
            command_to_test.execute()
            self.assertEqual(len(cm.output), 1)
            self.assertIn("Check 100 fuel", cm.output[0])

    def test_execute_with_not_enough_fuel(self):
        command_to_test = CheckFuelCommand(self.ship, 100)
        with self.assertRaises(CommandException), self.assertLogs(logger=root_logger) as cm:
            command_to_test.execute()
            self.assertEqual(len(cm.output), 1)
            self.assertIn("Check 100 fuel", cm.output[0])
            command_to_test = CheckFuelCommand(self.ship, 101)
            command_to_test.execute()


if __name__ == '__main__':
    unittest.main()
