import pygame
from character import Character
from blocks import Hard_Block, Soft_Block
from random import choice
import gamesettings as gs

class Game:
    def __init__(self, main, assets):
        # Link with the main class and assets
        self.MAIN = main
        self.ASSETS = assets

        #Camera offset
        self.camera_x_offset = 0

        # self.player = Character(self, self.ASSETS.player_char)

        #Groups
        # self.hard_blocks = pygame.sprite.Group()
        # self.soft_blocks = pygame.sprite.Group()
        self.groups = {"hard_block": pygame.sprite.Group(),
                       "soft_block": pygame.sprite.Group(),
                       "bomb": pygame.sprite.Group(),
                       "player": pygame.sprite.Group()}

        self.player = Character(self, self.ASSETS.player_char, self.groups["player"], 3, 2, gs.SIZE)

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
        #self.hard_blocks.update()
        #self.soft_blocks.update()
        #self.player.update()
        for value in self.groups.values():
            for item in value:
                item.update()

    def draw(self, window):
        window.fill(gs.GREY)
        for row_num, row in enumerate(self.level_matrix):
            for col_num, col in enumerate(row):
                window.blit(self.ASSETS.background["background"][0],
                            ((col_num * gs.SIZE) - self.camera_x_offset, (row_num * gs.SIZE) + gs.Y_OFFSET))
        # self.hard_blocks.draw(window)
        # self.soft_blocks.draw(window)
        # self.player.draw(window)
        for value in self.groups.values():
            for item in value:
                item.draw(window, self.camera_x_offset)

    def generate_level_matrix(self, rows, cols):
        """Generate the basic level matrix"""
        matrix = []
        for row in range(rows + 1):
            line = []
            for col in range(cols +1):
                line.append("_")
            matrix.append(line)
        self.insert_hard_blocks_into_matrix(matrix)
        self.insert_soft_blocks_into_matrix(matrix)
        for row in matrix:
            print(row)
        print()
        return matrix

    def insert_hard_blocks_into_matrix(self, matrix):
        """Insert all the Hard Barrier Blocks into the level matrix"""
        for row_num, row in enumerate(matrix):
            for col_num, col in enumerate(row):
                if row_num == 0 or row_num == len(matrix)-1 or \
                        col_num == 0 or col_num == len(row)-1 or \
                        (row_num % 2 == 0 and col_num % 2 == 0):
                    matrix[row_num][col_num] = Hard_Block(self, self.ASSETS.hard_block["hard_block"], self.groups["hard_block"], row_num, col_num, gs.SIZE)
        return

    def insert_soft_blocks_into_matrix(self, matrix):
        """Randomly insert soft blocks into the level matrix"""
        for row_num, row in enumerate(matrix):
            for col_num, col in enumerate(row):
                if row_num == 0 or row_num == len(matrix) - 1 or \
                        col_num == 0 or col_num == len(row) - 1 or \
                        (row_num % 2 == 0 and col_num % 2 == 0):
                    continue
                elif row_num in [2, 3, 4] and col_num in [1, 2, 3]:
                    continue
                else:
                    cell = choice(["@", "_", "_", "_"])
                    if cell == "@":
                        cell = Soft_Block(self, self.ASSETS.soft_block["soft_block"], self.groups["soft_block"], row_num, col_num, gs.SIZE)
                    matrix[row_num][col_num] = cell
        return

    def update_x_camera_offset_player_position(self, player_x_pos):
        """Updates the camera x position per the player x position"""
        if player_x_pos >= 576 and player_x_pos <= 1280:
            self.camera_x_offset = player_x_pos - 576