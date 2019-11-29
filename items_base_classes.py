import abc

from vector_2d import Vector


class Collective:
    def move(self, vector: Vector):
        for element in self:
            element.pos_increment(vector)

    @abc.abstractmethod
    def __iter__(self):
        ...

    @abc.abstractmethod
    def __add__(self, other):
        ...

    @abc.abstractmethod
    def __radd__(self, other):
        ...
