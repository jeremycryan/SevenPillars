import pygame
import os
from math import *
from Constants import *

class Board():
    def __init__(self, screen):
        self.debug_font = pygame.font.SysFont('myriad pro cond', 50)
        self.screen = screen
        self.mesh = pygame.image.load(os.path.join('mesh.png')).convert_alpha()
        self.mesh = pygame.transform.scale(self.mesh, (100, 100))
        change_alpha(self.mesh, 50, False)
        self.mesh = pygame.transform.scale(self.mesh, (400, 400))
        change_brightness(self.mesh, 0.6)
        self.mesh_pos = (WINDOW_WIDTH/2 - 200, 100)
        self.slash_list = []
        self.old_slash_list = []
        self.old_slash_alpha = 255
        self.true_offset = (0, 0)
        self.prop_done = 0
        self.mountains = pygame.image.load(os.path.join('mountains.png')).convert_alpha()
        self.mountains = pygame.transform.scale(self.mountains, (int(WINDOW_WIDTH * 1.5), WINDOW_HEIGHT))
        self.sky = pygame.image.load(os.path.join('sky.png')).convert_alpha()
        self.sky = pygame.transform.scale(self.sky, (int(WINDOW_WIDTH * 1.5), WINDOW_HEIGHT))
        self.mist = pygame.image.load(os.path.join('mist.png')).convert_alpha()
        self.mist = pygame.transform.scale(self.mist, (int(WINDOW_WIDTH * 2.5), WINDOW_HEIGHT))
        self.pillars = pygame.image.load(os.path.join('pillars.png')).convert_alpha()
        self.pillars = pygame.transform.scale(self.pillars, (int(WINDOW_WIDTH * 2.5), WINDOW_HEIGHT))
        self.white_screen = pygame.image.load(os.path.join('white_pixel.png')).convert_alpha()
        change_alpha(self.white_screen, 80, False)
        self.blue = pygame.image.load(os.path.join('blue.png')).convert_alpha()
        self.white = pygame.image.load(os.path.join('cirquel.png')).convert_alpha()
        self.bpos = (0, 0)
        self.cat = pygame.image.load(os.path.join('catface.png')).convert_alpha()
        self.logo = pygame.image.load(os.path.join('seven_pillars.png')).convert_alpha()
        self.logo = pygame.transform.scale(self.logo, (600, 400))
        change_alpha(self.blue, 120)

    def render_lives(self, number, position):
        xpos = position[0]
        ypos = position[1]
        spacing = 50
        cat = pygame.image.load(os.path.join('catface.png')).convert_alpha()
        #change_alpha(cat, 175)
        self.screen.blit(cat, position)
        if number > 1:
            self.render_lives(number - 1, (xpos + spacing, ypos))

    def make_blue(self, pos):
        xpos, ypos = COORD_DICT[pos]
        xspace = 157
        x = xpos * xspace + 440
        yspace = 157
        y = ypos * yspace - 60
        self.bpos = (x, y)
        self.screen.blit(self.blue, (x, y))

    def update_offset(self, framerate, number):
        direction = DIRECTION_DICT[number]
        if self.prop_done < 1:
            move_amt = 20
            self.true_offset = (sin(self.prop_done*pi)*direction[0] * move_amt, sin(self.prop_done*pi)*direction[1] * move_amt)
            self.prop_done = self.prop_done + 3/framerate
        else:
            self.true_offset = (0, 0)
            self.prop_done = 1

    def print_seq(self, seq):
        render = self.debug_font.render(str(seq), 1, (255, 255, 255))
        self.screen.blit(render, (50, 50))

    def print_active(self, button):
        render = self.debug_font.render(str(button), 1, (255, 255, 255))
        self.screen.blit(render, (50, 100))

    def update_board(self):
        mesh_rect = self.mesh.get_rect()
        meshy = (self.mesh_pos[0] + self.true_offset[0], self.mesh_pos[1] + self.true_offset[1])
        self.screen.blit(self.mesh, meshy)

    def render_slashes(self, newslash = None, old = False, icon = False):
        if newslash != None:
            self.slash_list.append(newslash)
        list = self.slash_list
        alpha = 255
        if old:
            list = self.old_slash_list
            alpha = max(0, self.old_slash_alpha)
        for a in list:
            a.render_slash((a.init_pos), alpha)

    def render_background(self, pos, in_time = False):
        pos_prop = pos/7
        spos = -pos_prop * WINDOW_WIDTH/2 * 0.4
        mpos = -pos_prop * WINDOW_WIDTH/2 * 1.0
        mypos = -pos_prop * WINDOW_WIDTH/2 * 2.5
        pillar_offset = 780
        ppos = -pos_prop * WINDOW_WIDTH/2 * 4.4 + pillar_offset
        self.screen.blit(self.sky, (spos, 0))
        self.screen.blit(self.mountains, (mpos, 0))
        self.screen.blit(self.mist, (mypos, 0))
        if in_time:
            white = self.white_screen
            white = pygame.transform.scale(white, (WINDOW_WIDTH, WINDOW_HEIGHT))
            self.screen.blit(white, (0, 0))
        self.screen.blit(self.pillars, (ppos, 50))

    def render_washout(self, alpha):
        self.white = pygame.image.load(os.path.join('white_pixel.png')).convert_alpha()
        change_alpha(self.white, alpha * 255.0, True)
        white = pygame.transform.scale(self.white, (WINDOW_WIDTH, WINDOW_HEIGHT))
        self.screen.blit(white, (0, 0))

    def make_logo(self, pos, t):
        cap = 30.0
        t = max(0, t)
        done = t/cap
        alpha = (1-done) * 255
        if done < 1:
            logo = pygame.image.load(os.path.join('seven_pillars.png')).convert_alpha()
            change_alpha(logo, alpha, False)
            logo = pygame.transform.scale(logo, (int(600 + 30*done), int(400 + 30*done)))
            self.screen.blit(logo, pos)


class Slash():
    def __init__(self, num1, num2, board, icon = False):
        local_origin = (WINDOW_WIDTH/2 - 310 + board.true_offset[0], board.true_offset[1] - 20)
        if num1 > num2:
            num1, num2 = num2, num1
        num1_pos = COORD_DICT[num1]
        num2_pos = COORD_DICT[num2]
        self.compress = 0.3
        self.width = num1_pos[0] - num2_pos[0]
        self.height = num1_pos[1] - num2_pos[1]
        init_x = min(num1_pos[0], num2_pos[0])
        init_y = min(num1_pos[1], num2_pos[1])
        xscale = 155
        yscale = 155
        self.is_icon = icon
        #self.rect_width = 50 + 180*(self.width)
        #self.rect_height = 50 + 180*(self.height)
        self.angle = -(atan2(self.height, (self.width+0.01))/2/pi*360)
        self.slash = pygame.image.load(os.path.join('slash.png')).convert_alpha()
        self.length = sqrt((abs(self.width) + 1)**2 + (abs(self.height) + 1)**2)*1.0
        self.board = board
        self.init_pos = init_x * xscale + local_origin[0] - 15, init_y * yscale + local_origin[1]

        self.shadow = pygame.image.load(os.path.join('slashshadow.png')).convert_alpha()
        self.shadow_length = sqrt((abs(self.width) + 1)**2 + (abs(self.height) + 1)**2)*1.10
        self.shadow = pygame.transform.scale(self.shadow, (int(100 * self.shadow_length * self.compress), int(50 * self.compress)))
        self.shadow = pygame.transform.rotate(self.shadow, self.angle)

    def render_slash(self, pos, alpha = 255):
        img = pygame.transform.scale(self.slash, (int(100 * self.length * self.compress), int(30 * self.compress)))
        if alpha != 255:
            change_alpha(img, alpha, False)
        img = pygame.transform.scale(img, (int(100 * self.length), int(30)))
        img = pygame.transform.rotate(img, self.angle)
        surface = self.board.screen
        if self.is_icon:
            surface = pygame.Surface((400, 400)).convert_alpha()
            surface.fill((255, 0, 0))
            surface.set_alpha(255)
            surface.blit(img, (self.init_pos[0] - 1000, self.init_pos[1]))
            self.remove_trans(surface)
            surface = pygame.transform.scale(surface, (100, 100))
            img = surface
        self.board.screen.blit(img, pos)

    def remove_trans(self, img):
        width, height = img.get_size()
        for x in range(0, width):
            for y in range(0, height):
                r, g, b, alpha = img.get_at((x, y))
                if (r, g, b) == (255, 0, 0):
                    img.set_at((x, y), (r, g, b, 0))

    def render_shadow(self, pos, alpha = 255):
        img = self.shadow
        if alpha != 255:
            change_alpha(img, alpha)
        self.board.screen.blit(img, pos)

class Flare():
    def __init__(self, pos, s1, screen, start_opacity, redden = False):
        self.redden = redden
        self.start_opacity = start_opacity
        self.screen = screen
        self.init_pos = pos
        self.flaret = 0
        self.s1 = s1
        self.scale = sqrt(self.flaret * 0.1 + 1)
        self.pos = (pos[0] - s1/2 * self.scale, pos[1] - s1/2 * self.scale)
        self.opacity = int(max(0, 255 - self.flaret * 5)) * start_opacity
        self.flare = pygame.image.load(os.path.join('cirquel.png')).convert_alpha()
        pygame.transform.scale(self.flare, (int(s1 * self.scale), int(s1 * self.scale)))


    def update(self):
        self.scale = sqrt(self.flaret * 0.1 + 1)
        self.pos = (self.init_pos[0] - self.s1/2 * self.scale, self.init_pos[1] - self.s1/2 * self.scale)
        self.opacity = int(max(0, 255 - self.flaret * 5)) * self.start_opacity
        flare = pygame.image.load(os.path.join('cirquel.png')).convert_alpha()
        flare = pygame.transform.scale(flare, (40, 40))
        self.flaret += 3
        if self.opacity > 0:
            change_alpha(flare, self.opacity, self.redden)
            flare = pygame.transform.scale(flare, (int(self.s1 * self.scale), int(self.s1 * self.scale)))
            self.screen.blit(flare, self.pos)

def change_alpha(img, alpha=255, redden = True): #   change opacity of img to alpha
    width,height=img.get_size()
    for x in range(0,width):
        for y in range(0,height):
            r,g,b,old_alpha=img.get_at((x,y))
            if redden:
                prop = (1 - (alpha + 100)/600.0)
                g, b = prop*g, prop*b
            img.set_at((x,y),(r,g,b,alpha/255.0*float(old_alpha)))

def change_brightness(img, f = 0.75):
    width, height = img.get_size()
    for x in range(0, width):
        for y in range(0, height):
            r, g, b, alpha = img.get_at((x, y))
            img.set_at((x, y), (r*f, g*f, b*f, float(alpha)))
