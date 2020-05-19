
import pygame
import pyBaba
import config



def get_all_obj(game):
    return [[ game.GetMap().At(x_pos, y_pos) for x_pos in range(game.GetMap().GetWidth())] for y_pos in range(game.GetMap().GetHeight())]


def get_screen_size(game, show_metatxt=True):
    if show_metatxt:
        screen_size = (game.GetMap().GetWidth() * config.BLOCK_SIZE,
                       (game.GetMap().GetHeight() + 1) * config.BLOCK_SIZE)
    else:
        screen_size = (game.GetMap().GetWidth() * config.BLOCK_SIZE,
                       game.GetMap().GetHeight() * config.BLOCK_SIZE)
    return screen_size
 

