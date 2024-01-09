from typing import Union

from commands.base_command import BaseCommand
from ship import Ship, RotatableShip, CommandException
from utility.custom_logger import root_logger


class MoveCommand(BaseCommand):
    def __init__(self, ship: Union[RotatableShip, Ship]):
        super().__init__()
        self.ship = ship

    def execute(self):
        try:
            return self.ship.move()
        except CommandException as e:
            root_logger.exception(f"Unable to change velocity: {e}")

    def undo(self):
        pass
