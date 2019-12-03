import pygame

shovel = (  # sized 24x16
    "  XXXXXX                ",
    "X........X              ",
    "X.........X             ",
    "X..........X            ",
    "  X........X            ",
    "   X XX..X              ",
    "       X..X             ",
    "        X..X            ",
    "         X..X           ",
    "          X..X          ",
    "           X..X         ",
    "            X..X        ",
    "             X..X       ",
    "              X...X     ",
    "              X.XX.X    ",
    "                X       ",
)

axe = (  # sized 24x16
    "        XX              ",
    "       X..X             ",
    "      X....X            ",
    "     X......X           ",
    "    X........X          ",
    "   X..........X         ",
    "  X........XX..X        ",
    "   X......X  X..X       ",
    "    X....X    X..X      ",
    "     X..X      X..X     ",
    "      X         X..X    ",
    "                 X..X   ",
    "                  X..X  ",
    "                   X..X ",
    "                    X..X",
    "                      X ",
)
pick = (  # sized 24x16
    "        XXXXXXXXX       ",
    "   XXXXX....XXX         ",
    "   X..X...XX            ",
    "   XX...XX              ",
    "  X....X                ",
    " X...XX.X               ",
    "X....XX..X              ",
    "X...X  X..X             ",
    "X..X    X..X            ",
    "X.X      X..X           ",
    "X         X..X          ",
    "X          X..X         ",
    "            X..X        ",
    "             X..X       ",
    "              X..X      ",
    "               X..X     ",
)

compiled_shovel = ((24, 16), (0, 0), *pygame.cursors.compile(shovel, 'X', '.'))
compiled_axe = ((24, 16), (0, 0), *pygame.cursors.compile(axe, 'X', '.'))
compiled_pick = ((24, 16), (0, 0), *pygame.cursors.compile(pick, 'X', '.'))
