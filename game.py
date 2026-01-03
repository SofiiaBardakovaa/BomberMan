import pygame
from character import Character
import gamesettings as gs

class Game:
    def __init__(self, main, assets):
        # Link with the main class and assets
        self.MAIN = main
        self.ASSETS = assets

        self.player = Character(self, self.ASSETS.player_char)

    def input(self):
        # for event in pygame.event.get():
        #     # Check if red cross is clicked
        #     if event.type == pygame.QUIT:
        #         self.MAIN.run = False
        #     elif event.type == pygame.KEYDOWN:
        #         if event.key == pygame.K_ESCAPE:
        #             self.MAIN.run = False
        self.player.input()

    def update(self):
        self.player.update()

    def draw(self, window):
        self.player.draw(window)
