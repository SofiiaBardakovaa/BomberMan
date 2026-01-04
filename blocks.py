import pygame
import gamesettings as gs

class Blocks(pygame.sprite.Sprite):
    def __init__(self, game, images, group, row_num, col_num, size):
        super().__init__(group)
        self.GAME = game
        self.y_offset = gs.Y_OFFSET

        #Position in level matrix
        self.row = row_num
        self.col = col_num

        # Cell size
        self.size = size

        #Coordinates of Blocks
        self.x = self.col * self.size
        self.y = (self.row * self.size) + self.y_offset

        self.passable = True

        self.image_list = images
        self.image_index = 0
        self.image = self.image_list[self.image_index]
        self.rect = self.image.get_rect(topleft=(self.x, self.y))

    def update(self):
        pass

    def draw(self, window):
        window.blit(self.image, self.rect)

    def __repr__(self):
        return "'#'"

class Hard_Block(Blocks):
    def __init__(self, game, images, group, row_num, col_num, size):
        super().__init__(game, images, group, row_num, col_num, size)

class Soft_Block(Blocks):
    def __init__(self, game, images, group, row_num, col_num, size):
        super().__init__(game, images, group, row_num, col_num, size)
    def __repr__(self):
        return "'@'"