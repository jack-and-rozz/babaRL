import pygame
import pyBaba
import sprites
import config

COLOR_BACKGROUND = config.COLOR_BACKGROUND
BLOCK_SIZE = config.BLOCK_SIZE

class Renderer():
    def __init__(self, game, enable_render=True):
        pygame.init()
        pygame.font.init()
        pygame.display.set_caption('OpenAI Gym - baba-is-out-v0')

        self.font = pygame.font.Font(None, BLOCK_SIZE)

        self.game = game
        self.game_over = False
        self.enable_render = enable_render

        if self.enable_render is True:
            self.screen_size = (game.GetMap().GetWidth() * BLOCK_SIZE,
                                (game.GetMap().GetHeight() + 1) * BLOCK_SIZE)
            self.screen = pygame.display.set_mode(
                (self.screen_size[0], self.screen_size[1]), pygame.DOUBLEBUF)

            self.sprite_loader = sprites.SpriteLoader(BLOCK_SIZE)
            self.draw(game.GetMap())

    def draw_obj(self, map, x_pos, y_pos):
        objects = map.At(x_pos, y_pos)

        for obj_type in objects.GetTypes():
            if pyBaba.IsTextType(obj_type):
                obj_image = self.sprite_loader.text_images[obj_type]
            else:
                if obj_type == pyBaba.ObjectType.ICON_EMPTY:
                    continue
                obj_image = self.sprite_loader.icon_images[obj_type]
            obj_rect = obj_image.get_rect()
            obj_rect.topleft = (x_pos * BLOCK_SIZE, (y_pos + 1) * BLOCK_SIZE)
            self.screen.blit(obj_image, obj_rect)

    def draw(self, map, text=""):
        for y_pos in range(map.GetHeight()):
            for x_pos in range(map.GetWidth()):
                self.draw_obj(map, x_pos, y_pos)
        if text:
            text = self.font.render(text, False, config.COLOR_METATXT)
            self.screen.blit(text, (0, 0))


    def render(self, map, mode='human', text=""):
        if not hasattr(self, 'screen'):
            return

        try:
            if not self.game_over:
                self.screen.fill(config.COLOR_BACKGROUND)
                metabar = pygame.Rect(0, 0, 
                                      self.game.GetMap().GetWidth() * BLOCK_SIZE,
                                      BLOCK_SIZE)
                pygame.draw.rect(self.screen, (128, 128, 128), metabar, width=0)
                self.draw(map, text=text)

                if mode == 'human':
                    self.draw(map, text=text)
                    pygame.display.flip()

            self.process_event()
        except Exception as e:
            self.game_over = True
            self.quit_game()
            raise e
        else:
            pass

    def process_event(self):
        if not self.game_over:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.game_over = True
                    self.quit_game()

    def quit_game(self):
        self.game_over = True
        if self.enable_render is True:
            pygame.display.quit()
        pygame.quit()
