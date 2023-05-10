import sys
import pygame
from pygame.locals import *

img_basic_address = './img/'


class UNOGame():
    def __init__(self):
        pygame.init()
        self.background = pygame.image.load('../img/background.png')
        self.screen_width = 800
        self.screen_height = 600
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

        start_rect = pygame.Rect(self.screen_width/2-50, int(self.screen_height*0.4), 200, 50)
        story_rect = pygame.Rect(self.screen_width/2-50, int(self.screen_height*0.5), 200, 50)
        multiplay_rect = pygame.Rect(self.screen_width/2-50, int(self.screen_height*0.6), 200, 50)
        set_rect = pygame.Rect(self.screen_width/2-50, int(self.screen_height*0.7), 200, 50)
        quit_rect = pygame.Rect(self.screen_width/2-50, int(self.screen_height*0.8), 200, 50)
        achievement_rect = pygame.Rect(self.screen_width/2-50, int(self.screen_height*0.9), 200, 50)

        while menu:
            pygame.init()
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == KEYDOWN:
                    if event.key == K_UP:
                        if selected <= 1:
                            selected = 1
                        else:
                            selected = selected - 1
                    elif event.key == K_DOWN:
                        if selected >= 6:
                            selected = 6
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
                        if selected == 4:
                            #실행할 내용
                            pass
                        if selected == 5:
                            #실행할 내용
                            pass
                        if selected >= 6:
                            pygame.quit()
                            sys.exit()
                            pass
                if event.type == MOUSEBUTTONDOWN:
                    mouse_pos = pygame.mouse.get_pos()
                    if start_rect.collidepoint(mouse_pos):
                        selected = 1
                        pass
                    elif story_rect.collidepoint(mouse_pos):
                        selected = 2
                        pass
                    elif multiplay_rect.collidepoint(mouse_pos):
                        selected = 3
                        pass
                    elif set_rect.collidepoint(mouse_pos):
                        selected = 4
                        pass
                    elif achievement_rect.collidepoint(mouse_pos):
                        selected = 5
                        pass
                    elif quit_rect.collidepoint(mouse_pos):
                        text_quit = self.text_format("QUIT", self.font, 50, (0,0,0))
                        self.screen.blit(text_quit, quit_rect)
                        pygame.display.update()
                        pygame.time.delay(500)
                        pygame.quit()
                        sys.exit()

            if selected == 1:
                text_start = self.text_format("START", self.font, 50, (0,0,0))
            else:
                text_start = self.text_format("START", self.font, 50, (255, 255, 255))

            if selected == 2:
                text_story = self.text_format("STORY MOD", self.font, 50, (0,0,0))
            else:
                text_story= self.text_format("STORY MOD", self.font, 50, (255, 255, 255))

            if selected == 3:
                text_multiplay = self.text_format("MULTIPLAY", self.font, 50, (0,0,0))
            else:
                text_multiplay = self.text_format("MULTIPLAY", self.font, 50, (255, 255, 255))

            if selected == 4:
                text_setting = self.text_format("SETTING", self.font, 50, (0,0,0))
            else:
                text_setting = self.text_format("SETTING", self.font, 50, (255, 255, 255))

            if selected == 5:
                text_achievement = self.text_format("ACHIEVEMENT", self.font, 50, (0,0,0))
            else:
                text_achievement = self.text_format("ACHIEVEMENT", self.font, 50, (255, 255, 255))

            if selected == 6:
                text_quit = self.text_format("QUIT", self.font, 50, (0,0,0))
            else:
                text_quit = self.text_format("QUIT", self.font, 50, (255, 255, 255))

            # 메뉴 아이템 표시
            start_rect = text_start.get_rect()
            story_rect = text_story.get_rect()
            multiplay_rect = text_multiplay.get_rect()
            set_rect = text_setting.get_rect()
            achievement_rect = text_achievement.get_rect()
            quit_rect = text_quit.get_rect()

            start_rect = pygame.Rect(self.screen_width/2-50, int(self.screen_height*0.4), 200, 50)
            story_rect = pygame.Rect(self.screen_width/2-50, int(self.screen_height*0.5), 200, 50)  
            multiplay_rect = pygame.Rect(self.screen_width/2-50, int(self.screen_height*0.6), 200, 50)         
            set_rect = pygame.Rect(self.screen_width/2-50, int(self.screen_height*0.7), 200, 50)
            achievement_rect = pygame.Rect(self.screen_width/2-50, int(self.screen_height*0.8), 200, 50)
            quit_rect = pygame.Rect(self.screen_width/2-50, int(self.screen_height*0.9), 200, 50)

            self.screen.blit(text_start, start_rect)
            self.screen.blit(text_story, story_rect)
            self.screen.blit(text_multiplay, multiplay_rect)
            self.screen.blit(text_setting, set_rect)
            self.screen.blit(text_achievement, achievement_rect)
            self.screen.blit(text_quit, quit_rect)

            pygame.display.update()
            self.clock.tick(self.FPS)
            pygame.display.set_caption("UNO!")
    

def main():
    game = UNOGame() 
    game.main_menu()

if __name__ == '__main__': 
    main()