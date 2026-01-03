import pygame
from pygame.key import get_pressed

import gamesettings as gs

class Character(pygame.sprite.Sprite):
    def __init__(self, game):
        super().__init__()
        self.GAME = game

        # Character position
        self.x = 0
        self.y = 0

        #Character attributes
        self.alive = True
        self.speed = 3

        # Character Display
        self.image = None
        self.rect = pygame.Rect(self.x, self.y, gs.SIZE, gs.SIZE)

    def input(self):
        for event in pygame.event.get():
            # Check if red cross is clicked
            if event.type == pygame.QUIT:
                self.GAME.MAIN.run = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.GAME.MAIN.run = False

        keys_pressed = pygame.key.get_pressed()
        if keys_pressed[pygame.K_d] or keys_pressed[pygame.K_RIGHT]:
            self.x += self.speed
        elif keys_pressed[pygame.K_a] or keys_pressed[pygame.K_LEFT]:
            self.x -= self.speed
        elif keys_pressed[pygame.K_w] or keys_pressed[pygame.K_UP]:
            self.y -= self.speed
        elif keys_pressed[pygame.K_s] or keys_pressed[pygame.K_DOWN]:
            self.y += self.speed

        # update the character rect position
        self.rect.topleft = (self.x, self.y)

    def update(self):
        pass

    def draw(self, window):
        pygame.draw.rect(window, gs.RED, self.rect)
