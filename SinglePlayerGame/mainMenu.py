import pygame
import sys
import random
from pygame.locals import *

pygame.init()
pygame.display.set_caption('UNO Game')
FPSCLOCK = pygame.time.Clock()
width, height = 1280, 720
Board = pygame.display.set_mode((width, height))
background = pygame.image.load('./UNOfficial/SinglePlayerGame/img/background.jpg')
game_font = pygame.font.SysFont(None, 40)

deck = []
colors = ['red', 'green', 'blue', 'yellow']
nums = ['R', 'S', '+2'] # reverse, skip, +2 draw
for i in range(0, 10):
    nums.append(str(i))
nums *= 2

for color in colors:
    for num in nums:
        deck.append((color, num))

#특수카드 추가
deck.append(('black', '+4'))

random.shuffle(deck)

def Game_Border():
    pygame.draw.line(Board, (255, 255, 255), (960, 0), (960, 720))
    pygame.draw.line(Board, (255, 255, 255), (0, 540), (960, 540))

class Button():
    def __init__(self, x, y, width, height, buttonText='Button', onclickFunction=None, onePress=False):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.onclickFunction = onclickFunction
        self.onePress = onePress

        self.fillColors = {
            'normal': '#ffffff',
            'hover': '#666666',
            'pressed': '#333333',
        }

        self.buttonSurface = pygame.Surface((self.width, self.height))
        self.buttonRect = pygame.Rect(self.x, self.y, self.width, self.height)

        self.buttonSurf = game_font.render(buttonText, True, (20, 20, 20))

        self.alreadyPressed = False

    def process(self):
        mousePos = pygame.mouse.get_pos()
        
        self.buttonSurface.fill(self.fillColors['normal'])
        if self.buttonRect.collidepoint(mousePos):
            self.buttonSurface.fill(self.fillColors['hover'])

            if pygame.mouse.get_pressed(num_buttons=3)[0]:
                self.buttonSurface.fill(self.fillColors['pressed'])

                if self.onePress:
                    self.onclickFunction()

                elif not self.alreadyPressed:
                    self.onclickFunction()
                    self.alreadyPressed = True

            else:
                self.alreadyPressed = False

        self.buttonSurface.blit(self.buttonSurf, [
            self.buttonRect.width/2 - self.buttonSurf.get_rect().width/2,
            self.buttonRect.height/2 - self.buttonSurf.get_rect().height/2
        ])
        Board.blit(self.buttonSurface, self.buttonRect)

def UNO_Button():
    print('Button Pressed')

customButton = Button(440, 100, 80, 50, 'UNO!', UNO_Button)

def main():
    while True:
        Board.fill((0, 0, 0))
        Board.blit(background, (0, 0))
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
        customButton.process()
        Game_Border()
        pygame.display.flip()
        FPSCLOCK.tick(60)

if __name__ == '__main__':
    main()