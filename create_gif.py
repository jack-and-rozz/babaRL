import argparse, glob
import pygame
import pyBaba
import sys, time
from PIL import Image

from core.images.rendering import Renderer
import core.images.sprites as sprites
import core.options as options
import config

def get_all_obj(game):
    return [[game.GetMap().At(x_pos, y_pos) for x_pos in range(game.GetMap().GetWidth())] for y_pos in range(game.GetMap().GetHeight())]

def play(game, actions, epoch=0):
    game_over = False
    images = []
    prev_state = None
    renderer = Renderer(game)
    screen = renderer.screen

    for time_step, action in enumerate(actions):
        text = 'Epoch %d, Step %d, Action: %s' % (epoch, time_step, action)

        if game_over:
            renderer.show_result()
            pygame.display.flip()
            return images

        game.MovePlayer(config.action_dic[actions[time_step]])

        if game.GetPlayState() == pyBaba.PlayState.WON or game.GetPlayState() == pyBaba.PlayState.LOST:
            game_over = True

        state = get_all_obj(game)
        if prev_state == state: # Omit rendering if the next state keeps the same.
            continue

        prev_state = state
        action = action.split('.')[-1]
        text = 'Epoch %d, Step %d, Action: %s' % (epoch, time_step, action)
        renderer.render(game.GetMap(), text=text)
        img = screen2image(renderer.screen, epoch, time_step, action)
        images.append(img)

    if game_over:
        renderer.show_result()
        pygame.display.flip()
        img = screen2image(screen, epoch, time_step, action)
        images.append(img)
    return images

def screen2image(screen, epoch, time_step, action):
    X, Y = screen.get_size()
    img = Image.new('RGB', (X, Y), (0,0,0))
    for x in range(X):
        for y in range(Y):
            c = screen.get_at((x,y))
            img.putpixel((x,y), (c.r,c.g,c.b))
    return img

def save_as_animation(images, save_path):
    images[0].save(save_path, save_all=True, 
                   append_images=images[1:], optimize=False, 
                   duration=200, loop=0)


def main(args):
    game = pyBaba.Game(args.map_path)

    action_logs = load_action_logs()
    images = []
    action_logs = [action_logs[0] for _ in range(2)]

    for epoch, actions in enumerate(action_logs):
        game = pyBaba.Game(args.map_path)
        images += play(game, actions, epoch)


    save_as_animation(images, 'stage.gif')


def load_action_logs():
    action_file = open("./action.txt", 'r')
    actions = action_file.read().splitlines()
    action_file.close()
    return [actions]

if __name__ == '__main__':
    args = options.get_evaluation_args()
    main(args)
