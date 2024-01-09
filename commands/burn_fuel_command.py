from typing import Union

from commands.base_command import BaseCommand
from ship import Ship, CommandException, RotatableShip


class BurnFuelCommand(BaseCommand):
    def __init__(self, ship: Union[RotatableShip, Ship], fuel_amount_to_check: int = 0):
        super().__init__()
        self.ship = ship
        self.fuel_amount_to_burn = fuel_amount_to_check

    def execute(self):
        try:
            self.ship.burn_fuel(self.fuel_amount_to_burn)
        except Exception as e:
            raise CommandException(f"Unable to burn fuel: {e}")

    def undo(self):
        pass
