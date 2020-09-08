import pygame
import pyBaba
from core.images.gifimage import GIFImage
from core.const import icon_id2name, text_id2name

class SpriteLoader:
    def __init__(self, block_size, as_gifimage=False):
        self.scale = - (1.0 - (2 * block_size) / 48.)
        self.icon_images = {k:v for k, v in icon_id2name.items()}

        for i in self.icon_images:
            if as_gifimage: 
                self.icon_images[i] = GIFImage(
                    './sprites/icon/{}.gif'.format(self.icon_images[i]))
                self.icon_images[i].scale(self.scale)
            else:
                self.icon_images[i] = pygame.transform.scale(pygame.image.load(
                    './sprites/icon/{}.gif'.format(self.icon_images[i])),
                                                (block_size, block_size))


        self.text_images = {k:v for k, v in text_id2name.items()}

        for i in self.text_images:
            if as_gifimage: 

                self.text_images[i] = GIFImage(
                    './sprites/text/{}.gif'.format(self.text_images[i]))
                self.text_images[i].scale(self.scale)
            else:
                self.text_images[i] = pygame.transform.scale(pygame.image.load(
                    './sprites/text/{}.gif'.format(self.text_images[i])),
                                                (block_size, block_size))



class ResultImage(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)

    def update(self, status, screen_size):
        if status == pyBaba.PlayState.WON:
            self.size = max(screen_size[0], screen_size[1]) // 2
            self.image = pygame.transform.scale(pygame.image.load(
                './sprites/won.png'), (self.size, self.size))
            self.rect = self.image.get_rect()
            self.rect.center = (screen_size[0] // 2, screen_size[1] // 2)
        else:
            self.size = max(screen_size[0], screen_size[1]) // 2
            self.image = pygame.transform.scale(pygame.image.load(
                './sprites/lost.png'), (self.size, self.size))
            self.rect = self.image.get_rect()
            self.rect.center = (screen_size[0] // 2, screen_size[1] // 2)
