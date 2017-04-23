import pygame
from random import *
from Constants import *
from Pad import *
from Board import *
from Spritesheet import *
from math import *

class Player():
    def __init__(self, pos):
        self.pos = pos
        self.state = STATE_ALIVE
        self.lives = 9

class Game():
    def initialize(self):
        pygame.init()
        pygame.display.set_caption("Game")
        self.screen = pygame.display.set_mode([WINDOW_WIDTH, WINDOW_HEIGHT])
        self.board = Board(self.screen)
        self.screen.fill((0, 0, 0))
        self.framerate = 30
        self.press_tolerance = 0.3
        self.time = 0.0
        self.beat_time = 8.0
        self.player = Player(3)
        self.curr_pad = Pad(self.player.pos)
        self.num_items = 4
        self.clock = pygame.time.Clock()
        self.jumpt = 0

        self.static_sprite = Sprite('static.png', (60, 60), 6, self.screen, self.player, 150)
        self.slash_l_sprite = Sprite('slashLC.png', (90, 90), 4, self.screen, self.player, 225)
        self.jump_r_sprite = Sprite('jumpR.png', (90, 90), 9, self.screen, self.player, 225)
        self.jump_l_sprite = Sprite('jumpR.png', (90, 90), 9, self.screen, self.player, 225, True)
        self.damaged_sprite = Sprite('damage.png', (60, 60), 6, self.screen, self.player, 150)

    def mainloop(self):
        is_running = 1
        self.time += 1
        can_complete = 0
        seq = gen_sequence(self.num_items)
        used = []
        exempt_keys = []
        self.flare_list = []
        bkpos = self.player.pos
        is_intro = 1
        while is_intro:
            pygame.display.update()
            pygame.event.pump()
            self.screen.fill((0, 0, 0))
            bkpos += (self.player.pos - bkpos) / float(self.framerate) * 3.0
            in_time = 0
            self.board.render_background(bkpos, in_time)
            self.board.update_board()
            pressed = pygame.key.get_pressed()
            bkpos += (self.player.pos - bkpos) / float(self.framerate) * 3.0
            self.time += 1
            self.make_tic()
            self.board.render_lives(self.player.lives, (WINDOW_WIDTH - 100, 50))
            pygame.display.flip()
            self.clock.tick(self.framerate)
            if pressed[pygame.K_SPACE]:
                is_intro = False
        self.time = -self.framerate * 5
        while is_running:
            pygame.display.update()
            pygame.event.pump()
            self.screen.fill((0, 0, 0))
            bkpos += float(self.player.pos - bkpos) / self.framerate * 3
            self.time += 1
            self.jumpt += 1
            a = self.time % (float(self.framerate*self.beat_time))
            pressed = pygame.key.get_pressed()
            kdict = self.curr_pad.KEY_DICT
            active_key = kdict[seq[0]]
            boom_key = kdict[5]
            in_time = (a <= self.framerate*self.press_tolerance) or (a >= float(self.framerate*self.beat_time) - self.framerate*self.press_tolerance) # check if is valid
            if in_time:
                #self.screen.fill((30, 30, 30))
                pass
            self.board.render_background(bkpos, in_time)
            for item in exempt_keys:
                if not pressed[item]:
                    exempt_keys.remove(item)
            if pressed[pygame.K_ESCAPE] != 0:
                is_running = 0
                break
            if int(a) == int(self.press_tolerance*self.framerate):# and self.time > self.framerate*self.beat_time:  #
                if self.player.state == STATE_ALIVE:
                    self.ouch()
                seq = gen_sequence(self.num_items)
                self.board.old_slash_list = self.board.slash_list
                self.board.old_slash_alpha = 255
                self.board.slash_list = []
                used = []
                # for item in seq:
                #     try:
                #         self.board.render_slashes(Slash(item, itemprev, self.board, True), False, True)
                #     except:
                #         pass
                #     itemprev = item
                # check whether completed
            self.board.update_board()
            if self.board.old_slash_alpha > 0:
                self.board.render_slashes(None, True)
            if pressed[active_key] != 0 and len(seq) >= 2 and active_key not in exempt_keys:
                exempt_keys.append(active_key)
                used.append(seq[0])
                seq = seq[1:]
                if len(used) > 1:
                    self.board.render_slashes(Slash(used[-2], used[-1], self.board))
                self.player.state = STATE_SLASH_L
                self.slash_l_sprite.curr_frame = 1
                self.flare_list.append(Flare(self.index_to_pos(used[-1]), 50, self.screen, 0.4))
            elif pressed[boom_key] and boom_key not in exempt_keys and active_key == boom_key:
                if self.player.pos == 1 or (self.player.pos != 7 and random() < 0.5):
                    self.player.pos += 1
                    direc = 0
                else:
                    self.player.pos -= 1
                    direc = 1
                self.curr_pad = Pad(self.player.pos)
                if len(used) > 1:
                    self.board.render_slashes(Slash(used[-1], 5, self.board))
                if not direc:
                    self.player.state = STATE_JUMP_R
                    self.jump_r_sprite.curr_frame = 1
                else:
                    self.player.state = STATE_JUMP_L
                    self.jump_l_sprite.curr_frame = 9
                self.jumpt = 0
                self.flare_list.append(Flare(self.index_to_pos(5), 150, self.screen, 1.0))
                if random() < 0.2 and self.num_items < 9:
                    self.num_items += 1
                self.beat_time *=0.95
                self.time = 0
            self.board.render_slashes()
            self.board.make_blue(seq[0])
            self.board.print_seq(seq)
            self.board.print_active(active_key)
            dfade = 2000.0/self.framerate/self.beat_time
            print(dfade)
            self.board.old_slash_alpha -= dfade
            for flare in self.flare_list:
                flare.update()
                if flare.opacity <= 0:
                    self.flare_list.remove(flare)
            self.make_tic()
            self.board.render_lives(self.player.lives, (WINDOW_WIDTH - 100, 50))
            pygame.display.flip()
            self.clock.tick(self.framerate)
            if pressed[pygame.K_ESCAPE]:
                is_running = False
        pygame.quit()

    def ouch(self):
        self.player.lives -= 1
        self.flare_list.append(Flare(self.index_to_pos(8), 300, self.screen, 0.7, True))
        self.player.state = STATE_DAMAGED
        pass

    def make_tic(self):
        tic_speed = int(6.0 * self.framerate / 50.0)
        can_change = (self.player.state != STATE_JUMP_R)
        if self.player.state == STATE_ALIVE and can_change:
            self.static_sprite.tic((800, 480), self.time % tic_speed != 0)
        elif self.player.state == STATE_SLASH_L and can_change:
            self.slash_l_sprite.tic((800, 480), self.time % tic_speed != 0)
        elif self.player.state == STATE_DAMAGED:
            self.damaged_sprite.tic((800, 480), self.time % tic_speed != 0)
        elif self.player.state == STATE_JUMP_R:
            time_total = 1.5 * self.framerate
            amt_thru = self.jumpt/float(time_total)
            ydis = 80
            yoff = max(0, sin(amt_thru * 2 * pi) * ydis)
            self.jump_r_sprite.tic((800, 480 - yoff), self.jumpt % tic_speed != 0)
        elif self.player.state == STATE_JUMP_L:
            time_total = 1.5 * self.framerate
            amt_thru = self.jumpt/float(time_total)
            ydis = 80
            yoff = max(0, sin(amt_thru * 2 * pi) * ydis)
            self.jump_l_sprite.tic((800, 480 - yoff), self.jumpt % tic_speed != 0)

    def index_to_pos(self, ind):
        coord = COORD_DICT[ind]
        x = coord[0]
        y = coord[1]
        xpos = 158 * x + 490
        ypos = 158 * y - 10
        return((xpos, ypos))


if __name__ == "__main__":
    game = Game()
    game.initialize()
    game.mainloop()
