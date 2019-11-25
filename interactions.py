from typing import Set, Optional

from vector_2d import Vector

from characters import Character
from items import Item


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
