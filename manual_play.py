import argparse, time, glob
import pygame

import pyBaba
import config
import sys
import sprites


from rendering import Renderer


def main(args):
    game = pyBaba.Game(args.map_path)
    renderer = Renderer(game)

    clock = pygame.time.Clock()
    pygame.time.set_timer(pygame.USEREVENT, 100)
    game_over = False
    time_step = 0

    while True:
        if game_over:
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        pygame.quit()
                        sys.exit()

            renderer.show_result()
            pygame.display.flip()
            time.sleep(0.5)
            pygame.quit()
            sys.exit()

        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
                elif event.key == pygame.K_UP:
                    game.MovePlayer(pyBaba.Direction.UP)
                    time_step += 1
                elif event.key == pygame.K_DOWN:
                    game.MovePlayer(pyBaba.Direction.DOWN)
                    time_step += 1
                elif event.key == pygame.K_LEFT:
                    game.MovePlayer(pyBaba.Direction.LEFT)
                    time_step += 1
                elif event.key == pygame.K_RIGHT:
                    game.MovePlayer(pyBaba.Direction.RIGHT)
                    time_step += 1
                elif event.key == pygame.K_SPACE:
                    # game.MovePlayer(pyBaba.Direction.NONE) # This leads to game over?
                    time_step += 1

        if game.GetPlayState() == pyBaba.PlayState.WON or game.GetPlayState() == pyBaba.PlayState.LOST:
            game_over = True

        renderer.render(game.GetMap(), text='Step %d, (KEY: SPACE + UDLR)' % time_step)
        pygame.display.flip()
        clock.tick(config.FPS)

if __name__ == '__main__':

    map_candidates = [l.split('/')[-1].split('.')[0] for l in glob.glob(config.MAP_ROOT + '/*')]

    parser = argparse.ArgumentParser( 
        add_help=True,
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('map_name', choices=map_candidates)
    args = parser.parse_args()
    args.map_path = config.MAP_ROOT + '/' + args.map_name + '.txt'
    main(args)
