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

        # power up abilities
        self.power_up_activate = {"bomb_up": self.bomb_up_special, "fire_up": self.fire_up_special,
                                  "speed_up": self.speed_up_special, "wall_hack": self.wall_hack_special,
                                  "remote": self.remote_special, "bomb_pass": self.bomb_hack_special,
                                  "flame_pass": self.flame_pass_special, "invincible": self.invincible_special,
                                  "exit": self.end_stage}

    def update(self):
        if self.GAME.player.rect.collidepoint(self.rect.center):
            # activate power up
            self.power_up_activate[self.name](self.GAME.player)

            if self.name == "exit":
                return

            self.GAME.level_matrix[self.row][self.col] = "_"
            self.kill()
            return

    def draw(self, window, x_offset):
        window.blit(self.image, (self.rect.x - x_offset, self.rect.y))

    def bomb_up_special(self, player):
        """Increase the players bomb limit"""
        player.bomb_limit += 1

    def fire_up_special(self, player):
        """Increase the bombs power"""
        player.power += 1

    def speed_up_special(self, player):
        """Increase the speed of the player"""
        player.speed += 1

    def wall_hack_special(self, player):
        """Turn on the player wall hack"""
        player.wall_hack = True

    def remote_special(self, player):
        player.remote = True

    def bomb_hack_special(self, player):
        """Turn on the bomb hack"""
        player.bomb_hack = True

    def flame_pass_special(self, player):
        """Turn on the ability to ignore bomb blasts"""
        player.flame_pass = True

    def invincible_special(self, player):
        """Turn on th players invincibility"""
        player.invincibility = True
        player.invincibility_timer = pygame.time.get_ticks()

    def end_stage(self, player):
        """End the level and generate a new level"""
        if len(self.GAME.groups["enemies"].sprites()) > 0:
            return

        self.GAME.new_stage()