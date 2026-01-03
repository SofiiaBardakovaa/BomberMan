import pygame
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

    def update(self):
        pass

    def draw(self, window):
        pygame.draw.rect(window, gs.RED, self.rect)
