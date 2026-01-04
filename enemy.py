import pygame
import gamesettings as gs

class Enemy(pygame.sprite.Sprite):
    def __init__(self, game, image_dict, group, row_num, col_num, size):
        super().__init__(group)
        self.GAME = game

        #attributes
        self.speed = 1
        self.wall_hack = False
        self.chase_player = False
        self.LoS = 0 # Distance enemy can se player
        self.see_player_hack = False

        # level matrix spawn coord
        self.row = row_num
        self.col = col_num

        # spawn
        self.size = size
        self.x = self.col * self.size
        self.y = (self.row * self.size) + gs.Y_OFFSET

        self.destroyed = False
        self.direction = "left"

        self.index = 0
        self.action = f"walk_{self.direction}"
        self.image_dict = image_dict
        self.image = self.image_dict[self.action][self.index]
        self.rect = self.image.get_rect(topleft=(self.x, self.y))

    def update(self):
        pass

    def draw(self, window, x_offset):
        window.blit(self.image, (self.rect.x - x_offset, self.rect.y))
