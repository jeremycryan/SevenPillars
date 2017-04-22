import pygame
from random import *
from Constants import *
from Pad import *
from Board import *

class Player():
    def __init__(self, pos):
        self.pos = pos
        self.state = STATE_ALIVE

class Game():
    def initialize(self):
        pygame.init()
        pygame.display.set_caption("Game")
        self.screen = pygame.display.set_mode([WINDOW_WIDTH, WINDOW_HEIGHT])
        self.board = Board(self.screen)
        self.screen.fill((0, 0, 0))
        self.framerate = 50
        self.press_tolerance = 0.3
        self.time = 0
        self.beat_time = 8
        self.player = Player(3)
        self.curr_pad = Pad(self.player.pos)
        self.num_items = 4
        self.clock = pygame.time.Clock()

    def mainloop(self):
        is_running = 1
        self.time += 1
        can_complete = 0
        seq = gen_sequence(self.num_items)
        used = []
        exempt_keys = []
        bkpos = self.player.pos
        while is_running:
            pygame.display.update()
            pygame.event.pump()
            self.screen.fill((0, 0, 0))
            bkpos += (self.player.pos - bkpos) / self.framerate
            self.time += 1
            a = self.time%(self.framerate*self.beat_time)
            pressed = pygame.key.get_pressed()
            kdict = self.curr_pad.KEY_DICT
            active_key = kdict[seq[0]]
            boom_key = kdict[5]
            in_time = (a <= self.framerate*self.press_tolerance) or (a >= self.framerate*self.beat_time - self.framerate*self.press_tolerance) # check if is valid
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
                seq = gen_sequence(self.num_items)
                self.board.old_slash_list = self.board.slash_list
                self.board.old_slash_alpha = 255
                self.board.slash_list = []
                used = []
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
            elif in_time and pressed[boom_key] and boom_key not in exempt_keys and active_key == boom_key:
                if self.player.pos == 1 or (self.player.pos != 7 and random() < 0.5):
                    self.player.pos += 1
                else:
                    self.player.pos -= 1
                self.curr_pad = Pad(self.player.pos)
                if len(used) > 1:
                    self.board.render_slashes(Slash(used[-1], 5, self.board))
            else:
                self.board.render_slashes()
            self.board.print_seq(seq)
            self.board.print_active(active_key)
            dfade = 800/self.framerate/self.beat_time
            self.board.old_slash_alpha -= dfade
            pygame.display.flip()
            self.clock.tick(self.framerate)

if __name__ == "__main__":
    game = Game()
    game.initialize()
    game.mainloop()
