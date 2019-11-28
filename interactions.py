import math
from typing import Set, Optional, List

from vector_2d import Vector, VectorPolar

from characters import Character
from items import Item, Obstacle


class Interaction:
    last_pressed: Optional[Character] = None

    @staticmethod
    def mouse_characters(mouse: Vector, characters: Set[Character]) -> Character:
        if Interaction.last_pressed:
            Interaction.last_pressed.set_pressed(False)
        # TODO order the character list positionaly to improve check
        for character in characters:
            # print(abs(mouse - character.pos))
            if abs(mouse - character.pos) < character.radius:
                character.set_pressed(True)
                Interaction.last_pressed = character
                return Interaction.last_pressed

    @staticmethod
    def get_hovered(mouse: Vector, items: Set[Item]) -> Item:
        for item in items:
            if abs(mouse - item.pos) < item.radius:
                return item

    @staticmethod
    def get_new_unit_vectors(vector_polar: VectorPolar, angle: float):
        return (VectorPolar(1, vector_polar.angle + angle).to_cartesian(),
                VectorPolar(1, vector_polar.angle - angle).to_cartesian())

    @staticmethod
    def check_obstacles(characters: List[Character], obstacles: List[Obstacle]):
        angle_addition = math.pi / 16
        for character in characters:
            if character.director_vector:
                for obstacle in obstacles:
                    d = abs(obstacle.pos - character.pos)
                    if d < (obstacle.radius + character.sight_radius):
                        # FIXME que mire posiciones intermedias pues si es pequeño atraviesa
                        future_pos = character.pos + character.director_vector.unit() * character.sight_radius
                        if obstacle.is_point_inside(future_pos):
                            # FIxme IMPROVE THSI
                            salir = False
                            polar_unit_dir_vector = character.director_vector.unit().to_polar()
                            while not salir:
                                right, left = Interaction.get_new_unit_vectors(polar_unit_dir_vector, angle_addition)
                                if not obstacle.is_point_inside(character.pos + right * character.sight_radius):
                                    character.destination = character.pos + right * character.sight_radius
                                    salir = True
                                elif not obstacle.is_point_inside(character.pos + left * character.sight_radius):
                                    character.destination = character.pos + left * character.sight_radius
                                    salir = True
                                else:
                                    angle_addition += math.pi / 16
