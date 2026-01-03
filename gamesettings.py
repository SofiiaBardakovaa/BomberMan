from turtledemo.nim import SCREENWIDTH, SCREENHEIGHT

# Game Window Settings
SCREENWIDTH = 1290
SCREENHEIGHT = 892

# Game Frames per Second

FPS = 60

# Colours

BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

# Game Matrix
SIZE = 64

# Sprite coordinates
PLAYER = {"walk_left": [(0, 1), (0, 0), (0, 2)],
          "walk_down": [(0, 4), (0, 3), (0,5)],
          "walk_right": [(0, 7), (0, 6), (0, 8)],
          "walk_up": [(0, 10), (0, 9), (0, 11)],
          "dead_anim": [(1, 0), (1, 1), (1, 2), (1, 3), (1, 4), (1, 5), (1,6)]}