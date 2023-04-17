import sys
import pygame
from pygame.locals import *

img_basic_address = './img/'


class UNOGame():
    def __init__(self):
        pygame.init()
        self.screen_width = 1000
        self.screen_height = 600
        background = pygame.image.load('./img/Main_background.png')
        self.background = pygame.transform.scale_by(background, (self.screen_width/800, self.screen_height/600))
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
    
    def set_start(self):
        pygame.init()
        self.background = pygame.image.load('./img/default.png')
        self.background = pygame.transform.scale_by(self.background, (self.screen_width/800, self.screen_height/600))
        self.screen.blit(self.background, (-100, -70))
        selected = 1

        while True:
            pygame.mixer.pre_init(44100, -16, 1, 512)
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
                        if selected >= 5:
                            selected = 5
                        else:
                            selected = selected + 1
                    if event.key == K_RETURN:
                        if selected <= 1:
                            self.playernum = 2
                            self.set_players(self.playernum)
                            self.background = pygame.image.load('./img/Main_background.png')
                        if selected == 2:
                            self.playernum = 3
                            self.set_players(self.playernum)
                            self.background = pygame.image.load('./img/Main_background.png')
                        if selected == 3:
                            self.playernum = 4
                            self.set_players(self.playernum)
                            self.background = pygame.image.load('./img/Main_background.png')
                        if selected == 4:
                            self.playernum = 5
                            self.set_players(self.playernum)
                            self.background = pygame.image.load('./img/Main_background.png')
                        if selected >= 5:
                            self.background = pygame.image.load('./img/Main_background.png')
                            self.background = pygame.transform.scale_by(self.background, (self.screen_width/800, self.screen_height/600))
                            return
                if event.type == MOUSEBUTTONDOWN:
                    mouse_pos = pygame.mouse.get_pos()
                    if two_rect.collidepoint(mouse_pos):
                        self.playernum = 2
                        selected = 1
                        self.set_players(self.playernum)
                    elif three_rect.collidepoint(mouse_pos):
                        self.playernum = 3
                        selected = 2
                        self.set_players(self.playernum)
                    elif four_rect.collidepoint(mouse_pos):
                        self.playernum = 4
                        selected = 3
                        self.set_players(self.playernum)
                    elif five_rect.collidepoint(mouse_pos):
                        self.playernum = 5
                        selected = 4
                        self.set_players(self.playernum)
                    elif quit_rect.collidepoint(mouse_pos):
                        selected = 5
                        self.background = pygame.image.load('./img/Main_background.png')
                        return
            # 선택한 글자의 색을 빨간색으로 표시      
            if selected == 1:
                text_two = self.text_format("2 PLAYERS", self.font, 50, (255,24,0))
            else:
                text_two = self.text_format("2 PLAYERS", self.font, 50, (0,0,0))
            if selected == 2:
                text_three = self.text_format("3 PLAYERS", self.font, 50, (255,24,0))
            else:
                text_three = self.text_format("3 PLAYERS", self.font, 50, (0,0,0))
            if selected == 3:
                text_four = self.text_format("4 PLAYERS", self.font, 50, (255,24,0))
            else:
                text_four = self.text_format("4 PLAYERS", self.font, 50, (0,0,0))                
            if selected == 4:
                text_five = self.text_format("5 PLAYERS", self.font, 50, (255,24,0))
            else:
                text_five = self.text_format("5 PLAYERS", self.font, 50, (0,0,0))
            if selected == 5:
                text_quit = self.text_format("BACK", self.font, 50, (255,24,0))
            else:
                text_quit = self.text_format("BACK", self.font, 50, (0,0,0))

            two_rect = text_two.get_rect()
            three_rect = text_three.get_rect()
            four_rect = text_four.get_rect()
            five_rect = text_five.get_rect()
            quit_rect = text_quit.get_rect()

            two_rect = pygame.Rect(int(self.screen_width*(275/800)), int(self.screen_height*(180/600)), 200, 50)
            three_rect = pygame.Rect(int(self.screen_width*(275/800)), int(self.screen_height*(240/600)), 200, 50)
            four_rect = pygame.Rect(int(self.screen_width*(275/800)), int(self.screen_height*(300/600)), 200, 50)
            five_rect = pygame.Rect(int(self.screen_width*(275/800)), int(self.screen_height*(360/600)), 200, 50)
            quit_rect = pygame.Rect(int(self.screen_width*(325/800)), int(self.screen_height*(420/600)), 200, 50)

            self.screen.blit(text_two, two_rect)
            self.screen.blit(text_three, three_rect)
            self.screen.blit(text_four, four_rect)
            self.screen.blit(text_five, five_rect)
            self.screen.blit(text_quit, quit_rect)
            pygame.display.update()

    def set_players(self, playernum):
        pygame.init()
        self.background = pygame.image.load('./img/default.png')
        self.background = pygame.transform.scale_by(self.background, (self.screen_width/800, self.screen_height/600))
        self.playernum = playernum
        self.screen.blit(self.background, (-100, -70))
        selected = 1
        while True:
            pygame.mixer.pre_init(44100, -16, 1, 512)
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
                        if selected >= self.playernum:
                            selected = self.playernum
                        else:
                            selected = selected + 1
                    if event.key == K_RETURN:
                        if selected <= 1:
                            self.background = pygame.image.load('./img/Main_background.png')
                            pass
                        if selected == 2:
                            self.background = pygame.image.load('./img/Main_background.png')
                            pass
                        if selected == 3:
                            self.background = pygame.image.load('./img/Main_background.png')
                            pass
                        if selected == 4:
                            self.background = pygame.image.load('./img/Main_background.png')
                            pass
                        if selected >= 5:
                            self.background = pygame.image.load('./img/Main_background.png')
                            pass
                if event.type == MOUSEBUTTONDOWN:
                    mouse_pos = pygame.mouse.get_pos()
                    if two_rect.collidepoint(mouse_pos):
                        selected = 1
                        pass
                    elif three_rect.collidepoint(mouse_pos):
                        selected = 2
                        pass
                    elif four_rect.collidepoint(mouse_pos):
                        selected = 3
                        pass
                    elif five_rect.collidepoint(mouse_pos):
                        selected = 4
                        pass
                    elif start_rect.collidepoint(mouse_pos):
                        selected = self.playernum
                        pass
            # 선택한 글자의 색을 빨간색으로 표시      
            if selected == 1:
                text_two = self.text_format("COM 1", self.font, 50, (255,24,0))
            else:
                text_two = self.text_format("COM 1", self.font, 50, (0,0,0))
            if selected == 2:
                text_three = self.text_format("COM 2", self.font, 50, (255,24,0))
            else:
                text_three = self.text_format("COM 2", self.font, 50, (0,0,0))
            if selected == 3:
                text_four = self.text_format("COM 3", self.font, 50, (255,24,0))
            else:
                text_four = self.text_format("COM 3", self.font, 50, (0,0,0))                
            if selected == 4:
                text_five = self.text_format("COM 4", self.font, 50, (255,24,0))
            else:
                text_five = self.text_format("COM 4", self.font, 50, (0,0,0))
            if selected == self.playernum:
                text_start = self.text_format("START", self.font, 50, (255,24,0))
            else:
                text_start = self.text_format("START", self.font, 50, (0,0,0))

            two_rect = pygame.Rect(int(self.screen_width*(320/800)), int(self.screen_height*(150/600)), 200, 50)
            three_rect = pygame.Rect(int(self.screen_width*(320/800)), int(self.screen_height*(210/600)), 200, 50)
            four_rect = pygame.Rect(int(self.screen_width*(320/800)), int(self.screen_height*(270/600)), 200, 50)
            five_rect = pygame.Rect(int(self.screen_width*(320/800)), int(self.screen_height*(330/600)), 200, 50)
            start_rect = pygame.Rect(int(self.screen_width*(320/800)), int(self.screen_height*(390/600)), 200, 50)

            if self.playernum == 2:
                self.screen.blit(text_two, two_rect)
                self.screen.blit(text_start, start_rect)
            elif self.playernum == 3:
                self.screen.blit(text_two, two_rect)
                self.screen.blit(text_three, three_rect)
                self.screen.blit(text_start, start_rect)
            elif self.playernum == 4:
                self.screen.blit(text_two, two_rect)
                self.screen.blit(text_three, three_rect)
                self.screen.blit(text_four, four_rect)
                self.screen.blit(text_start, start_rect)
            elif self.playernum == 5:
                self.screen.blit(text_two, two_rect)
                self.screen.blit(text_three, three_rect)
                self.screen.blit(text_four, four_rect)
                self.screen.blit(text_five, five_rect)
                self.screen.blit(text_start, start_rect)

            pygame.display.update()


    def main_menu(self):
        menu = True
        selected = 1

        start_rect = pygame.Rect(self.screen_width/2-50, int(self.screen_height*0.4), 200, 50)
        story_rect = pygame.Rect(self.screen_width/2-50, int(self.screen_height*0.5), 200, 50)
        set_rect = pygame.Rect(self.screen_width/2-50, int(self.screen_height*0.6), 200, 50)
        quit_rect = pygame.Rect(self.screen_width/2-50, int(self.screen_height*0.7), 200, 50)

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
                        if selected >= 4:
                            selected = 4
                        else:
                            selected = selected + 1
                    if event.key == K_RETURN: # K_RETURN은 엔터키
                        if selected <= 1:
                            self.set_start()
                            self.screen.blit(self.background, (-30, -30))
                        if selected == 2:
                            #실행할 내용
                            pass
                        if selected == 3:
                            #실행할 내용
                            pass
                        if selected >= 4:
                            pygame.quit()
                            sys.exit()
                if event.type == MOUSEBUTTONDOWN:
                    mouse_pos = pygame.mouse.get_pos()
                    if start_rect.collidepoint(mouse_pos):
                        selected = 1
                        self.set_start()
                        self.screen.blit(self.background, (-30, -30))
                    elif story_rect.collidepoint(mouse_pos):
                        selected = 2
                        pass
                    elif set_rect.collidepoint(mouse_pos):
                        selected = 3
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
                text_setting = self.text_format("SETTING", self.font, 50, (0,0,0))
            else:
                text_setting = self.text_format("SETTING", self.font, 50, (255, 255, 255))

            if selected == 4:
                text_quit = self.text_format("QUIT", self.font, 50, (0,0,0))
            else:
                text_quit = self.text_format("QUIT", self.font, 50, (255, 255, 255))

            # 메뉴 아이템 표시
            start_rect = text_start.get_rect()
            story_rect = text_story.get_rect()
            set_rect = text_setting.get_rect()
            quit_rect = text_quit.get_rect()

            start_rect = pygame.Rect(self.screen_width/2-50, int(self.screen_height*0.4), 200, 50)
            story_rect = pygame.Rect(self.screen_width/2-50, int(self.screen_height*0.5), 200, 50)          
            set_rect = pygame.Rect(self.screen_width/2-50, int(self.screen_height*0.6), 200, 50)
            quit_rect = pygame.Rect(self.screen_width/2-50, int(self.screen_height*0.7), 200, 50)

            self.screen.blit(text_start, start_rect)
            self.screen.blit(text_story, story_rect)
            self.screen.blit(text_setting, set_rect)
            self.screen.blit(text_quit, quit_rect)

            pygame.display.update()
            self.clock.tick(self.FPS)
            pygame.display.set_caption("UNO!")
    

def main():
    game = UNOGame() 
    game.main_menu()

if __name__ == '__main__': 
    main()