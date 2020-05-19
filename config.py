import pygame, pyBaba

FPS = 20
# BLOCK_SIZE = 48
BLOCK_SIZE = 20
COLOR_BACKGROUND = pygame.Color(0, 0, 0)

COLOR_METATXT = (200, 50, 50)

pygame.font.init()
font = pygame.font.Font(None, BLOCK_SIZE)

action_dic = {
    "Direction.UP": pyBaba.Direction.UP, 
    "Direction.DOWN": pyBaba.Direction.DOWN,
    "Direction.LEFT": pyBaba.Direction.LEFT, 
    "Direction.RIGHT": pyBaba.Direction.RIGHT, 
    "Direction.NONE": pyBaba.Direction.NONE
}



