from typing import List

from commands.base_command import BaseCommand
from ship import CommandException
from utility.custom_logger import root_logger


class MacroCommand:
    def __init__(self, commands: List[BaseCommand] = None):
        if commands is None:
            self.commands = []
        else:
            self.commands = commands

    def add_command(self, command: BaseCommand):
        self.commands.append(command)

    def execute(self):
        for command in self.commands:
            try:
                command.execute()
            except Exception as e:
                root_logger.exception(e)
                raise CommandException(f"Unable to execute command: {e}")

    def undo(self):
        for command in reversed(self.commands):
            command.undo()
