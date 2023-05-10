import sys
import pygame
from pygame.locals import *

img_basic_address = './img/'


class UNOGame():
    def __init__(self):
        pygame.init()
        self.background = pygame.image.load('../img/Story map.jpg')
        self.screen_width = 930
        self.screen_height = 690
        self.background_Color = (0,66,0)
        self.playernum = 2
        self.difficulty = 1
        self.font = 'Berlin Sans FB'
        self.clock = pygame.time.Clock()
        self.FPS = 30
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        pygame.display.set_caption("UNO!")
        self.screen.fill(self.background_Color)
        self.screen.blit(self.background, (-30, -30))
        pygame.display.update()
        self.main_menu()

    def text_format(self, message, textFont, textSize, textColor):
        newFont = pygame.font.SysFont(textFont, textSize)
        newText = newFont.render(message, True, textColor)
        return newText

    def main_menu(self):
        menu = True
        selected = 1

        
        while menu:
            pygame.init()
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == KEYDOWN:
                    if event.key == K_DOWN:
                        if selected <= 1:
                            selected = 1
                        else:
                            selected = selected - 1
                    elif event.key == K_UP:
                        if selected >= 1:
                            selected = 1
                        else:
                            selected = selected + 1
                    if event.key == K_RETURN: # K_RETURN은 엔터키
                        if selected <= 1:
                            #실행할 내용
                            pass
                        if selected == 2:
                            #실행할 내용
                            pass
                        if selected == 3:
                            #실행할 내용
                            pass
                        if selected >= 4:
                            pass
                if event.type == MOUSEBUTTONDOWN:
                    mouse_pos = pygame.mouse.get_pos()
                    if  MAP1_rect.collidepoint(mouse_pos):
                        selected = 1
                        pass
                    elif  MAP2_rect.collidepoint(mouse_pos):
                        selected = 2
                        pass
                    elif  MAP3_rect.collidepoint(mouse_pos):
                        selected = 3
                        pass
                    elif  MAP4_rect.collidepoint(mouse_pos):
                        selected = 4
                        pass

            if selected == 1:
                text_MAP1 = self.text_format("CHALLENGE", self.font, 50, (0,0,255))
            else:
                text_MAP1 = self.text_format("CHALLENGE", self.font, 50, (255, 255, 255))

            if selected == 2:
                text_MAP2 = self.text_format("CHALLENGE", self.font, 50, (0,0,0))
            else:
                text_MAP2= self.text_format("CHALLENGE", self.font, 50, (255, 255, 255))

            if selected == 3:
                text_MAP3 = self.text_format("CHALLENGE", self.font, 50, (0,0,0))
            else:
                text_MAP3 = self.text_format("CHALLENGE", self.font, 50, (255, 255, 255))

            if selected == 4:
                text_MAP4 = self.text_format("CHALLENGE", self.font, 50, (0,0,0))
            else:
                text_MAP4 = self.text_format("CHALLENGE", self.font, 50, (255, 255, 255))

            # 메뉴 아이템 표시
            MAP1_rect = text_MAP1.get_rect()
            MAP2_rect = text_MAP2.get_rect()
            MAP3_rect = text_MAP3.get_rect()
            MAP4_rect = text_MAP4.get_rect()

            MAP1_rect = pygame.Rect(self.screen_width/2-275, int(self.screen_height*0.8+20), 200, 50)
            MAP2_rect = pygame.Rect(self.screen_width/2-245, int(self.screen_height*0.2+20), 200, 50)          
            MAP3_rect = pygame.Rect(self.screen_width/2-40, int(self.screen_height*0.5-20), 200, 50)
            MAP4_rect = pygame.Rect(self.screen_width/2+140, int(self.screen_height*0.2-20), 200, 50)

            self.screen.blit(text_MAP1, MAP1_rect)

            pygame.display.update()
            self.clock.tick(self.FPS)
            pygame.display.set_caption("UNO!")
    

def main():
    game = UNOGame() 
    game.main_menu()

if __name__ == '__main__': 
    main()