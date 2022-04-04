import argparse, time, glob
import pygame

import pyBaba
import config
import sys
import sprites
import copy

from core.images.rendering import Renderer
import core.options as options
from core.const import icon_id2name, text_id2name

def listup_objects_and_positions(game, object_properties=[]):
    res = []
    rule_manager = game.GetRuleManager()
    map_ = game.GetMap()
    width = map_.GetWidth()
    height = map_.GetHeight()
    for y in range(height):
        for x in range(width):
            sq = map_.At(x, y)
            objs = sq.GetObjects()
            for obj in objs:
                if rule_manager.HasType(obj, pyBaba.ObjectType.YOU):
                    res.append((icon_id2name[obj.GetType()], obj.GetId(), x, y))
    return res


def print_state(game, time_step):
    def rule2tuple(rule):
        subj = rule.GetSubject()
        oper = rule.GetOperator()
        pred = rule.GetPredicate()
        return tuple([text_id2name[x] for x in [subj, oper, pred]])

    print('<Step %d> Rules' % time_step, flush=True)
    current_rules = game.GetRuleManager().GetAllRules()
    for rule in current_rules:
        print('-', rule2tuple(rule))

    objects_and_positions = listup_objects_and_positions(game, [pyBaba.ObjectType.YOU])
    print('<Step %d> YOUs (type, id, x, y)' % time_step, flush=True)
    for obj, obj_id, x, y in objects_and_positions:
        print('-', (obj, obj_id, x, y))

    # you_ids = game.FindObjectIdsAndPositionsByProperty(pyBaba.ObjectType.YOU)
    # print(you_ids)

def change_time_step(game, time_step, diff=1):
    time_step += diff
    print_state(game, time_step)
    return time_step


def main(args):
    game = pyBaba.Game(args.map_path)
    print(game)
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
            renderer.render(game.GetMap(), text='Step %d, (KEY: SPACE + UDLR)' % time_step)

            time.sleep(0.5)
            renderer.show_result()
            pygame.display.flip()
            time.sleep(0.5)
            pygame.quit()
            sys.exit()

        events = pygame.event.get()
        if not events:
            continue
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
                elif event.key == pygame.K_UP:
                    game.MovePlayer(pyBaba.Direction.UP)
                    time_step = change_time_step(game, time_step, diff=1)
                elif event.key == pygame.K_DOWN:
                    game.MovePlayer(pyBaba.Direction.DOWN)
                    time_step = change_time_step(game, time_step, diff=1)
                elif event.key == pygame.K_LEFT:
                    game.MovePlayer(pyBaba.Direction.LEFT)
                    time_step = change_time_step(game, time_step, diff=1)
                elif event.key == pygame.K_RIGHT:
                    game.MovePlayer(pyBaba.Direction.RIGHT)
                    time_step = change_time_step(game, time_step, diff=1)
                elif event.key == pygame.K_SPACE:
                    game.MovePlayer(pyBaba.Direction.NONE) 
                    time_step = change_time_step(game, time_step, diff=1)
                elif event.key == pygame.K_BACKSPACE:
                    print('TODO: implement undo')
                    time_step = change_time_step(game, time_step, diff=-1)
        if game.GetPlayState() == pyBaba.PlayState.WON or game.GetPlayState() == pyBaba.PlayState.LOST:
            game_over = True

        renderer.render(game.GetMap(), 
                        text='Step %d, (KEY: SPACE + UDLR)' % time_step)
        pygame.display.flip()
        clock.tick(config.FPS)

if __name__ == '__main__':
    args = options.get_evaluation_args()
    main(args)

