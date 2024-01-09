from dataclasses import dataclass
from math import cos, sin
from typing import Iterable

from abstracts.rotate import Rotate
from abstracts.vector import Position, Velocity


@dataclass
class RealPosition(Position):
    x: float = 0
    y: float = 0

    def __iadd__(self, other):
        self.x += other.x
        self.y += other.y
        return self

    def __add__(self, other) -> Position:
        return RealPosition(self.x + other.x, self.y + other.y)

    def get_position(self) -> (float, float):
        return self.x, self.y


@dataclass
class RealVelocity(Velocity):
    x_velocity: float = 0
    y_velocity: float = 0

    def get_velocity(self):
        return self.x_velocity, self.y_velocity


class RealRotate(Rotate):
    def get_new_velocity(self, current_velocity: RealVelocity) -> RealVelocity:
        return RealVelocity(
            current_velocity.x_velocity * cos(self.angle % 360),
            current_velocity.y_velocity * sin(self.angle % 360)
        )


class Vector:
    def __init__(self, position: Position, velocity: Velocity):
        self.position = position
        self.velocity = velocity

    def set_velocity(self, new_velocity: Velocity):
        self.velocity = new_velocity

    def set_position(self, new_position: Position):
        self.position = new_position

    def get_position(self) -> tuple:
        return self.position.get_position()

    def get_velocity(self) -> tuple:
        return self.velocity.get_velocity()

    def move(self, coords: Iterable) -> None:
        position_class = type(self.position)

        self.set_position(position_class(*coords))
