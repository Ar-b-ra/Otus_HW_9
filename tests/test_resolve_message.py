import json
import unittest
from abs_implementation.implementation import (
    Vector,
    RealVelocity,
    RealPosition,
    RealRotate,
)
from commands.move_command import MoveCommand
from commands.rotate_command import ChangeVelocityCommand
from resolver.command_resolver import CommandResolver
from resolver.message_resolver import MessageResolver
from ship import Ship, RotatableShip


class TestResolve(unittest.TestCase):
    def setUp(self):
        self.command_resolver = CommandResolver()
        self.message_resolver = MessageResolver(self.command_resolver)
        position = RealPosition()
        velocity = RealVelocity()
        vector = Vector(position, velocity)
        ship = Ship(vector)
        self.command_resolver.add_object(1, ship)
        angle = 30
        ship = RotatableShip(Vector(RealPosition(), RealVelocity()), RealRotate(angle))
        self.command_resolver.add_object(2, ship)

        # self.message_resolver.command_resolver = self.mock_command_resolver

    def test_resolve_with_change_velocity_command(self):
        args = {"x_velocity": 2, "y_velocity": 3}
        message = json.dumps(
            {"game_id": 1, "object_id": 2, "operation_id": 2, "args": json.dumps(args)}
        )
        result = self.message_resolver.resolve(message)
        self.assertTrue(isinstance(result, ChangeVelocityCommand))

    def test_resolve_with_move_command(self):
        args = {"x": 2, "y": 3}
        message = json.dumps(
            {"game_id": 1, "object_id": 1, "operation_id": 1, "args": json.dumps(args)}
        )
        result = self.message_resolver.resolve(message)
        self.assertTrue(isinstance(result, MoveCommand))

    def test_resolve_with_incorrect_command(self):
        args = {}
        message = json.dumps(
            {"game_id": 1, "object_id": 1, "operation_id": -1, "args": json.dumps(args)}
        )
        result = self.message_resolver.resolve(message)
        self.assertIsNone(result)

    def test_resolve_with_incorrect_object(self):
        args = {}
        message = json.dumps(
            {"game_id": 1, "object_id": -1, "operation_id": 1, "args": json.dumps(args)}
        )
        result = self.message_resolver.resolve(message)
        self.assertIsNone(result)


if __name__ == "__main__":
    unittest.main()
