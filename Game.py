import pygame
from random import *
from Constants import *
from Pad import *
from Board import *
from Spritesheet import *
from math import *
import os

class Player():
    def __init__(self, pos):
        self.pos = pos
        self.state = STATE_ALIVE
        self.lives = 9

class Game():
    def initialize(self):
        pygame.init()
        pygame.mixer.init()
        pygame.mixer.music.load(os.path.join('ambience2.wav'))
        pygame.mixer.music.play(-1)
        pygame.display.set_caption("Seven Pillars")
        self.screen = pygame.display.set_mode([WINDOW_WIDTH, WINDOW_HEIGHT])
        self.board = Board(self.screen)
        self.screen.fill((0, 0, 0))
        self.framerate = 20
        self.press_tolerance = 0.3
        self.time = 0.0
        self.beat_time = 15
        self.player = Player(1)
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
        self.first = 1
        is_running = 1
        self.time += 1
        can_complete = 0
        seq = gen_sequence(self.num_items)
        used = []
        exempt_keys = []
        self.flare_list = []
        bkpos = self.player.pos
        self.space_to_start = pygame.image.load(os.path.join('space_to_start.png')).convert_alpha()
        self.space_to_start = pygame.transform.scale(self.space_to_start, (330, 30))
        is_intro = 1
        intro_t = 0
        inst_up = True
        inst2_up = False
        while is_intro:
            intro_t += 1
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
            self.screen.blit(self.board.logo, (500, 130 + 20*sin(intro_t * self.framerate * 0.003)))
            self.make_tic()
            self.board.render_lives(self.player.lives, (WINDOW_WIDTH/2 - 218, 50))
            if self.time % self.framerate < self.framerate / 2 and self.first:
                self.screen.blit(self.space_to_start, (642, 15))
            pygame.display.flip()
            self.clock.tick(self.framerate)
            if pressed[pygame.K_SPACE]:
                is_intro = False
        self.time = -self.framerate * 5
        self.is_vulnerable = 0
        ref = intro_t
        num_complete = 0
        self.inst_t = 0
        self.inst2_t = 0
        inst_text_1 = pygame.image.load(os.path.join('inst_1.png')).convert_alpha()
        inst_text_2 = pygame.image.load(os.path.join('inst_2.png')).convert_alpha()
        inst_text_1 = pygame.transform.scale(inst_text_1, (450, 500))
        inst_text_2 = pygame.transform.scale(inst_text_2, (450, 500))
        self.time_dead = 0
        while is_running:
            pygame.display.update()
            pygame.event.pump()
            self.screen.fill((0, 0, 0))
            bkpos += float(self.player.pos - bkpos) / self.framerate * 3
            self.time += 1
            intro_t += 1
            if self.inst_t < self.framerate and inst_up == True:
                self.inst_t += 1
            elif self.inst_t > 0 and inst_up == False:
                self.inst_t -= 1
            if self.inst2_t < self.framerate and inst2_up == True:
                self.inst2_t += 1
            elif self.inst2_t > 0 and inst2_up == False:
                self.inst2_t -= 1
            self.jumpt += 1
            a = self.time % (float(self.framerate*self.beat_time))
            pressed = pygame.key.get_pressed()
            kdict = self.curr_pad.KEY_DICT
            active_key = kdict[seq[0]]
            boom_key = kdict[5]
            closeness = a/(self.beat_time * self.framerate)
            if self.is_vulnerable:
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
            if int(a) == int(self.press_tolerance*self.framerate) and self.is_vulnerable:# and self.time > self.framerate*self.beat_time:  #
                if self.player.state != STATE_JUMP_R and self.player.state != STATE_JUMP_L:
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
                self.beat_time *=0.93
                self.time = 0
                num_complete += 1
                if num_complete == 1:
                    inst2_up = True
                if num_complete == 2:
                    inst2_up = False
            if num_complete >= 1:
                self.is_vulnerable = 1
                inst_up = False
            self.board.render_slashes()
            self.board.make_blue(seq[0])
            # self.board.print_seq(seq)
            # self.board.print_active(active_key)
            dfade = 2000.0/self.framerate/self.beat_time
            self.board.old_slash_alpha -= dfade
            for flare in self.flare_list:
                flare.update()
                if flare.opacity <= 0:
                    self.flare_list.remove(flare)
            if self.is_vulnerable:
                self.board.render_washout(closeness**3 * 0.5)
            if self.player.lives == 0:
                self.player.state = STATE_DEAD
            if inst2_up and self.first:
                inst_up = 0
                s = pygame.Surface((440, 490))
                s.set_alpha(128)
                s.fill((255,255,255))
                self.screen.blit(s, (70, 170))
                self.screen.blit(inst_text_2, (70, 150))
            if inst_up and self.first:
                s = pygame.Surface((440, 490))
                s.set_alpha(128)
                s.fill((255,255,255))
                self.screen.blit(s, (70, 170))
                self.screen.blit(inst_text_1, (70, 150))
            if self.first:
                self.board.make_logo((500, 130 + 20*sin(intro_t * self.framerate * 0.003)), intro_t - ref)
            self.make_tic()
            #self.check_instructions()
            self.board.render_lives(self.player.lives, (WINDOW_WIDTH/2 - 218, 50))
            pygame.display.flip()
            self.clock.tick(self.framerate)
            if pressed[pygame.K_ESCAPE]:
                is_running = False
            timer = 0.0
            if self.player.state == STATE_DEAD:
                self.time_dead += 1
            while self.player.state == STATE_DEAD and self.time_dead > self.framerate * 1.2:
                timer += 1.0
                pygame.display.update()
                pygame.event.pump()
                self.screen.fill((50, 50, 50))
                self.board.render_background(sin(timer/float(self.framerate)*2.0*pi/60.0)*3 + 4)
                game_over = pygame.image.load(os.path.join('game_over.png')).convert_alpha()
                game_over = pygame.transform.scale(game_over, (300, 200))
                self.screen.blit(game_over, (WINDOW_WIDTH/2 - 150, WINDOW_HEIGHT/2 - 100))
                pressed = pygame.key.get_pressed()
                if pressed[pygame.K_SPACE] != 0:
                    self.player.state = STATE_ALIVE
                    self.initialize()
                    is_running = 1
                    self.time += 1
                    can_complete = 0
                    seq = gen_sequence(self.num_items)
                    used = []
                    exempt_keys = []
                    self.flare_list = []
                    bkpos = self.player.pos
                    self.space_to_start = pygame.image.load(os.path.join('space_to_start.png')).convert_alpha()
                    self.space_to_start = pygame.transform.scale(self.space_to_start, (330, 30))
                    is_intro = 1
                    intro_t = 0
                    inst_up = False
                    inst2_up = False
                    self.first = False
                    self.time = -self.framerate * 5
                    self.is_vulnerable = 0
                    ref = intro_t
                    num_complete = 0
                    self.time_dead = 0
                pygame.display.flip()
                self.clock.tick(self.framerate)


        pygame.quit()

    # def check_instructions(self):
    #     alpha1 = min(1, self.inst_t/float(self.framerate))
    #     alpha2 = min(1, self.inst2_t/float(self.framerate))
    #     if alpha1 != 0:
    #         img = pygame.image.load(os.path.join('inst_1.png')).convert_alpha()
    #         self.change_alpha(img, alpha1 * 160, False)
    #         #img = pygame.transform.scale(img, (300, 240))
    #         img = pygame.transform.scale(img, (300, 240))
    #         self.screen.blit(img, (100, 360))
    #         text = pygame.image.load(os.path.join('inst_1.2.png')).convert_alpha()
    #         text = pygame.transform.scale(text, (320, 55))
    #         self.screen.blit(text, (100, 275))

    def ouch(self):
        if self.is_vulnerable:
            self.player.lives -= 1
            self.flare_list.append(Flare(self.index_to_pos(8), 300, self.screen, 0.7, True))
            self.player.state = STATE_DAMAGED
            self.beat_time *= 1.2
            if self.num_items > 5:
                self.num_items -= 1
            if self.beat_time > 8:
                self.beat_time = 8
            self.time = self.press_tolerance * self.framerate + 1
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
        elif self.player.state == STATE_DEAD:
            self.jump_l_sprite.tic((800, 480), self.time_dead % (tic_speed + 4) != 0)

    def index_to_pos(self, ind):
        coord = COORD_DICT[ind]
        x = coord[0]
        y = coord[1]
        xpos = 158 * x + 490
        ypos = 158 * y - 10
        return((xpos, ypos))

    def change_alpha(self, img, alpha=255, redden = True): #   change opacity of img to alpha
        width,height=img.get_size()
        for x in range(0,width):
            for y in range(0,height):
                r,g,b,old_alpha=img.get_at((x,y))
                if redden:
                    prop = (1 - (alpha + 100)/600.0)
                    g, b = prop*g, prop*b
                img.set_at((x,y),(r,g,b,alpha/255.0*float(old_alpha)))


if __name__ == "__main__":
    game = Game()
    game.initialize()
    game.mainloop()
