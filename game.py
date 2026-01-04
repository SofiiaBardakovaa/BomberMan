import pygame
from character import Character
from blocks import Hard_Block
import gamesettings as gs

class Game:
    def __init__(self, main, assets):
        # Link with the main class and assets
        self.MAIN = main
        self.ASSETS = assets

        self.player = Character(self, self.ASSETS.player_char)

        #Groups
        self.hard_blocks = pygame.sprite.Group()

        #Level Information
        self.level = 1
        self.level_matrix = self.generate_level_matrix(gs.ROWS, gs.COLS)


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
        self.hard_blocks.update()
        self.player.update()

    def draw(self, window):
        self.hard_blocks.draw(window)
        self.player.draw(window)

    def generate_level_matrix(self, rows, cols):
        """Generate the basic level matrix"""
        matrix = []
        for row in range(rows + 1):
            line = []
            for col in range(cols +1):
                line.append("_")
            matrix.append(line)
        self.insert_hard_blocks_into_matrix(matrix)
        for row in matrix:
            print(row)
        return matrix

    def insert_hard_blocks_into_matrix(self, matrix):
        """Insert all the Hard Barrier Blocks into the level matrix"""
        for row_num, row in enumerate(matrix):
            for col_num, col in enumerate(row):
                if row_num == 0 or row_num == len(matrix)-1 or col_num == 0 or col_num == len(row)-1 or (row_num % 2 == 0 and col_num % 2 == 0):
                    matrix[row_num][col_num] = Hard_Block(self, self.ASSETS.hard_block["hard_block"], self.hard_blocks, row_num, col_num, gs.SIZE)
        return

