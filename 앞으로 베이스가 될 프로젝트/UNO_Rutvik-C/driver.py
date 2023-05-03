from classes import *
from functions import *

pygame.init()

# classes.py의 클래스들의 객체를 생성
img = Image()
PM = PlayMode()
sound = Sound()
FONT = TextFont()
ess = Essentials()

# Creating root window
root = pygame.display.set_mode((1000, 600))
pygame.display.set_caption('UNO')
pygame.display.set_icon(img.icon)

# 배경음악 세팅
pygame.mixer.music.load(sound.back_g)
pygame.mixer.music.play(-1)  # 지속적인 배경음악 재생
pygame.mixer.music.set_volume(0.3)  # 배경음악 볼륨 세팅
music_on = True  # 모든 효과음/배경음악 상태를 저장하는 변수

# 초기 게임 변수 세팅
active = True  # 이 변수가 True이면 게임은 지속된다
ess.play_mode = PM.load  # 초기 play_mode는 "LOAD PAGE" -> 시작 화면이다

disp = False
win_dec = False  # 승자가 선언되면 True
pen_check = False  # UNO 페널티 체크 플래그

# 카드 덱을 세팅하고, 버려진 카드덱에 카드 한장 놓았고, 플레이어들에게 카드를 배분한다
create(ess)

# 게임 루프
while active:

    # 모든 발생하는 이벤트를 체크한다
    for event in pygame.event.get():
        # Quit button Check
        if event.type == pygame.QUIT:
            active = False

        # 마우스 클릭을 체크한다
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse = pygame.mouse.get_pos()  # 마우스 클릭 위치를 가져온다

            if ((20 < mouse[0] < 55 or 210 < mouse[0] < 245) and 150 < mouse[1] < 180) and ess.play_mode == PM.load: # 난이도 조절하는 < > 버튼
                if music_on:
                    sound.click.play()
                if ess.easy:
                    ess.easy = False
                else:
                    ess.easy = True

            if 0 < mouse[0] < 265 and 205 < mouse[1] < 270 and ess.play_mode == PM.load: # 플레이 버튼
                if music_on:
                    sound.click.play()
                ess.play_mode = PM.in_game # "IN GAME" 모드로 변경

            if 0 < mouse[0] < 265 and 340 < mouse[1] < 405 and ess.play_mode == PM.load: # 게임의 설명등이 담겨있는 info 버튼
                if music_on:
                    sound.click.play()
                ess.play_mode = PM.info

            if 10 < mouse[0] < 42 and 10 < mouse[1] < 42 and (
                    ess.play_mode == PM.in_game or ess.play_mode == PM.info): # 게임화면이나, Help 화면에서 뒤로가기 버튼
                if music_on:
                    sound.click.play()
                re_initialize(ess) # 게임을 모두 초기화하고, 다시 시작 화면으로 돌아가 초기화된 상태로 시작한다
                ess.play_mode = PM.load # "LOAD PAGE" = 시작 화면 모드로 변경
            # PM.win = "WINNER"
            if 420 < mouse[0] < 555 and 425 < mouse[1] < 543 and ess.play_mode == PM.win: # 게임이 누군가의 승리로 끝나면 보이는 홈 버튼
                if music_on:
                    sound.click.play()
                re_initialize(ess)
                win_dec = False # 다시 승자를 초기화
                ess.play_mode = PM.load

            if 960 < mouse[0] < 1000 and 0 < mouse[1] < 40:  # Music ON OFF 버튼
                if music_on:
                    sound.click.play()
                if music_on:
                    pygame.mixer.music.pause() # 배경음악 일시정지
                    music_on = False
                else:
                    pygame.mixer.music.unpause() # 배경음악 다시 재생
                    music_on = True

            if ess.player_playing:  # 유저가 카드 클릭 시, 동작 로직
                if 850 < mouse[0] < 916 and 500 < mouse[1] < 565:  # UNO 버튼 클릭
                    if music_on:
                        sound.uno.play()

                    ess.uno[0] = True

                if 775 < mouse[0] < 840 and 505 < mouse[1] < 570:  # 턴 종료 버튼
                    if music_on:
                        sound.click.play()
                    ess.player_playing = False # 유저의 턴이 끝났다는 것을 알린다

                for i in range(625, 625 - 50 * len(ess.player_list[0]), -50):  # 유저가 카드를 클릭했는지 감지
                    if i < mouse[0] < i + 50 and 470 < mouse[1] < 585:
                        play_this_card(ess, ess.player_list[0][int((625 - i) / 50)])
                        if music_on:
                            sound.card_played.play()

                if 340 < mouse[0] < 425 and 240 < mouse[1] < 355: # 낼 카드가 없어 덱에서 카드를 뽑을 때
                    take_from_stack(ess)
                    if music_on:
                        sound.card_drawn.play()

            # 이번 턴에 와일드 카드를 냈으면, 새로운 색깔 선택
            if ess.choose_color:
                if 395 < mouse[0] < 440 and 390 < mouse[1] < 450:  # 빨간색 버튼
                    ess.choose_color = False
                    play_this_card_2(ess, "Red")
                    if music_on:
                        sound.click.play()
                if 450 < mouse[0] < 495 and 390 < mouse[1] < 450:  # 초록색 버튼
                    ess.choose_color = False
                    play_this_card_2(ess, "Green")
                    if music_on:
                        sound.click.play()
                if 505 < mouse[0] < 550 and 390 < mouse[1] < 450:  # 파란색 버튼
                    ess.choose_color = False
                    play_this_card_2(ess, "Blue")
                    if music_on:
                        sound.click.play()
                if 560 < mouse[0] < 605 and 390 < mouse[1] < 450:  # 노란색 버튼
                    ess.choose_color = False
                    play_this_card_2(ess, "Yellow")
                    if music_on:
                        sound.click.play()

    # 시작 화면
    if ess.play_mode == PM.load:
        # 필수적인 이미지와 텍스트를 표시한다
        root.blit(img.load, (0, 0)) # 시작 화면의 배경 화면
        text = pygame.font.Font(FONT.joe_fin, 50).render("<", True, (255, 238, 46))
        root.blit(text, [20, 140])
        text = pygame.font.Font(FONT.joe_fin, 50).render(">", True, (255, 238, 46))
        root.blit(text, [220, 140])
        if ess.easy:
            text = pygame.font.Font(FONT.joe_fin, 30).render("EASY", True, (255, 238, 46))
            root.blit(text, [93, 153])
        else:
            text = pygame.font.Font(FONT.joe_fin, 30).render("HARD", True, (255, 238, 46))
            root.blit(text, [93, 153])

    # 게임 화면 
    elif ess.play_mode == PM.in_game:
        # 승자가 생겼는지 체크
        for i in ess.player_list:
            if len(i) == 0: # 플레이어의 카드가 0장이면 승자가 생긴 것
                win_dec = True
                ess.winner = ess.player_list.index(i) # 승자의 인덱스 저장
                break

        # 처음 덱 섞는 소리
        if ess.play_lag == -1 and music_on:
            sound.shuffled.play()

        # 필수적인 이미지 표현
        root.blit(img.bg, (0, 0))
        root.blit(img.back, (10, 10))
        root.blit(img.card_back, (340, 240))
        try: # 게임을 시작하면, 버려진 카드 덱에 놓이는 처음 카드 이미지를 표시한다
            root.blit(pygame.image.load("./images/" + ess.current[1] + str(ess.current[0]) + ".png"), (580, 240))
        except:
            root.blit(pygame.image.load("./images/" + ess.current[1] + ".png"), (580, 240))
        root.blit(img.p1, (290, 30))
        root.blit(img.p2, (865, 90))
        root.blit(img.p3, (55, 440))
        root.blit(img.p4, (675, 490))

        text = pygame.font.Font(FONT.joe_fin, 20).render("YOU", True, (255, 238, 46))
        root.blit(text, [690, 460])
        text = pygame.font.Font(FONT.joe_fin, 20).render(ess.bot_map[2], True, (255, 238, 46))
        root.blit(text, [295, 4])
        text = pygame.font.Font(FONT.joe_fin, 20).render(ess.bot_map[3], True, (255, 238, 46))
        root.blit(text, [870, 60])
        text = pygame.font.Font(FONT.joe_fin, 20).render(ess.bot_map[1], True, (255, 238, 46))
        root.blit(text, [60, 410])

        text = pygame.font.Font(FONT.joe_fin, 20).render(ess.message, True, (255, 238, 46))
        root.blit(text, [340, 210])

        # 각 플레이어들의 초기 카드 배치
        for i in range(len(ess.player_list[1])):
            root.blit(img.card_back_l, (40, 315 - 30 * i)) # Back_left.png
        for i in range(len(ess.player_list[2])):
            root.blit(img.card_back_i, (380 + 30 * i, 20)) # Back_inverted.png
        for i in range(len(ess.player_list[3])):
            root.blit(img.card_back_r, (845, 190 + 30 * i)) # Back_right.png
        for i in range(len(ess.player_list[0])):
            root.blit(
                pygame.image.load("./images/" + ess.player_list[0][i][1] + str(ess.player_list[0][i][0]) + ".png"),
                (590 - 50 * i, 470))

        if ess.choose_color: # 유저가 와일드 카드를 냈으면, 색깔을 선택할 수 있게 이미지를 표시한다
            root.blit(img.red, (395, 390))
            root.blit(img.green, (450, 390))
            root.blit(img.blue, (505, 390))
            root.blit(img.yellow, (560, 390))

        root.blit(img.uno_button, (850, 500)) # -> 일단 플레이어의 UNO 버튼은 항상 표시되게 함

        # Play Flow, 플레이 흐름
        if ess.player_playing: # 유저가 플레이하고 있으면 True, 아니면 False
            ess.message = ""

            if not ess.drawn and not ess.played:  # Checking for previous special card overheads, 이전에 기술 카드를 냈는지 확인
                if ess.current[0] == '+2' and ess.special_check == 0:  # Draw 2
                    for _ in range(2):
                        try:
                            ess.player_list[0].append(ess.deck1.pop())
                        except:
                            ess.deck1, ess.deck2 = ess.deck2, ess.deck1
                            random.shuffle(ess.deck1)
                            ess.player_list[0].append(ess.deck1.pop())
                    ess.special_check = 1
                    ess.player_playing = False

                elif ess.current[0] == '+4' and ess.special_check == 0:  # Draw 4
                    for _ in range(4):
                        try:
                            ess.player_list[0].append(ess.deck1.pop())
                        except:
                            ess.deck1, ess.deck2 = ess.deck2, ess.deck1
                            random.shuffle(ess.deck1)
                            ess.player_list[0].append(ess.deck1.pop())
                    ess.special_check = 1
                    ess.player_playing = False

            # img.line은 현재 플레이 해야할 플레이어를 표시하고, 유저는 체크 버튼과 UNO 버튼이 추가로 표시된다
            root.blit(img.line, (682, 550))
            root.blit(img.done, (775, 505))
            # root.blit(img.uno_button, (850, 500)) -> 일단 플레이어의 UNO 버튼은 항상 표시되게 함

        else: # AI가 플레이 중이면
            if ess.play_lag == 140:  # 플레이어 간의 행동 사이에 지연을 구현한다
                disp = False
                pen_check = False

                # 다음 플레이어를 결정한다
                set_curr_player(ess, True)

                # 그게 유저의 턴이면
                if ess.position == 0:
                    ess.uno[0] = False # 유자 플레이어가 UNO를 외쳤는지 저장하는 플래그를 초기화한다
                    ess.player_playing = True # 유저가 플레이 중임을 표시한다

                else: # 다음 플레이어가 AI라면
                    # 일단 유저의 플래그를 초기화한다
                    ess.played = False
                    ess.drawn = False

                    # 그 다음 AI의 행동을 결정한다
                    bot_action(ess, sound)

                ess.play_lag = 0  # 랙 리셋

            else: # 아직 1.4초 안 지났으면
                if win_dec and ess.play_lag == 70:  # 게임의 승자 선언을 0.7초 지연한다
                    ess.play_mode = PM.win

                if not pen_check: # 페널티 체크 플래그, 게임이 처음 시작할 때는 False였다
                    if ess.position != -1 and len(ess.player_list[ess.position]) == 1 and not ess.uno[ess.position]: # 1장 남았는데, UNO를 외치지 않으면
                        for j in range(4):
                            if ess.position != j: # 다른 플레이어들의 카드를 한 장씩 가져온다
                                ess.player_list[ess.position].append(ess.player_list[j].pop())

                        ess.message = "Penalty!"
                        ess.uno[ess.position] = True
                    pen_check = True

                ess.play_lag += 1 # 게임의 FPS마다 1씩 증가한다

                if not disp: # disp을 True로 한다?
                    disp = True

                # 현재 턴의 플레이어를 표시한다
                if (ess.position + ess.direction_check) % 4 == 1:
                    root.blit(img.line, (67, 512))
                elif (ess.position + ess.direction_check) % 4 == 2:
                    root.blit(img.line, (293, 85))
                elif (ess.position + ess.direction_check) % 4 == 3:
                    root.blit(img.line, (870, 145))

    # HELP 화면
    elif ess.play_mode == PM.info:
        root.blit(img.help, (0, 0))
        root.blit(img.back, (10, 10))

    # 게임 승리 화면
    elif ess.play_mode == PM.win and ess.winner != -1:
        # sounds
        if music_on:
            sound.victory.play()

        # 적절한 메시지를 생성한다
        string = ""
        if ess.winner == 0:
            string = "Well Done! You've Won this Round!"
        else:
            string = "%s has won this Round" % ess.bot_map[ess.winner]

        # 이미지를 렌더링한다
        root.blit(img.win, (0, 0))
        text = pygame.font.Font(FONT.pacifico, 40).render(string, True, (255, 238, 46))
        root.blit(text, [190, 100])

    # 배경음악 / 효과음 토글 버튼
    if music_on:
        root.blit(img.mute, (960, 8))
    else:
        root.blit(img.unmute, (960, 8))

    # 화면 지속적으로 갱신
    pygame.display.update()
