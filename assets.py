import pygame
import gamesettings as gs

class Assets:
    def __init__(self):
        self.spritesheet = self.load_sprite_sheet("images", "spritesheet.png", 192*4, 272*4)

        self.player_char = self.load_sprite_range(gs.PLAYER, self.spritesheet)
        self.hard_block = self.load_sprite_range(gs.HARD_BLOCK, self.spritesheet)
        self.soft_block = self.load_sprite_range(gs.SOFT_BLOCK, self.spritesheet)
        self.background = self.load_sprite_range(gs.BACKGROUND, self.spritesheet)
        self.bomb = self.load_sprite_range(gs.BOMB, self.spritesheet)

    def load_sprite_sheet(self, path, filename, width, height):
        """Load in the sprite sheet image and resize it"""
        image = pygame.image.load(f"{path}/{filename}").convert_alpha()
        image = pygame.transform.scale(image, (width, height))
        return image

    def load_sprites(self, spritesheet, xcoord, ycoord, width, height):
        """Load an individual sprite image"""
        image = pygame.Surface((width, height))
        image.fill((0, 0, 1))
        image.blit(spritesheet, (0, 0), (xcoord, ycoord, width, height))
        image.set_colorkey(gs.BLACK)
        return image

    def load_sprite_range(self, image_dict, spritesheet, row = gs.SIZE, col = gs.SIZE, width = gs.SIZE, height = gs.SIZE, resize = False):
        """Return a dict containing lists of images for the animations"""
        animation_images = {}
        for animation in image_dict.keys():
            animation_images[animation] = []
            for coord in image_dict[animation]:
                image = self.load_sprites(spritesheet, coord[1] * col, coord[0] * row, width, height)
                if resize:
                    image = pygame.transform.scale(image, (32, 32))
                animation_images[animation].append(image)
        return animation_images

