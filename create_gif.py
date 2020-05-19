import argparse
import pygame
import pyBaba
import config
import sys, time
import sprites
from PIL import Image, ImageDraw, ImageFont

def draw_obj(game, screen, x_pos, y_pos):
    objects = game.GetMap().At(x_pos, y_pos)

    for obj_type in objects.GetTypes():
        if pyBaba.IsTextType(obj_type):
            obj_image = sprite_loader.text_images[obj_type]
        else:
            if obj_type == pyBaba.ObjectType.ICON_EMPTY:
                continue
            obj_image = sprite_loader.icon_images[obj_type]
        obj_image.render(screen, (x_pos * config.BLOCK_SIZE,
                                  (y_pos + 1) * config.BLOCK_SIZE))

def draw(game, screen, epoch, time_step, action):
    for y_pos in range(game.GetMap().GetHeight()):
        for x_pos in range(game.GetMap().GetWidth()):
            draw_obj(game, screen, x_pos, y_pos)


    action = action.split('.')[-1]
    text = 'Epoch %d, Step %d, Action: %s' % (epoch, time_step, action)
    text = font.render(text, False, config.COLOR_METATXT)
    screen.blit(text, (0, 0))
    pygame.display.update()


def get_all_obj(game):
    return [[ game.GetMap().At(x_pos, y_pos) for x_pos in range(game.GetMap().GetWidth())] for y_pos in range(game.GetMap().GetHeight())]

def play(game, actions, epoch=0):
    game_over = False
    images = []
    prev_state = None
    for time_step, action in enumerate(actions):
        text = 'Epoch %d, Step %d, Action: %s' % (epoch, time_step, action)
        print(text)

        if game_over:
            if game.GetPlayState() == pyBaba.PlayState.WON:
                result_image_group.update(pyBaba.PlayState.WON, screen_size)
                result_image_group.draw(screen)
                print('Won')
            else:
                result_image_group.update(pyBaba.PlayState.LOST, screen_size)
                result_image_group.draw(screen)
                print('Lost')
            pygame.display.flip()
            return images

        game.MovePlayer(action_dic[actions[time_step]])

        if game.GetPlayState() == pyBaba.PlayState.WON or game.GetPlayState() == pyBaba.PlayState.LOST:
            game_over = True

        state = get_all_obj(game)
        if prev_state == state: # Omit rendering if the next state keeps the same.
            continue

        prev_state = state

        screen.fill(config.COLOR_BACKGROUND)
        draw(game, screen, epoch, time_step, action)
        pygame.display.flip()

        img = screen2image(screen, epoch, time_step, action)
        images.append(img)

    if game_over:
        screen_size = (game.GetMap().GetWidth() * config.BLOCK_SIZE,
                       (game.GetMap().GetHeight() + 1) * config.BLOCK_SIZE)

        if game.GetPlayState() == pyBaba.PlayState.WON:
            result_image_group.update(pyBaba.PlayState.WON, screen_size)
            result_image_group.draw(screen)
            print('Won')
        else:
            result_image_group.update(pyBaba.PlayState.LOST, screen_size)
            result_image_group.draw(screen)
            print('Lost')
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


def setup_game(map_path):
    game = pyBaba.Game(map_path)
    return game

def setup_screen(game):
    screen_size = (game.GetMap().GetWidth() * config.BLOCK_SIZE,
                   (game.GetMap().GetHeight() + 1) * config.BLOCK_SIZE)
    screen = pygame.display.set_mode(
        (screen_size[0], screen_size[1]), pygame.DOUBLEBUF) #.convert()
    return screen

def setup_sprites():
    sprite_loader = sprites.SpriteLoader(config.BLOCK_SIZE, as_gifimage=True)
    result_image = sprites.ResultImage()
    result_image_group = pygame.sprite.Group()
    result_image_group.add(result_image)
    return sprite_loader, result_image_group

def main(args):
    map_path = "../../Resources/Maps/out_of_reach.txt"
    map_path = "baba-is-auto/Resources/Maps/baba_is_you.txt"

    global screen 
    game = setup_game(map_path)
    screen = setup_screen(game)

    global sprite_loader 
    global result_image_group
    sprite_loader, result_image_group = setup_sprites()

    global action_dic
    action_dic = {
        "Direction.UP": pyBaba.Direction.UP, 
        "Direction.DOWN": pyBaba.Direction.DOWN,
        "Direction.LEFT": pyBaba.Direction.LEFT, 
        "Direction.RIGHT": pyBaba.Direction.RIGHT, 
        "Direction.NONE": pyBaba.Direction.NONE
    }

    pygame.init()
    pygame.font.init()
    global font
    font = pygame.font.Font(None, config.BLOCK_SIZE)

    action_logs = load_action_logs()
    images = []
    action_logs = [action_logs[0] for _ in range(2)]

    for epoch, actions in enumerate(action_logs):
        game = setup_game(map_path)
        images += play(game, actions, epoch)


    save_as_animation(images, 'stage.gif')


def load_action_logs():
    action_file = open("./action.txt", 'r')
    actions = action_file.read().splitlines()
    action_file.close()
    return [actions]

if __name__ == '__main__':
    parser = argparse.ArgumentParser( 
        add_help=True,
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    # parser.add_argument('models_root', type=str)
    args = parser.parse_args()
    main(args)

