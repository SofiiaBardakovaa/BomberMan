import pygame
import gamesettings as gs

class Special(pygame.sprite.Sprite):
    def __init__(self, game, image, name, group, row_num, col_num, size):
        super().__init__(group)
        self.GAME = game

        self.name = name

        self.row = row_num
        self.col = col_num

        self.size = size
        self.x = self.col * self.size
        self.y = (self.row * self.size) + gs.Y_OFFSET

        self.image = image
        self.rect = self.image.get_rect(topleft=(self.x, self.y))

    def update(self):
        pass

    def draw(self, window, x_offset):
        window.blit(self.image, (self.rect.x - x_offset, self.rect.y))