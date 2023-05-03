import pygame
from pygame.locals import *

# pick_color()가 20번째로 호출
class Popup(pygame.sprite.Sprite): 
    def __init__(self, name, position): # 'pickcolor', (400, 300)
        pygame.sprite.Sprite.__init__(self)
        self.name = name
        self.image = pygame.image.load('./img/' + name + '.png')
        self.position = position
        self.rect = self.image.get_rect()
        self.rect.center = self.position

    def get_name(self):
        return self.name
    def get_rect(self):
        return self.rect
