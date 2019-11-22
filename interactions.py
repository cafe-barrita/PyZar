from typing import Set

from vector_2d import Vector

from characters import Character

radius = 5


def mouse_characters(mouse: Vector, characters: Set[Character]) -> Character:
    someone_pressed = False
    retorno = None
    for character in characters:
        character.set_pressed(False)
        print(abs(mouse - character.pos))
        if not someone_pressed and abs(mouse - character.pos) < radius:
            character.set_pressed(True)
            retorno = character
            someone_pressed = True

    return retorno
