from abc import ABC

from abs_implementation.implementation import Vector
from abs_implementation.move import Move
from abstracts.rotate import Rotate
from abstracts.vector import Velocity


class RotatableMove(Move, Rotate, ABC):
    def __init__(self, vector: Vector, rotator: Rotate):
        super().__init__(vector)
        self.rotator = rotator

    def move(self):
        new_coords = self.add_velocities_to_coordinates()
        self.vector.move(new_coords)

    def get_new_velocity(self, go_to_velocity: Velocity):
        return self.rotator.get_new_velocity(go_to_velocity)
