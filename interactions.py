import math
from typing import Set, Optional, List

from vector_2d import Vector, VectorPolar

from characters import Character
from items import Item, Obstacle


class Interaction:
    last_pressed: Optional[Character] = None

    @staticmethod
    def mouse_characters(mouse: Vector, characters: List[Character]) -> Character:
        if Interaction.last_pressed:
            Interaction.last_pressed.set_pressed(False)
        # TODO order the character list positionaly to improve check
        for character in characters:
            # print(abs(mouse - character.pos))
            if abs(mouse - character._pos) < character.radius:
                character.set_pressed(True)
                Interaction.last_pressed = character
                return Interaction.last_pressed

    @staticmethod
    def get_hovered(mouse: Vector, items: Set[Item]) -> Item:
        for item in items:
            if abs(mouse - item._pos) < item.radius:
                return item

    @staticmethod
    def get_new_unit_vectors(vector_polar: VectorPolar, angle: float):
        return (VectorPolar(1, vector_polar.angle + angle).to_cartesian(),
                VectorPolar(1, vector_polar.angle - angle).to_cartesian())

    @staticmethod
    def check_obstacles(characters: List[Character], obstacles: List[Obstacle]):
        increment = angle_addition = 0.39  # pi/8
        for character in characters:
            if abs(character.director_vector):
                for obstacle in obstacles:
                    d = abs(obstacle.pos - character._pos)
                    if d < (obstacle.radius + character.sight_radius):
                        # FIXME que mire posiciones intermedias pues si es pequeño atraviesa
                        while obstacle.is_point_inside(
                                character._pos + character.director_vector.unit() * character.sight_radius):
                            # FIXME si entra es while true por que nada cambia la condicion de entrada
                            # FIxme IMPROVE THSI
                            for vector in Interaction.get_new_unit_vectors(character.director_vector.unit().to_polar(),
                                                                           angle_addition):
                                if not obstacle.is_point_inside(character._pos + vector * character.sight_radius):
                                    character.destination = character._pos + vector * character.sight_radius
                                    character.obstacle = obstacle
                                    return
                            angle_addition += increment
