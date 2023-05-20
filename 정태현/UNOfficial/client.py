import pygame
import sys
from pygame.locals import *
from network import Network
from functions import draw_text, text_format
from singleplay import Make_Rect
from game import check_winner

def drawWindow(uno, img, game, player, selected_card):
    width, height = uno.screen_width, uno.screen_height # 화면 크기

    if player == 0: # 다른 플레이어의 인덱스 선언
        other = 1
    else:
        other = 0

    if not(game.connected()):
        uno.screen.fill((128, 128, 128)) # 회색 배경
        font = pygame.font.SysFont("comicsans", 80)
        text = font.render("Waiting for Player...", 1, (255,0,0), True)

        uno.screen.blit(text, (width*(150/1000), height*(200/600)))
    else:
        # 필수적인 이미지 표현
        uno.screen.blit(img.bg, (0, 0)) # 배경 화면
        uno.screen.blit(img.pause, (width*(10/1000), height*(10/1000))) # 일시 정지 버튼
        uno.screen.blit(img.card_back, (width*(140/1000), height*(140/600))) # 카드 덱 이미지
        uno.screen.blit(img.uno_button, (width*(640/1000), height*(500/600))) # -> 일단 플레이어의 UNO 버튼은 항상 표시되게 함

        try: # 게임을 시작하면, 버려진 카드 덱에 놓이는 처음 카드 이미지를 표시한다
            uno.screen.blit(pygame.image.load("./images/original/" + game.current[1] + str(game.current[0]) + ".png"), (width*(380/1000), height*(140/600)))
        except:
            uno.screen.blit(pygame.image.load("./images/original/" + game.current[1] + ".png"), (width*(380/1000), height*(140/600)))

        if player == 0: # 플레이어가 0번 플레이어일 경우 이미지
            uno.screen.blit(img.p_user, (width*(475/1000), height*(490/600)))
        else: # 플레이어가 1번 플레이어일 경우 이미지
            uno.screen.blit(img.p1, (width*(475/1000), height*(490/600)))
        
        text_user = pygame.font.Font("./fonts/JosefinSans-Bold.ttf", int(height*(20/600))).render(game.player_mapp[player], True, (255, 238, 46))
        uno.screen.blit(text_user, [width*(490/1000), height*(460/600)]) # 유저 이름 텍스트
        
        for i in range(len(game.player_list[player])):
            x_diff = i % 10
            y_diff = i // 10
            if (selected_card == i): # 카드 선택 애니메이션 구현
                uno.screen.blit(pygame.image.load("./images/original/" + game.player_list[player][i][1] + str(game.player_list[player][i][0]) + ".png"), (width*((390 - 30 * x_diff)/1000), height*((480 - 80 * y_diff)/600)))
            else:
                uno.screen.blit(pygame.image.load("./images/original/" + game.player_list[player][i][1] + str(game.player_list[player][i][0]) + ".png"), (width*((390 - 30 * x_diff)/1000), height*((520 - 80 * y_diff)/600)))
        # 카드 선택의 가시성을 위해 선택된 카드를 한 번 다시 그렸다
        uno.screen.blit(pygame.image.load("./images/original/" + game.player_list[player][selected_card][1] + str(game.player_list[player][selected_card][0]) + ".png"), (width*((390 - 30 * (selected_card % 10))/1000), height*((480 - 80 * (selected_card // 10))/600)))
        
        if player == 0:
            text_other = pygame.font.Font("./fonts/JosefinSans-Bold.ttf", int(height*(20/600))).render(game.player_mapp[1], True, (255, 238, 46))
        else:
            text_other = pygame.font.Font("./fonts/JosefinSans-Bold.ttf", int(height*(20/600))).render(game.player_mapp[0], True, (255, 238, 46))
        text_p2 = pygame.font.Font("./fonts/JosefinSans-Bold.ttf", int(height*(20/600))).render(game.player_mapp[2], True, (255, 238, 46))
        text_p3 = pygame.font.Font("./fonts/JosefinSans-Bold.ttf", int(height*(20/600))).render(game.player_mapp[3], True, (255, 238, 46))

        # 다른 플레이어들의 초기 카드 이미지 표시 -> 컴퓨터의 카드가 11장 이상이면 카드 이미지 x 숫자로 표시
        if game.player_num >= 2:
            uno.screen.blit(img.p1, (width*(940/1000), height*(10/600))) # 다른 플레이어 이미지
            uno.screen.blit(text_other, [width*(860/1000), height*(10/600)]) # 다른 플레이어 이름
            if len(game.player_list[other]) >= 11: 
                uno.screen.blit(img.card_back_computer, [width*(800/1000), height*(60/600)])
                draw_text(uno, ("x " + str(len(game.player_list[other]))), 40, (0, 0, 255), width*(850/1000), height*(70/600))
            else:
                for i in range(len(game.player_list[other])): # 다른 플레이어의 카드 이미지
                    uno.screen.blit(img.card_back_computer, (width*((940 - 20 * i)/1000), height*(60/600)))
            if game.player_num >= 3:
                uno.screen.blit(img.p2, (width*(940/1000), height*(130/600))) # EDITH 이미지
                uno.screen.blit(text_p2, [width*(860/1000), height*(130/600)]) # EDITH 이름 표시
                if len(game.player_list[2]) >= 11:
                    uno.screen.blit(img.card_back_computer, [width*(800/1000), height*(180/600)])
                    draw_text(uno, ("x " + str(len(game.player_list[2]))), 40, (0, 0, 255), width*(850/1000), height*(190/600))
                else:
                    for i in range(len(game.player_list[2])): # EDITH의 카드 이미지
                        uno.screen.blit(img.card_back_computer, (width*((940 - 20 * i)/1000), height*(180/600)))
                if game.player_num == 4:
                    uno.screen.blit(img.p3, (width*(940/1000), height*(250/600))) # FRIDAY 이미지
                    uno.screen.blit(text_p3, [width*(860/1000), height*(250/600)]) # FRIDAY 이름 표시
                    if len(game.player_list[3]) >= 11:
                        uno.screen.blit(img.card_back_computer, [width*(800/1000), height*(300/600)])
                        draw_text(uno, ("x " + str(len(game.player_list[3]))), 40, (0, 0, 255), width*(850/1000), height*(310/600))
                    else:
                        for i in range(len(game.player_list[3])): # FRIDAY의 카드 이미지
                            uno.screen.blit(img.card_back_computer, (width*((940 - 20 * i)/1000), height*(300/600)))

        text = pygame.font.Font("./fonts/JosefinSans-Bold.ttf", int(height*(30/600))).render(game.message, True, (255, 238, 46))
        uno.screen.blit(text, [width*(140/1000), height*(100/600)]) # 게임 진행 메시지

        if game.position == player:
            # img.line은 현재 플레이 해야할 플레이어를 표시하고, 유저는 체크 버튼이 추가로 표시된다
            uno.screen.blit(img.line, (width*(482/1000), height*(550/600)))
            uno.screen.blit(img.done, (width*(565/1000), height*(505/600)))
        elif game.position == other:
            uno.screen.blit(img.line, (width*(860/1000), height*(10/600)))
        else:
            for i in range(2, 4):
                if i == game.position:
                    uno.screen.blit(img.line, (width*(860/1000), height*((-110 + i * 120)/600)))


    pygame.display.update() # 화면 갱신

def main(ess, uno, sound, img, saves):
    run = True
    clock = pygame.time.Clock()
    n = Network()
    player = int(n.getP())
    print("You are player : ", player)

    width, height = uno.screen_width, uno.screen_height # 화면 크기
    selected_card = 0 # 선택한 카드의 인덱스

    First_connect = True # 처음 접속 여부

    while run:
        clock.tick(60)
        try: # 서버에서 게임 정보를 받아온다
            game = n.send("get")
        except: # 서버에서 게임 정보를 받아오지 못하면 종료
            run = False
            print("Couldn't get game")
            break
        
        # if game.connected() and First_connect == True: # 게임이 진행중이면
        #     game = n.send("game_start")
        #     First_connect = False

        # if not(game.connected()): # 게임이 시작되면
        #     pass
        # else:
        #     if player == 0 and First_connect == True: # 플레이어가 0번이면
        #         n.send("next_turn")

        if check_winner(game): # 게임의 승자가 결정되면
            drawWindow(uno, img, game, player) # 화면을 다시 그린다

            pygame.time.delay(200)
            try: # 서버에서 게임 정보를 받아온다
                game = n.send("reset")
            except:
                run = False
                print("Couldn't get game")
                break

            sound.victory.play() # 승리 효과음을 재생
            string = ""
            if (game.winner == 0 and player == 0) or (game.winner == 1 and player == 1): # 그리고 적절한 메시지를 생성
                string = "Well Done! You've Won this Round!"
            else:
                string = "%s has won this Round" % game.player_mapp[game.winner]

            # 이미지와 메시지를 렌더링한다
            uno.screen.blit(img.win, (0, 0))
            text = pygame.font.Font("./fonts/Pacifico.ttf", int(height*(40/600))).render(string, True, (255, 238, 46))
            uno.screen.blit(text, [width*(190/1000), height*(100/600)])

            pygame.display.update()
            pygame.time.delay(2000)
        
        for event in pygame.event.get():
            if event.type == QUIT:
                run = False
                pygame.quit()
                sys.exit()

            if event.type == KEYDOWN:
                # 클라이언트의 턴이어야 키 입력을 받는다
                if (game.p1_player_playing and player == 0) or (game.p2_player_playing and player == 1):
                    if event.key == saves["up"]: # 선택한 카드를 낸다
                        card = ":".join(game.player_list[player][selected_card]) # 튜플을 문자열로 변환
                        
                        n.send(card) # "+4:Red" 형식으로 서버에 전송
                        
                        sound.card_played.play()
                        selected_card = 0 # 카드를 낸 뒤에는 선택한 카드를 초기화
                    elif event.key == saves["down"]: # 덱에서 카드 한장 드로우
                        n.send("draw")
                        sound.card_drawn.play()
                    elif event.key == saves["select"]: # 턴을 넘긴다
                        n.send("next_turn")
                        sound.click.play()
                if event.key == saves["left"]: # 왼쪽으로 카드 선택
                    if (selected_card >= len(game.player_list[player]) - 1):
                        selected_card = 0
                    else:
                        selected_card += 1
                elif event.key == saves["right"]: # 오른쪽으로 카드 선택
                    if (selected_card <= 0):
                        selected_card = len(game.player_list[player]) - 1
                    else:
                        selected_card -= 1
                elif event.key == K_ESCAPE: # ESC 버튼을 누르면 게임이 일시정지됨
                    pass
            if event.type == MOUSEMOTION:
                mouse_pos = pygame.mouse.get_pos()
                if (game.p1_player_playing and player == 0) or (game.p2_player_playing and player == 1):
                    # 1) 유저가 카드 위에 마우스를 올려놓았을 때
                    for i in range(int((width/1000)*410), int((width/1000)*410 - 30 * len(game.player_list[player])), -30):
                        if i < mouse_pos[0] < (i + 30) and height*(520/600) < mouse_pos[1] < height*(590/600):
                            selected_card = int(((width/1000)*425 - i) / 30)
            # 클라이언트의 턴이어야 마우스 입력을 받는다
            if event.type == MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if (game.p1_player_playing and player == 0) or (game.p2_player_playing and player == 1):
                    if uno_button_rect.collidepoint(mouse_pos): # 1) UNO 버튼을 클릭
                        sound.uno.play()
                        n.send("shout_uno")
                    if play_done_rect.collidepoint(mouse_pos): # 2) 턴 종료 버튼을 클릭
                        sound.click.play()
                        n.send("next_turn")
                    # 3) 낼 카드가 없어 덱에서 카드를 뽑을 때
                    elif card_deck_rect.collidepoint(mouse_pos):
                        sound.card_drawn.play()
                        n.send("draw")

                    # 4) 유저가 카드를 클릭했는지 감지
                    for i in range(int((width/1000)*410), int((width/1000)*410 - 30 * len(game.player_list[0])), -30):
                        if i < mouse_pos[0] < (i + 30) and height*(520/600) < mouse_pos[1] < height*(590/600):
                            card = ":".join(game.player_list[player][selected_card]) # 튜플을 문자열로 변환
                            
                            sound.card_played.play()
                            n.send(card)
                            
                            selected_card = 0 # 카드를 낸 뒤에는 선택한 카드를 초기화

                # 5) 이번 턴에 와일드 카드를 냈으면, 새로운 색깔 선택
                if (((game.p1_player_playing and player == 0) or (game.p2_player_playing and player == 1)) and game.choose_colors[player] == True):
                    if width*(395/1000) < mouse_pos[0] < width*(440/1000) and height*(390/600) < mouse_pos[1] < height*(450/600): # 빨간색 버튼
                        n.send("Red")
                        sound.click.play()
                    if width*(450/1000) < mouse_pos[0] < width*(495/1000) and height*(390/600) < mouse_pos[1] < height*(450/600): # 초록색 버튼
                        n.send("Green")
                        sound.click.play()
                    if width*(505/1000) < mouse_pos[0] < width*(550/1000) and height*(390/600) < mouse_pos[1] < height*(450/600): # 파란색 버튼
                        n.send("Blue")
                        sound.click.play()
                    if width*(560/1000) < mouse_pos[0] < width*(605/1000) and height*(390/600) < mouse_pos[1] < height*(450/600): # 노란색 버튼
                        n.send("Yellow")
                        sound.click.play()
        
        # pause_button_rect = Make_Rect(uno, 10, 10, 32, 32)
        uno_button_rect = Make_Rect(uno, 640, 500, 64, 64)
        play_done_rect = Make_Rect(uno, 565, 505, 64, 64)
        card_deck_rect = Make_Rect(uno, 140, 140, 85, 115)
        
        drawWindow(uno, img, game, player, selected_card)

def select_screen(ess, uno, sound, img, saves):
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
                        main(ess, uno, sound, img, saves)
                    elif selected >= 1:
                        main(ess, uno, sound, img, saves)
            if event.type == MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if server_rect.collidepoint(mouse_pos):
                    selected = 0
                    main(ess, uno, sound, img, saves)
                elif client_rect.collidepoint(mouse_pos):
                    selected = 1
                    main(ess, uno, sound, img, saves)
        
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