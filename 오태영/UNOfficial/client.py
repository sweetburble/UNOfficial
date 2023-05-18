import pygame
import sys
from pygame.locals import *
from network import Network
from functions import draw_text, text_format

# pygame.font.init()

# width = 700
# height = 700
# win = pygame.display.set_mode((width, height))
# pygame.display.set_caption("Client")

class Button:
    def __init__ (self, text, x, y, color):
        self.text = text
        self.x = x
        self.y = y
        self.color = color
        self.width = 150
        self.height = 100
    
    def draw(self, uno):
        pygame.draw.rect(uno.screen, self.color, (self.x, self.y, self.width, self.height))
        
        font = pygame.font.SysFont("comicsans", 40)
        text = font.render(self.text, 1, (255,255,255))
        uno.screen.blit(text, (self.x + round(self.width/2) - round(text.get_width()/2), self.y + round(self.height/2) - round(text.get_height()/2)))
    
    def click(self, pos): # pos = 마우스 위치
        x1 = pos[0]
        y1 = pos[1]
        
        if self.x <= x1 <= self.x + self.width and self.y <= y1 <= self.y + self.height:
            return True
        else:
            return False


def redrawWindow(uno, game, p):
    uno.screen.fill((128, 128, 128)) # 회색
    width, height = uno.screen_width, uno.screen_height

    if not(game.connected()):
        font = pygame.font.SysFont("comicsans", 80)
        text = font.render("Waiting for Player...", 1, (255,0,0), True)

        uno.screen.blit(text, (uno.screen_width/2 - text.get_width()/2, uno.screen_height/2 - text.get_height()/2))
    else:
        font = pygame.font.SysFont("comicsans", 60)
        text = font.render("MY Move", 1, (0,255,255))
        uno.screen.blit(text, (80, 200))

        text = font.render("Opponents", 1, (0,255,255))
        uno.screen.blit(text, (380, 200))

        move1 = game.get_player_move(0)
        move2 = game.get_player_move(1)
        if game.bothWent():
            text1 = font.render(move1, 1, (0,0,0))
            text2 = font.render(move2, 1, (0,0,0))
        else:
            if game.p1Went and p == 0:
                text1 = font.render(move1, 1, (0,0,0))
            elif game.p1Went:
                text1 = font.render("Locked In", 1, (0,0,0))
            else:
                text1 = font.render("Waiting...", 1, (0,0,0))
            
            if game.p2Went and p == 1:
                text2 = font.render(move2, 1, (0,0,0))
            elif game.p2Went:
                text2 = font.render("Locked In", 1, (0,0,0))
            else:
                text2 = font.render("Waiting...", 1, (0,0,0))

        if p == 1:
            uno.screen.blit(text2, (100, 350))
            uno.screen.blit(text1, (400, 350))
        else:
            uno.screen.blit(text1, (100, 350))
            uno.screen.blit(text2, (400, 350))
        
        for btn in btns:
            btn.draw(uno)
    
    pygame.display.update()

btns = [Button("Rock", 50, 500, (0,0,0)), Button("Scissors", 250, 500, (255,0,0)), Button("Paper", 450, 500, (0,255,0))]
def main(uno):
    run = True
    clock = pygame.time.Clock()
    n = Network()
    player = int(n.getP())
    print("You are player : ", player)

    while run:
        clock.tick(60)
        try: # 서버에서 게임 정보를 받아온다
            game = n.send("get")
        except: # 서버에서 게임 정보를 받아오지 못하면 종료
            run = False
            print("Couldn't get game")
            break
        
        if game.bothWent(): # 두 플레이어가 모두 선택했으면
            redrawWindow(uno, game, player) # 화면을 다시 그린다
            pygame.time.delay(200)
            try: # 서버에서 게임 정보를 받아온다
                game = n.send("reset")
            except:
                run = False
                print("Couldn't get game")
                break

            font = pygame.font.SysFont("comicsans", 90)
            if (game.winner() == 1 and player == 1) or (game.winner() == 0 and player == 0):
                text = font.render("You Won!", 1, (255,0,0))
            elif game.winner() == -1:
                text = font.render("Tie Game!", 1, (255,0,0))
            else:
                text = font.render("You Lost...", 1, (255,0,0))

            uno.screen.blit(text, (uno.screen_width/2 - text.get_width()/2, uno.screen_height/2 - text.get_height()/2))
            pygame.display.update()
            pygame.time.delay(2000)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                for btn in btns:
                    if btn.click(pos) and game.connected():
                        if player == 0:
                            if not game.p1Went:
                                n.send(btn.text)
                        else:
                            if not game.p2Went:
                                n.send(btn.text)
        
        redrawWindow(uno, game, player)

def select_screen(ess, uno, saves):
    pygame.init()
    selected = 0
    clock = pygame.time.Clock()

    while True:
        clock.tick(60)

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN:
                if event.key == saves["right"]:
                    selected = (selected + 1) % 2
                elif event.key == saves["left"]:
                    selected = (selected - 1) % 2
                elif event.key == saves["select"]:
                    if selected <= 0:
                        main(uno)
                    elif selected >= 1:
                        main(uno)
            if event.type == MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if server_rect.collidepoint(mouse_pos):
                    selected = 0
                    main(uno)
                elif client_rect.collidepoint(mouse_pos):
                    selected = 1
                    main(uno)
        
        uno.background = pygame.image.load('./images/Pause_background.jpg')
        uno.background = pygame.transform.scale_by(uno.background, (uno.screen_width/800, uno.screen_height/600))
        uno.screen.blit(uno.background, (-10, -10))
        
        draw_text(uno, "Select Server or Client", 50, (255, 0, 0), uno.screen_width*(250/1000), uno.screen_height*(200/600))

        text_server = text_format("Server", uno.font, 50, (255, 255, 255))
        text_client = text_format("Client", uno.font, 50, (255, 255, 255))

        if selected == 0:
            text_server = text_format("Server", uno.font, 50, (0, 0, 255))
        elif selected == 1:
            text_client = text_format("Client", uno.font, 50, (0, 0, 255))
        
        server_rect = text_server.get_rect()
        client_rect = text_client.get_rect()

        server_rect = pygame.Rect(uno.screen_width*(300/1000), uno.screen_height*(400/600), 200, 50)
        client_rect = pygame.Rect(uno.screen_width*(600/1000), uno.screen_height*(400/600), 200, 50)

        uno.screen.blit(text_server, server_rect)
        uno.screen.blit(text_client, client_rect)

        pygame.display.update()