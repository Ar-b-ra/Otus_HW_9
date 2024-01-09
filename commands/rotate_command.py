from commands.base_command import BaseCommand
from ship import Ship, RotatableShip, CommandException
from utility.custom_logger import root_logger


class ChangeVelocityCommand(BaseCommand):
    def __init__(self, ship: RotatableShip, angle: int = 0):
        super().__init__()
        self.ship = ship
        self.angle = angle

    def execute(self):
        try:
            return self.ship.rotate(self.angle)
        except Exception as e:
            root_logger.exception(f"Unable to change velocity: {e}")
            raise CommandException(f"Unable to change velocity: {e}")

    def undo(self):
        pass
