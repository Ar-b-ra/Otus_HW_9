from abc import abstractmethod


class BaseCommand:
    def __init__(self, *args, **kwargs):
        pass

    @abstractmethod
    def execute(self):
        pass

    @abstractmethod
    def undo(self):
        pass

