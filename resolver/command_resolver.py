import json
from typing import Dict, Any, Union

from abs_implementation.implementation import RealPosition, RealVelocity
from abs_implementation.move import Move
from commands.base_command import BaseCommand
from commands.move_command import MoveCommand
from commands.rotate_command import ChangeVelocityCommand
from ship import CommandException
from utility.custom_logger import root_logger

REAL_COMMANDS = {
    "Direct move": MoveCommand,
    "Rotate": ChangeVelocityCommand,
}


class CommandResolver:
    def __init__(self):
        self.objects: Dict[int, Move] = {}

    def resolve_command(
        self, object_id: int, real_command: str, args: dict
    ) -> Union[Any, None]:
        root_logger.info(f"Resolving command: {object_id} {real_command} {args}")
        real_object = self.get_object(object_id)
        if real_object:
            if real_command in REAL_COMMANDS:
                if REAL_COMMANDS[real_command] == MoveCommand:
                    real_position = RealPosition(x=args["x"], y=args["y"])
                    real_object.set_position(real_position)
                else:
                    real_velocity = RealVelocity(
                        x_velocity=args["x_velocity"], y_velocity=args["y_velocity"]
                    )
                    real_object.set_velocity(real_velocity)
                return REAL_COMMANDS[real_command](real_object)
            else:
                root_logger.exception(f"Unknown command: {real_command}")
                raise CommandException(f"Unknown command: {real_command}")
        return

    def add_object(self, object_id, game_object):
        self.objects[object_id] = game_object

    def get_object(self, object_id):
        return self.objects.get(object_id)
