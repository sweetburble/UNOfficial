import sys
import pygame
from pygame.locals import *

img_basic_address = './img/'


class UNOGame():
    def __init__(self):
        pygame.init()
        self.background = pygame.image.load('img/background.jpg')
        self.screen_width = 300
        self.screen_height = 300
        self.background_Color = (0,66,0)
        self.playernum = 2
        self.difficulty = 1
        self.font = 'Berlin Sans FB'
        self.clock = pygame.time.Clock()
        self.FPS = 30
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        pygame.display.set_caption("UNO!")
        self.screen.fill(self.background_Color)
        self.screen.blit(self.background, (-300, -300))
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
                        if selected >= 2:
                            selected = 2
                        else:
                            selected = selected + 1
                    if event.key == K_RETURN: # K_RETURN은 엔터키
                        if selected <= 1:
                            #실행할 내용
                            pass
                        if selected == 2:
                            #실행할 내용
                            pass
                   
                if event.type == MOUSEBUTTONDOWN:
                    mouse_pos = pygame.mouse.get_pos()
                    if  MAP2_rect.collidepoint(mouse_pos):
                        selected = 1
                        pass
                    elif  MAP3_rect.collidepoint(mouse_pos):
                        selected = 2
                        pass
                    elif  MAP4_rect.collidepoint(mouse_pos):
                        selected = 3
                        pass
                       
            if selected == 1:
                text_MAP2 = self.text_format("OPTION", self.font, 50, (0,0,0))
            else:
                text_MAP2 = self.text_format("OPTION", self.font, 50, (255, 255, 255))

            if selected == 2:
                text_MAP3 = self.text_format("ACHIEVEMENT", self.font, 50, (0,0,0))
            else:
                text_MAP3= self.text_format("ACHIEVEMENT", self.font, 50, (255, 255, 255))

            if selected == 3:
                text_MAP4 = self.text_format("QUIT", self.font, 50, (0,0,0))
            else:
                text_MAP4= self.text_format("QUIT", self.font, 50, (255, 255, 255))

            #질문 내용 표시
            text_MAP1= self.text_format("PAUSE", self.font, 70, (255, 255, 255))

            # 메뉴 아이템 표시
            MAP1_rect = text_MAP1.get_rect()
            MAP2_rect = text_MAP2.get_rect()
            MAP3_rect = text_MAP3.get_rect()
            MAP4_rect = text_MAP4.get_rect()

            MAP1_rect = pygame.Rect(self.screen_width/2-80, int(self.screen_height*0.1), 100, 100)
            MAP2_rect = pygame.Rect(self.screen_width/8-20, int(self.screen_height*0.4), 100, 40)
            MAP3_rect = pygame.Rect(self.screen_width/8-20, int(self.screen_height*0.6), 100, 40)  
            MAP4_rect = pygame.Rect(self.screen_width/8-20, int(self.screen_height*0.8), 100, 40) 
  
            self.screen.blit(text_MAP1, MAP1_rect)
            self.screen.blit(text_MAP2, MAP2_rect)
            self.screen.blit(text_MAP3, MAP3_rect)
            self.screen.blit(text_MAP4, MAP4_rect)

            pygame.display.update()
            self.clock.tick(self.FPS)
            pygame.display.set_caption("UNO!")
    

def main():
    game = UNOGame() 
    game.main_menu()

if __name__ == '__main__': 
    main()