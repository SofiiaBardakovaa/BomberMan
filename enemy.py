import pygame
import gamesettings as gs
from random import choice


class Enemy(pygame.sprite.Sprite):
    def __init__(self, game, image_dict, group, row_num, col_num, size):
        super().__init__(group)
        self.GAME = game

        #  Attribs
        self.speed = 1          #  Speed of the enemy
        self.wall_hack = False  #  Enemy can move through walls
        self.chase_player = False   #  Enemy wil chase the player
        self.LoS = 0            #  Distance Enemy can see player
        self.see_player_hack = False    #  Enemy can see player through walls

        #  Level matrix spawn coord
        self.row = row_num
        self.col = col_num

        #  Spawn
        self.size = size
        self.x = self.col * self.size
        self.y = (self.row * self.size) + gs.Y_OFFSET

        self.destroyed = False
        self.direction = "left"
        self.dir_mvmt = {"left": -self.speed, "right": self.speed,
                         "up": -self.speed, "down": self.speed}
        self.change_dir_timer = pygame.time.get_ticks()
        self.dir_time = 1500

        self.index = 0
        self.action = f"walk_{self.direction}"
        self.image_dict = image_dict
        self.anim_frame_time = 100
        self.anim_timer = pygame.time.get_ticks()

        self.image = self.image_dict[self.action][self.index]
        self.rect = self.image.get_rect(topleft=(self.x, self.y))


    def update(self):
        self.movement()
        self.animate()


    def draw(self, window, x_offset):
        window.blit(self.image, (self.rect.x - x_offset, self.rect.y))


    def movement(self):
        """Method that incorporates all movement conditions to enable the enemy to move around
        the game area"""
        if self.destroyed:
            return

        move_direction = self.action.split("_")[1]
        if move_direction in ["left", "right"]:
            self.x += self.dir_mvmt[move_direction]
        else:
            self.y += self.dir_mvmt[move_direction]

        #  reset the directions listing for the char to choose from
        directions = ["left", "right", "up", "down"]

        self.new_direction(self.GAME.groups["hard_block"], move_direction, directions)

        self.new_direction(self.GAME.groups["soft_block"], move_direction, directions)

        self.new_direction(self.GAME.groups["bomb"], move_direction, directions)

        # change of dir is sufficient amount of time's elapsed
        self.check_directions(directions)

        self.rect.update(self.x, self.y, self.size, self.size)

    def collision_detection_blocks(self, group, direction):
        #  collision detection
        for block in group:
            #  compare each block for collision with enemy char rect
            if block.rect.colliderect(self.rect):
                if direction == "left" and self.rect.right > block.rect.right:
                    self.x = block.rect.right
                    return direction
                if direction == "right" and self.rect.left < block.rect.left:
                    self.x = block.rect.left - self.size
                    return direction
                if direction == "up" and self.rect.bottom > block.rect.bottom:
                    self.y = block.rect.bottom
                    return direction
                if direction == "down" and self.rect.top < block.rect.top:
                    self.y = block.rect.top - self.size
                    return direction
        return None

    def new_direction(self, group, move_direction, directions):
        dir = self.collision_detection_blocks(group, move_direction)
        if dir:
            directions.remove(dir)
            new_direction = choice(directions)
            self.action = f"walk_{new_direction}"
            self.change_dir_timer = pygame.time.get_ticks()

    def check_directions(self, direction_list):
        """Randomly change dir after a set amount of time elapsed"""
        if pygame.time.get_ticks() - self.change_dir_timer < self.dir_time:
            return

        if self.x % self.size != 0 or (self.y - gs.Y_OFFSET) % self.size != 0:
            return

        row = int((self.y - gs.Y_OFFSET) // self.size)
        col = int(self.x // self.size)

        #if cell at row\col isn't a 4 way intersection, return
        if row % 2 == 0 or col % 2 == 0:
            return

        self.determine_if_direction_valid(direction_list, row, col)

        #randomly select new direction from remaining dir list
        new_direction = choice(direction_list)
        self.action = f"walk_{new_direction}"

        self.change_dir_timer = pygame.time.get_ticks()
        return

    def determine_if_direction_valid(self, directions, row, col):
        """Check the 4 directions to determine if move is possible"""
        if self.GAME.level_matrix[row - 1][col] != "_":
            directions.remove("up")
        if self.GAME.level_matrix[row + 1][col] != "_":
            directions.remove("down")
        if self.GAME.level_matrix[row][col - 1] != "_":
            directions.remove("left")
        if self.GAME.level_matrix[row][col + 1] != "_":
            directions.remove("right")

        if len(directions) == 0:
            directions.append("left")
        return

    def animate(self):
        """Cycle through the enemy animation images"""
        if pygame.time.get_ticks() - self.anim_timer >= self.anim_frame_time:
            self.index += 1
            if self.destroyed and self.index == len(self.image_dict[self.action]):
                self.kill()
            self.index = self.index % len(self.image_dict[self.action])
            self.image = self.image_dict[self.action][self.index]
            self.anim_timer = pygame.time.get_ticks()

    def destroy(self):
        """Deactivate th enemy when killed"""
        self.destroyed = True
        self.index = 0
        self.action = "death"
        self.image = self.image_dict[self.action][self.index]