from abc import abstractmethod
from dataclasses import dataclass


@dataclass
class Position:

    @abstractmethod
    def get_position(self) -> tuple:
        raise NotImplementedError


@dataclass
class Velocity:

    @abstractmethod
    def get_velocity(self) -> tuple:
        raise NotImplementedError



