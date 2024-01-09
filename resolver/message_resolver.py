import json
from typing import Union

from commands.base_command import BaseCommand
from resolver.command_resolver import CommandResolver
from utility.custom_logger import root_logger

OPERATIONS = {
    1: "Direct move",
    2: "Rotate",
}


class MessageResolver:
    def __init__(self, command_resolver: CommandResolver):
        self.command_resolver = command_resolver

    def resolve(self, message: Union[bytes, str]) -> BaseCommand:
        root_logger.debug(message)
        request = json.loads(message)
        game_id = request.get("game_id")  # TODO: create game object, to implement
        object_id = request.get("object_id")
        operation_id = request.get("operation_id")
        real_command = OPERATIONS.get(operation_id)
        if real_command:
            args = request.get("args")
            if args:
                dict_args = json.loads(args)
            else:
                dict_args = {}
            return self.command_resolver.resolve_command(
                object_id, real_command, dict_args
            )
