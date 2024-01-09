from typing import Union

from commands.base_command import BaseCommand
from ship import Ship, CommandException, RotatableShip
from utility.custom_logger import root_logger


class CheckFuelCommand(BaseCommand):
    def __init__(self, ship: Union[RotatableShip, Ship], fuel_amount_to_check: int = 0):
        super().__init__()
        self.ship = ship
        self.fuel_amount_to_check = fuel_amount_to_check

    def execute(self):
        root_logger.info(f"Check {self.ship.fuel_level} fuel")
        if not self.ship.check_fuel(self.fuel_amount_to_check):
            raise CommandException(f"Not enough fuel for this command")

    def undo(self):
        pass
