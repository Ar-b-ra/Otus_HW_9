from abs_implementation.implementation import Vector
from abstracts.vector import Velocity, Position


class Move:
    def __init__(self, vector: Vector):
        self.vector = vector

    def move(self):
        new_coords = self.add_velocities_to_coordinates()
        self.vector.move(new_coords)

    def add_velocities_to_coordinates(self):
        current_position = self.vector.get_position()
        current_velocity = self.vector.get_velocity()
        if len(current_velocity) != len(current_position):
            raise IndexError('Wrong number of coordinates')
        result = list(map(lambda x, y: x + y, current_position, current_velocity))

        return result

    def set_velocity(self, new_velocity: Velocity):
        self.vector.set_velocity(new_velocity)

    def set_position(self, new_position: Position):
        self.vector.set_position(new_position)

    def get_velocity(self):
        return self.vector.get_velocity()

    def get_position(self):
        return self.vector.get_position()
