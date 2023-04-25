import pygame
from pygame.locals import *
import math

# set_window()가 4번째로 호출
class Card(pygame.sprite.Sprite):
    def __init__(self, name, position):
        pygame.sprite.Sprite.__init__(self)
        self.name = name
        self.image = pygame.image.load('./img/' + name + '.png') # back.png -> 뒤집힌 카드 이미지를 로드한다.
        self.image = pygame.transform.scale(self.image, (80, 100))
        self.orig_pos = position # (350, 300)이다. 
        self.position = position
        self.user_rotation = 30
        self.rect = self.image.get_rect()
        self.rect.center = self.position

    # dest_loc = (200 + 70*i, 500)이다
    def update(self, dest_loc):
        x, y = self.position
        vx, vy = (dest_loc[0] - x, dest_loc[1] - y)
        vx, vy = (x/(x**2+y**2)**0.5, y/(x**2+y**2)**0.5)

        speed = 5

        x = x + speed*vx
        y = y + speed*vy

        if x >= dest_loc[0]:
            x = dest_loc[0]
        if y >= dest_loc[1]:
            y = dest_loc[1]

        self.position = (x, y)
        self.rect = self.image.get_rect()
        self.rect.center = self.position
    
    # 카드를 rotate만큼 회전시키는 함수
    def rotation(self, rotate):
        self.image = pygame.transform.rotate(self.image, rotate)

    def getposition(self):
        return self.position

    def setposition(self, x, y):
        i_x = x
        i_y = y
        self.position = (i_x, i_y)
        self.rect = self.image.get_rect()
        self.rect.center = self.position

    def move(self, compare_pos):
        x, y = self.position
        i_x = compare_pos[0]
        i_y = compare_pos[1]

        if x > i_x+60 and y == i_y:
            x -= 70

        elif y > i_y:
            if x <= 200:
                x = 620
                y = y - 80
            else:
                x -=70
        self.position = (x, y)
        self.rect = self.image.get_rect()
        self.rect.center = self.position

    def get_rect(self):
        return self.rect

    def get_name(self):
        return self.name
