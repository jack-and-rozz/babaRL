import argparse
import pygame

import pyBaba
import config
import sys
import sprites

from create_gif import draw, draw_obj, setup_game, setup_sprites, setup_screen
import utils

def main(args):
    map_path = "baba-is-auto/Resources/Maps/baba_is_you.txt"

    game = setup_game(map_path)
    screen = setup_screen(game)
    sprite_loader, result_image_group = setup_sprites()
    pygame.init()
    pygame.font.init()

    action_dic = {"Direction.UP": pyBaba.Direction.UP, "Direction.DOWN": pyBaba.Direction.DOWN,
                  "Direction.LEFT": pyBaba.Direction.LEFT, "Direction.RIGHT": pyBaba.Direction.RIGHT, "Direction.NONE": pyBaba.Direction.NONE}
    action_file = open("./action.txt", 'r')
    actions = action_file.read().splitlines()
    action_file.close()

    clock = pygame.time.Clock()

    pygame.time.set_timer(pygame.USEREVENT, 200)

    game_over = False
    time_step = 0

    screen_size = utils.get_screen_size(game)

    while True:
        if game_over:
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        pygame.quit()
                        sys.exit()
            if game.GetPlayState() == pyBaba.PlayState.WON:
                result_image_group.update(pyBaba.PlayState.WON, screen_size)
                result_image_group.draw(screen)
            else:
                result_image_group.update(pyBaba.PlayState.LOST, screen_size)
                result_image_group.draw(screen)
            pygame.display.flip()
            continue

        for event in pygame.event.get():
            if event.type == pygame.USEREVENT:
                if time_step < len(actions):
                    game.MovePlayer(action_dic[actions[time_step]])
                    time_step += 1
                else:
                    pass
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()

        if game.GetPlayState() == pyBaba.PlayState.WON or game.GetPlayState() == pyBaba.PlayState.LOST:
            game_over = True

        screen.fill(config.COLOR_BACKGROUND)
        text = None
        draw(game, screen, sprite_loader, text=text)
        pygame.display.flip()

        clock.tick(config.FPS)

if __name__ == '__main__':
    parser = argparse.ArgumentParser( 
        add_help=True,
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    args = parser.parse_args()
    main(args)

