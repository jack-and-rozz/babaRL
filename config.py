import pygame, pyBaba

FPS = 10
# BLOCK_SIZE = 48
BLOCK_SIZE = 20
COLOR_BACKGROUND = pygame.Color(0, 0, 0)

COLOR_METATXT = (200, 50, 50)

# pygame.font.init()
# font = pygame.font.Font(None, BLOCK_SIZE)

action_dic = {
    "Direction.UP": pyBaba.Direction.UP, 
    "Direction.DOWN": pyBaba.Direction.DOWN,
    "Direction.LEFT": pyBaba.Direction.LEFT, 
    "Direction.RIGHT": pyBaba.Direction.RIGHT, 
    "Direction.NONE": pyBaba.Direction.NONE
}

MAP_ROOT = 'baba-is-auto/Resources/Maps'



# deffiles = ['NounType.def', 'OpType.def', 'PropertyType.def', 'IconType.def']
# enum_root = 'baba-is-auto/Includes/baba-is-auto/Enums'
object_id2name = [l.strip() for l in open('./objects.list')]


