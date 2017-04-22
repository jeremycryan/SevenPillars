import pygame
import os
from math import *
from Constants import *

class Board():
    def __init__(self, screen):
        self.debug_font = pygame.font.SysFont('myriad pro cond', 50)
        self.screen = screen
        self.mesh = pygame.image.load(os.path.join('mesh.png')).convert_alpha()
        self.mesh = pygame.transform.scale(self.mesh, (400, 400))
        change_alpha(self.mesh, 50)
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
        self.mist = pygame.transform.scale(self.mist, (int(WINDOW_WIDTH * 2), WINDOW_HEIGHT))
        self.white_screen = pygame.image.load(os.path.join('white_pixel.png')).convert_alpha()
        change_alpha(self.white_screen, 50, False)

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

    def render_slashes(self, newslash = None, old = False):
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
        mypos = -pos_prop * WINDOW_WIDTH/2 * 2.0
        self.screen.blit(self.sky, (spos, 0))
        self.screen.blit(self.mountains, (mpos, 0))
        self.screen.blit(self.mist, (mypos, 0))
        if in_time:
            white = self.white_screen
            white = pygame.transform.scale(white, (WINDOW_WIDTH, WINDOW_HEIGHT))
            self.screen.blit(white, (0, 0))

class Slash():
    def __init__(self, num1, num2, board):
        local_origin = (WINDOW_WIDTH/2 - 300 + board.true_offset[0], board.true_offset[1])
        if num1 > num2:
            num1, num2 = num2, num1
        num1_pos = COORD_DICT[num1]
        num2_pos = COORD_DICT[num2]
        self.compress = 0.3
        self.width = num1_pos[0] - num2_pos[0]
        self.height = num1_pos[1] - num2_pos[1]
        init_x = min(num1_pos[0], num2_pos[0])
        init_y = min(num1_pos[1], num2_pos[1])
        xscale = 145
        yscale = 145
        self.init_pos = init_x * xscale + local_origin[0], init_y * yscale + local_origin[1]
        #self.rect_width = 50 + 180*(self.width)
        #self.rect_height = 50 + 180*(self.height)
        self.angle = -(atan2(self.height, (self.width+0.01))/2/pi*360)
        self.slash = pygame.image.load(os.path.join('slash.png')).convert_alpha()
        self.length = sqrt((abs(self.width) + 1)**2 + (abs(self.height) + 1)**2)*0.95
        self.board = board

        self.shadow = pygame.image.load(os.path.join('slashshadow.png')).convert_alpha()
        self.shadow_length = sqrt((abs(self.width) + 1)**2 + (abs(self.height) + 1)**2)*1.10
        self.shadow = pygame.transform.scale(self.shadow, (int(100 * self.shadow_length * self.compress), int(50 * self.compress)))
        self.shadow = pygame.transform.rotate(self.shadow, self.angle)

    def render_slash(self, pos, alpha = 255):
        img = pygame.transform.scale(self.slash, (int(100 * self.length * self.compress), int(30 * self.compress)))
        if alpha != 255:
            change_alpha(img, alpha)
        img = pygame.transform.scale(img, (int(100 * self.length), int(30)))
        img = pygame.transform.rotate(img, self.angle)
        self.board.screen.blit(img, pos)

    def render_shadow(self, pos, alpha = 255):
        img = self.shadow
        if alpha != 255:
            change_alpha(img, alpha)
        self.board.screen.blit(img, pos)

def change_alpha(img, alpha=255, redden = True): #   change opacity of img to alpha
    width,height=img.get_size()
    for x in range(0,width):
        for y in range(0,height):
            r,g,b,old_alpha=img.get_at((x,y))
            if redden:
                prop = (1 - alpha/800)
                g, b = prop*g, prop*b
            img.set_at((x,y),(r,g,b,alpha/255*old_alpha))

def change_brightness(img, f = 0.75):
    width, height = img.get_size()
    for x in range(0, width):
        for y in range(0, height):
            r, g, b, alpha = img.get_at((x, y))
            img.set_at((x, y), (r*f, g*f, b*f, alpha))
