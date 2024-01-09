import math
from abc import abstractmethod
from dataclasses import dataclass

ANGLE_STEPS = 36000


@dataclass
class Rotate:
    angle: int = 0

    @abstractmethod
    def get_angle(self):
        return self.angle

    @abstractmethod
    def get_new_velocity(self, *args, **kwargs):
        return
