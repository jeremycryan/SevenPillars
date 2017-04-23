import pygame

# Visuals
WINDOW_WIDTH = 1600
WINDOW_HEIGHT = 900


# Gameplay
NUM_PILLARS = 7
KDICT_1 = {1:pygame.K_1, 2:pygame.K_2, 3:pygame.K_3, 4:pygame.K_q, 5:pygame.K_w, 6:pygame.K_e, 7:pygame.K_a, 8:pygame.K_s, 9:pygame.K_d}
KDICT_2 = {1:pygame.K_2, 2:pygame.K_3, 3:pygame.K_4, 4:pygame.K_w, 5:pygame.K_e, 6:pygame.K_r, 7:pygame.K_s, 8:pygame.K_d, 9:pygame.K_f}
KDICT_3 = {1:pygame.K_3, 2:pygame.K_4, 3:pygame.K_5, 4:pygame.K_e, 5:pygame.K_r, 6:pygame.K_t, 7:pygame.K_d, 8:pygame.K_f, 9:pygame.K_g}
KDICT_4 = {1:pygame.K_4, 2:pygame.K_5, 3:pygame.K_6, 4:pygame.K_r, 5:pygame.K_t, 6:pygame.K_y, 7:pygame.K_f, 8:pygame.K_g, 9:pygame.K_h}
KDICT_5 = {1:pygame.K_5, 2:pygame.K_6, 3:pygame.K_7, 4:pygame.K_t, 5:pygame.K_y, 6:pygame.K_u, 7:pygame.K_g, 8:pygame.K_h, 9:pygame.K_j}
KDICT_6 = {1:pygame.K_6, 2:pygame.K_7, 3:pygame.K_8, 4:pygame.K_y, 5:pygame.K_u, 6:pygame.K_i, 7:pygame.K_h, 8:pygame.K_j, 9:pygame.K_k}
KDICT_7 = {1:pygame.K_7, 2:pygame.K_8, 3:pygame.K_9, 4:pygame.K_u, 5:pygame.K_i, 6:pygame.K_o, 7:pygame.K_j, 8:pygame.K_k, 9:pygame.K_l}
PAD_DICT = {1:KDICT_1, 2:KDICT_2, 3:KDICT_3, 4:KDICT_4, 5:KDICT_5, 6:KDICT_6, 7:KDICT_7}

COORD_DICT = {1:(1, 1), 2:(2, 1), 3:(3, 1), 4:(1, 2), 5:(2, 2), 6:(3, 2), 7:(1, 3), 8:(2, 3), 9:(3, 3)}
NOT_COOL = [[1, 2, 3], [4, 5, 6], [7, 8, 9], [1, 4, 7], [2, 5, 8], [3, 6, 9], [1, 5, 9], [3, 5, 7]]

DIRECTION_DICT = {1:(-1, -1), 2:(0, -1), 3:(1, -1), 4:(-1, 0), 5:(0, 0), 6:(1, 0), 7:(-1, 1), 8:(0, 1), 9:(1, 1)}

# States
STATE_ALIVE = 0
STATE_SLASH_L = 1
STATE_JUMP_R = 2
STATE_JUMP_L = 3
STATE_DAMAGED = 4
STATE_DEAD = 5
