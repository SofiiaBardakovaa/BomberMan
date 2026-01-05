import pygame
from character import Character
from enemy import Enemy
from blocks import Hard_Block, Soft_Block, Special_Soft_Block
from random import choice, randint
import gamesettings as gs


class Game:
    def __init__(self, main, assets):
        #  Link with the main class and assets
        self.MAIN = main
        self.ASSETS = assets

        #  Camera Offset
        self.camera_x_offset = 0

        #  Groups
        self.groups = {"hard_block": pygame.sprite.Group(),
                       "soft_block": pygame.sprite.Group(),
                       "bomb": pygame.sprite.Group(),
                       "specials": pygame.sprite.Group(),
                       "explosions": pygame.sprite.Group(),
                       "enemies": pygame.sprite.Group(),
                       "player": pygame.sprite.Group()}

        self.player = Character(self, self.ASSETS.player_char, self.groups["player"], 3, 2, gs.SIZE)

        self.level = 1
        self.level_special = self.select_a_special()
        self.level_matrix = self.generate_level_matrix(gs.ROWS, gs.COLS)


    def input(self):
        self.player.input()


    def update(self):
        for value in self.groups.values():
            for item in value:
                item.update()

        # Perform enemy collision check with explosions
        if self.groups["explosions"]:
            killed_enemies = pygame.sprite.groupcollide(self.groups["explosions"], self.groups["enemies"], False, False)
            if killed_enemies:
                for flame, enemies in killed_enemies.items():
                    for enemy in enemies:
                        if pygame.sprite.collide_mask(flame, enemy):
                            enemy.destroy()


    def draw(self, window):
        window.fill(gs.GREY)

        for row_num, row in enumerate(self.level_matrix):
            for col_num, col in enumerate(row):
                window.blit(self.ASSETS.background["background"][0],
                            ((col_num * gs.SIZE) - self.camera_x_offset, (row_num * gs.SIZE) + gs.Y_OFFSET))

        for value in self.groups.values():
            for item in value:
                item.draw(window, self.camera_x_offset)


    def generate_level_matrix(self, rows, cols):
        """Generate the basic level matrix"""
        matrix = []
        for row in range(rows + 1):
            line = []
            for col in range(cols + 1):
                line.append("_")
            matrix.append(line)
        self.insert_hard_blocks_into_matrix(matrix)
        self.insert_soft_blocks_into_matrix(matrix)
        self.insert_power_up_into_matrix(matrix, self.level_special)
        self.insert_power_up_into_matrix(matrix, "exit")
        self.insert_enemies_into_level(matrix)
        for row in matrix:
            print(row)
        return matrix


    def insert_hard_blocks_into_matrix(self, matrix):
        """Inserts all the hard blocks into the level matrix"""
        for row_num, row in enumerate(matrix):
            for col_num, col in enumerate(row):
                if row_num == 0 or row_num == len(matrix)-1 or \
                    col_num == 0 or col_num == len(row)-1 or \
                        (row_num % 2 == 0 and col_num % 2 == 0):
                    matrix[row_num][col_num] = Hard_Block(self, self.ASSETS.hard_block["hard_block"],
                                                          self.groups["hard_block"], row_num, col_num, gs.SIZE)
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
                        cell = Soft_Block(self, self.ASSETS.soft_block["soft_block"],
                                          self.groups["soft_block"], row_num, col_num, gs.SIZE)
                    matrix[row_num][col_num] = cell
        return


    def insert_power_up_into_matrix(self, matrix, special):
        """Randomly insert the special Block into the level matrix"""
        power_up = special
        valid = False
        while not valid:
            row = randint(0, gs.ROWS)
            col = randint(0, gs.COLS)
            if row == 0 or row == len(matrix) - 1 or col == 0 or col == len(matrix[0]) - 1:
                continue
            elif row % 2 == 0 and col % 2 == 0:
                continue
            elif row in [2, 3, 4] and col in [1, 2, 3]:
                continue
            elif matrix[row][col] != "_":
                continue
            else:
                valid = True
        cell = Special_Soft_Block(self,
                                  self.ASSETS.soft_block["soft_block"],
                                  self.groups["soft_block"],
                                  row, col, gs.SIZE, power_up)
        matrix[row][col] = cell


    def update_x_camera_offset_player_position(self, player_x_pos):
        """Updates the camera x position per the player x position"""
        if player_x_pos >= 576 and player_x_pos <= 1280:
            self.camera_x_offset = player_x_pos - 576


    def insert_enemies_into_level(self, matrix):
        """Randomly insert enemies into the level, using level matrix for valid locations"""
        enemies_list = self.select_enemies_to_spawn()
        print(enemies_list)

        pl_col = self.player.col_num
        pl_row = self.player.row_num

        #  Load in the enemies
        for enemy in enemies_list:
            valid_choice = False
            while not valid_choice:
                row = randint(0, gs.ROWS)
                col = randint(0, gs.COLS)

                #  Check if this row/col within 3 blocks of the player
                if row in [pl_row-3, pl_row-2, pl_row-1, pl_row, pl_row+1, pl_row+2, pl_row+3] and \
                    col in [pl_col-3, pl_col-2, pl_col-1, pl_col, pl_col+1, pl_col+2, pl_col+3]:
                    continue

                elif matrix[row][col] == "_":
                    valid_choice = True
                    Enemy(self, self.ASSETS.enemies[enemy], self.groups["enemies"], enemy, row, col, gs.SIZE)
                else:
                    continue


    def regenerate_stage(self):
        """Restart a stage/level"""
        for key in self.groups.keys():
            if key == "player":
                continue
            self.groups[key].empty()

        self.level_matrix.clear()
        self.level_matrix = self.generate_level_matrix(gs.ROWS, gs.COLS)

        self.camera_x_offset = 0


    def select_enemies_to_spawn(self):
        """Generate a list of enemies to spawn"""
        enemies_list = []
        enemies = {0: "ballom", 1: "ballom", 2: "onil", 3: "dahl", 4: "minvo", 5: "doria",
                   6: "ovape", 7: "pass", 8: "pontan"}

        if self.level <= 8:
            self.add_enemies_to_list(8, 2, 0, enemies, enemies_list)
        elif self.level <= 17:
            self.add_enemies_to_list(7, 2, 1, enemies, enemies_list)
        elif self.level <= 26:
            self.add_enemies_to_list(6, 3, 1, enemies, enemies_list)
        elif self.level <= 35:
            self.add_enemies_to_list(5, 3, 2, enemies, enemies_list)
        elif self.level <= 45:
            self.add_enemies_to_list(4, 4, 2, enemies, enemies_list)
        else:
            self.add_enemies_to_list(3, 4, 4, enemies, enemies_list)
        return enemies_list


    def add_enemies_to_list(self, num_1, num_2, num_3, enemies, enemies_list):
        for num in range(num_1):
            enemies_list.append("ballom")
        for num in range(num_2):
            enemies_list.append(enemies[(self.level % 9)])
        for num in range(num_3):
            enemies_list.append(choice(list(enemies.values())))
        return


    def select_a_special(self):
        specials = list(gs.SPECIALS.keys())
        specials.remove("exit")
        if self.level == 4:
            power_up = "speed_up"
        elif self.level == 1:
            power_up = "bomb_up"
        elif self.player.bomb_limit <= 2 or self.player.power <= 2:
            power_up = choice(["bomb_up", "fire_up"])
        else:
            if self.player.wall_hack:
                specials.remove("wall_hack")
            if self.player.remote_detonate:
                specials.remove("remote")
            if self.player.bomb_hack:
                specials.remove("bomb_pass")
            if self.player.flame_hack:
                specials.remove("flame_pass")
            if self.player.bomb_limit == 10:
                specials.remove("bomb_up")
            if self.player.power == 10:
                specials.remove("fire_up")
            power_up = choice(specials)
        return power_up

    def new_stage(self):
        """Increases the stage level num and selects a new level special"""
        self.level += 1
        self.level_special = self.select_a_special()
        self.player.set_player_position()
        self.player.set_player_images()
        self.regenerate_stage()
        print(self.level)