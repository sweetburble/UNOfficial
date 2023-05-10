from classes import *
from functions import *
from settings import *

pygame.init()

# classes.py의 클래스들의 객체를 생성
img = Image()
PM = PlayMode()
sound = Sound()
FONT = TextFont()
ess = Essentials()
uno = UNOGame()
STORY = StoryMode()

# 파일 아이콘 설정
pygame.display.set_icon(img.icon)

# 배경음악 & 환경음 세팅
pygame.mixer.music.load(sound.back_g)
pygame.mixer.music.play(-1)  # 지속적인 배경음악 재생
pygame.mixer.music.set_volume(saves["background"])  # 배경음악 볼륨 세팅
volumesetting(sound, saves["effects"])

music_on = True  # 모든 효과음/배경음악 상태를 저장하는 변수

# 초기 게임 변수 세팅
active = True  # 이 변수가 True이면 게임은 지속된다
ess.play_mode = PM.load  # 초기 play_mode는 "LOAD PAGE" -> 시작 화면이다

disp = False
win_dec = False  # 승자가 선언되면 True
pen_check = False  # UNO 페널티 체크 플래그

# 타이머 변수 세팅
max_time = 10 # 플레이어에게 10초의 시간을 주고, 그 시간 안에 카드를 내지 않으면 자동으로 턴이 넘어간다

# 게임 루프
while True:
    # 모든 발생하는 이벤트를 체크한다
    for event in pygame.event.get():
        # Quit 버튼
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        # 마우스 클릭을 체크한다
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse = pygame.mouse.get_pos()  # 마우스 클릭 위치를 가져온다

            if width*(10/1000) < mouse[0] < width*(42/1000) and height*(10/600) < mouse[1] < height*(42/1000) and (
                    ess.play_mode == PM.in_game or ess.play_mode == PM.setting): # 게임화면이나, Help 화면에서 뒤로가기 버튼
                if music_on:
                    sound.click.play()
                re_initialize(ess, uno) # 게임을 모두 초기화하고, 다시 시작 화면으로 돌아가 초기화된 상태로 시작한다
                uno.background = pygame.image.load('./images/Main_background.png')
                uno.background = pygame.transform.scale_by(uno.background, (uno.screen_width/800, uno.screen_height/600))
                uno.screen.blit(uno.background, (-30, -30))
                ess.play_mode = PM.load # "LOAD PAGE" = 시작 화면 모드로 변경
            
            # PM.win = "WINNER"
            if width*(420/1000) < mouse[0] < width*(555/1000) and height*(425/600) < mouse[1] < height*(543/600) and ess.play_mode == PM.win: # 게임이 누군가의 승리로 끝나면 보이는 홈 버튼
                if music_on:
                    sound.click.play()
                re_initialize(ess, uno)
                uno.background = pygame.image.load('./images/Main_background.png')
                uno.background = pygame.transform.scale_by(uno.background, (uno.screen_width/800, uno.screen_height/600))
                uno.screen.blit(uno.background, (-30, -30))
                win_dec = False # 다시 승자를 초기화
                ess.play_mode = PM.load

            if width*(60/1000) < mouse[0] < width*(100/1000) and 0 < mouse[1] < height*(40/600):  # Music ON OFF 버튼
                if music_on:
                    sound.click.play()
                if music_on:
                    pygame.mixer.music.pause() # 배경음악 일시정지
                    music_on = False
                else:
                    pygame.mixer.music.unpause() # 배경음악 다시 재생
                    music_on = True

            if ess.player_playing:  # 유저가 플레이 중일 때, 동작 로직
                if width*(640/1000) < mouse[0] < width*(706/1000) and height*(500/600) < mouse[1] < height*(565/600):  
                    # UNO 버튼 클릭
                    if music_on:
                        sound.uno.play()

                    ess.shouted_uno[0] = True

                # 턴 종료 버튼
                if width*(565/1000) < mouse[0] < width*(630/1000) and height*(505/600) < mouse[1] < height*(570/600): 
                    if music_on:
                        sound.click.play()
                    ess.player_playing = False # 유저의 턴이 끝났다는 것을 알린다
                    ess.play_lag = 0

                for i in range(int((width/1000)*425), int((width/1000)*425 - 50 * len(ess.player_list[0])), -50): # 유저가 카드를 클릭했는지 감지
                    if i < mouse[0] < (i + 50) and height*(470/600) < mouse[1] < height*(585/600):
                        play_this_card(ess, uno, ess.player_list[0][int(((width/1000)*425 - i) / 50)])
                        if music_on:
                            sound.card_played.play()

                if width*(140/1000) < mouse[0] < width*(225/1000) and height*(140/600) < mouse[1] < height*(255/600): # 낼 카드가 없어 덱에서 카드를 뽑을 때
                    take_from_stack(ess)
                    if music_on:
                        sound.card_drawn.play()

            # 이번 턴에 와일드 카드를 냈으면, 새로운 색깔 선택
            if ess.choose_color:
                if width*(395/1000) < mouse[0] < width*(440/1000) and height*(390/600) < mouse[1] < height*(450/600):  # 빨간색 버튼
                    ess.choose_color = False
                    play_this_card_2(ess, "Red")
                    if music_on:
                        sound.click.play()
                if width*(450/1000) < mouse[0] < width*(495/1000) and height*(390/600) < mouse[1] < height*(450/600):  # 초록색 버튼
                    ess.choose_color = False
                    play_this_card_2(ess, "Green")
                    if music_on:
                        sound.click.play()
                if width*(505/1000) < mouse[0] < width*(550/1000) and height*(390/600) < mouse[1] < height*(450/600):  # 파란색 버튼
                    ess.choose_color = False
                    play_this_card_2(ess, "Blue")
                    if music_on:
                        sound.click.play()
                if width*(560/1000) < mouse[0] < width*(605/1000) and height*(390/600) < mouse[1] < height*(450/600):  # 노란색 버튼
                    ess.choose_color = False
                    play_this_card_2(ess, "Yellow")
                    if music_on:
                        sound.click.play()

    # 시작 화면
    if ess.play_mode == PM.load:
        function_key_config() # 키 설정을 불러온다
        pygame.mixer.music.set_volume(saves["background"]) # 배경음악과 효과음 설정을 적용한다
        volumesetting(sound, saves["effects"])

        main_menu(ess, uno, STORY) # 필수적인 이미지와 텍스트를 표시한다

    # 게임 화면 
    elif ess.play_mode == PM.in_game:
        
        # 승자가 생겼는지 체크
        for idx, item in enumerate(ess.player_list):
            if len(item) == 0: # 플레이어의 카드가 0장이면 게임에서 승리한다.
                win_dec = True
                ess.winner = idx # 승자의 인덱스 저장
                break

        # 처음 덱 섞는 소리
        if ess.play_lag == -1 and music_on:
            sound.shuffled.play()

        # 필수적인 이미지 표현
        uno.screen.blit(img.bg, (0, 0))
        uno.screen.blit(img.back, (width*(10/1000), height*(10/1000))) # 뒤로가기 버튼
        uno.screen.blit(img.card_back, (width*(140/1000), height*(140/600))) # 카드 덱 이미지
        
        try: # 게임을 시작하면, 버려진 카드 덱에 놓이는 처음 카드 이미지를 표시한다
            uno.screen.blit(pygame.image.load("./images/" + ess.current[1] + str(ess.current[0]) + ".png"), (width*(380/1000), height*(140/600)))
        except:
            uno.screen.blit(pygame.image.load("./images/" + ess.current[1] + ".png"), (width*(380/1000), height*(140/600)))
        
        # 유저와 컴퓨터 플레이어의 이미지를 표현한다
        uno.screen.blit(img.p_user, (width*(475/1000), height*(490/600))) # 유저 플레이어 이미지
        
        text_user = pygame.font.Font(FONT.joe_fin, int(height*(20/600))).render(ess.bot_map[6], True, (255, 238, 46))
        uno.screen.blit(text_user, [width*(490/1000), height*(460/600)]) # 유저 이름 텍스트
        
        for i in range(len(ess.player_list[0])): # 유저 플레이어의 카드 이미지
            uno.screen.blit(
                pygame.image.load("./images/" + ess.player_list[0][i][1] + str(ess.player_list[0][i][0]) + ".png"), (width*((390 - 50 * i)/1000), height*(470/600)))

        text_p1 = pygame.font.Font(FONT.joe_fin, int(height*(20/600))).render(ess.bot_map[1], True, (255, 238, 46))
        text_p2 = pygame.font.Font(FONT.joe_fin, int(height*(20/600))).render(ess.bot_map[2], True, (255, 238, 46))
        text_p3 = pygame.font.Font(FONT.joe_fin, int(height*(20/600))).render(ess.bot_map[3], True, (255, 238, 46))
        text_p4 = pygame.font.Font(FONT.joe_fin, int(height*(20/600))).render(ess.bot_map[4], True, (255, 238, 46))
        text_p5 = pygame.font.Font(FONT.joe_fin, int(height*(20/600))).render(ess.bot_map[5], True, (255, 238, 46))

        # 컴퓨터 플레이어들의 초기 카드 이미지 표시 -> Back_computer.png
        if uno.player_num >= 2:
            uno.screen.blit(img.p1, (width*(940/1000), height*(10/600))) # JARVIS 이미지
            uno.screen.blit(text_p1, [width*(860/1000), height*(10/600)]) # JARVIS 텍스트 표시
            for i in range(len(ess.player_list[1])): # JARVIS의 카드 이미지
                uno.screen.blit(img.card_back_computer, (width*((940 - 20 * i)/1000), height*(60/600)))
            if uno.player_num >= 3:
                uno.screen.blit(img.p2, (width*(940/1000), height*(130/600))) # EDITH 이미지
                uno.screen.blit(text_p2, [width*(860/1000), height*(130/600)]) # EDITH 텍스트 표시
                for i in range(len(ess.player_list[2])): # EDITH의 카드 이미지
                    uno.screen.blit(img.card_back_computer, (width*((940 - 20 * i)/1000), height*(180/600)))
                if uno.player_num >= 4:
                    uno.screen.blit(img.p3, (width*(940/1000), height*(250/600))) # FRIDAY 이미지
                    uno.screen.blit(text_p3, [width*(860/1000), height*(250/600)]) # FRIDAY 텍스트 표시
                    for i in range(len(ess.player_list[3])): # FRIDAY의 카드 이미지
                        uno.screen.blit(img.card_back_computer, (width*((940 - 20 * i)/1000), height*(300/600)))
                    if uno.player_num >= 5:
                        uno.screen.blit(img.p4, (width*(940/1000), height*(370/600))) # BRIAN 이미지
                        uno.screen.blit(text_p4, [width*(860/1000), height*(370/600)]) # BRIAN 텍스트 표시
                        for i in range(len(ess.player_list[4])): # BRIAN의 카드 이미지
                            uno.screen.blit(img.card_back_computer, (width*((940 - 20 * i)/1000), height*(420/600)))
                        if uno.player_num == 6:
                            uno.screen.blit(img.p5, (width*(940/1000), height*(490/600))) # SWIFT 이미지
                            uno.screen.blit(text_p5, [width*(860/1000), height*(490/600)]) # SWIFT 텍스트 표시
                            for i in range(len(ess.player_list[5])): # SWIFT의 카드 이미지
                                uno.screen.blit(img.card_back_computer, (width*((940 - 20 * i)/1000), height*(540/600)))

        text = pygame.font.Font(FONT.joe_fin, int(height*(20/600))).render(ess.message, True, (255, 238, 46))
        uno.screen.blit(text, [width*(140/1000), height*(110/600)]) # 게임 진행 메시지

        if ess.choose_color: # 유저가 와일드 카드를 냈으면, 색깔을 선택할 수 있게 이미지를 표시한다
            uno.screen.blit(img.red, (width*(395/1000), height*(390/600)))
            uno.screen.blit(img.green, (width*(450/1000), height*(390/600)))
            uno.screen.blit(img.blue, (width*(505/1000), height*(390/600)))
            uno.screen.blit(img.yellow, (width*(560/1000), height*(390/600)))

        uno.screen.blit(img.uno_button, (width*(640/1000), height*(500/600))) # -> 일단 플레이어의 UNO 버튼은 항상 표시되게 함

        # 각 플레이어가 UNO를 외쳤다면, UNO 이미지를 표시한다
        if ess.shouted_uno[0] == True:
            uno.screen.blit(img.shouted, (width*(490/1000), height*(400/600)))
        for i in range(1, uno.player_num):
            if (ess.shouted_uno[i] == True):
                uno.screen.blit(img.shouted, (width*(800/1000), height*(120 * (i - 1)/600)))

        # Play Flow, 플레이 흐름
        if ess.player_playing: # 유저가 플레이하고 있으면 True, 아니면 False
            if ess.play_lag == 400: # 약 10초 타이머
                ess.player_playing = False
                ess.play_lag = 0
            else:
                text = pygame.font.Font(FONT.joe_fin, int(height*(20/600))).render(str(max_time - ess.play_lag//40), True, (255, 238, 46))
                uno.screen.blit(text, [width*(550/1000), height*(460/600)])
                
                ess.message = ""

                if not ess.drawn and not ess.played:  # Checking for previous special card overheads, 이전에 기술 카드를 냈는지 확인

                    if ess.current[0] == '+1' and ess.special_check == 0:  # Draw 1
                        for _ in range(1):
                            try:
                                ess.player_list[0].append(ess.deck1.pop())
                            except:
                                ess.deck1, ess.deck2 = ess.deck2, ess.deck1
                                random.shuffle(ess.deck1)
                                ess.player_list[0].append(ess.deck1.pop())
                        ess.special_check = 1
                        ess.shouted_uno[0] = False
                        ess.player_playing = False
                    
                    elif ess.current[0] == '+2' and ess.special_check == 0:  # Draw 2
                        for _ in range(2):
                            try:
                                ess.player_list[0].append(ess.deck1.pop())
                            except:
                                ess.deck1, ess.deck2 = ess.deck2, ess.deck1
                                random.shuffle(ess.deck1)
                                ess.player_list[0].append(ess.deck1.pop())
                        ess.special_check = 1
                        ess.shouted_uno[0] = False
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
                        ess.shouted_uno[0] = False
                        ess.player_playing = False
                    
                    if len(ess.player_list[0]) == 1 and ess.shouted_uno[0] == False:
                        # 전에 UNO를 외치지 않았는데, 1장 남았다면,
                        try: 
                            ess.player_list[0].append(ess.deck1.pop()) # 페널티로 덱에서 카드 한장을 뽑는다.
                        except:
                            ess.deck1, ess.deck2 = ess.deck2, ess.deck1
                            random.shuffle(ess.deck1)
                            ess.player_list[0].append(ess.deck1.pop())
                            ess.message = "You didn't shout UNO! Penalty card drawn."
                            text = pygame.font.Font(FONT.joe_fin, int(height*(20/600))).render(ess.message, True, (255, 238, 46))
                            uno.screen.blit(text, [width*(140/1000), height*(110/600)]) # 게임 진행 메시지

                # img.line은 현재 플레이 해야할 플레이어를 표시하고, 유저는 체크 버튼과 UNO 버튼이 추가로 표시된다
                uno.screen.blit(img.line, (width*(482/1000), height*(550/600)))
                uno.screen.blit(img.done, (width*(565/1000), height*(505/600)))
                
                if ess.play_mode != "GAME PAUSE": # 게임이 일시정지 상태가 아니면
                    ess.play_lag += 1 # 게임의 FPS마다 1씩 증가한다

        else: # AI가 플레이 중이면
            if ess.play_lag == 140:  # 플레이어 간의 행동 사이에 지연을 구현한다
                disp = False
                pen_check = False

                # 다음 플레이어를 결정한다
                set_curr_player(ess, uno, True)

                # 그게 유저의 턴이면
                if ess.position == 0:
                    # ess.shouted_uno[0] = False # 유저 플레이어가 UNO를 외쳤는지 저장하는 플래그를 초기화한다
                    ess.player_playing = True # 유저가 플레이 중임을 표시한다

                else: # 다음 플레이어가 AI라면
                    # 일단 유저의 플래그를 초기화한다
                    ess.played = False
                    ess.drawn = False

                    # 그 다음 AI의 행동을 결정한다
                    bot_action(ess, uno, sound)

                ess.play_lag = 0  # 랙 리셋

            else: # 아직 1.4초 안 지났으면
                if win_dec and ess.play_lag == 70:  # 게임의 승자 선언을 0.7초 지연한다
                    ess.play_mode = PM.win

                if not pen_check: # 페널티 체크 플래그, 게임이 처음 시작할 때는 False였다
                    for i in range(1, uno.player_num):
                        if ess.position == i and len(ess.player_list[i]) == 1 and not ess.shouted_uno[i]: # 1장 남았는데, UNO를 외치지 않으면
                            try: 
                                ess.player_list[i].append(ess.deck1.pop()) # 페널티로 덱에서 카드 한장을 뽑는다.
                            except:
                                ess.deck1, ess.deck2 = ess.deck2, ess.deck1
                                random.shuffle(ess.deck1)
                                ess.player_list[i].append(ess.deck1.pop())

                            ess.message = "Penalty!"
                            pen_check = True
                if ess.play_mode != "GAME PAUSE": # 게임이 일시정지 상태가 아니면
                    ess.play_lag += 1 # 게임의 FPS마다 1씩 증가한다

                if not disp: # disp을 True로 한다?
                    disp = True

                # 현재 턴의 플레이어를 검정 선 이미지로 표시한다
                Flag_line = (ess.position + ess.direction_check) % uno.player_num
                for i in range(1, uno.player_num):
                    if Flag_line == i:
                        uno.screen.blit(img.line, (width*(860/1000), height*((-110 + i * 120)/600)))

    # SETTING 화면
    elif ess.play_mode == PM.setting or ess.play_mode == PM.key or ess.play_mode == PM.volume:
        uno.screen.blit(img.bg,(0,0))
        pygame.mixer.music.set_volume(saves["background"])
        volumesetting(sound, saves["effects"])
        
        if ess.play_mode == PM.setting: # 처음 setting 화면일 경우
            reset = load_setting(ess, uno, PM, FONT, saves)
            if reset == True:
                saves = return_default_setting()
        
        # Key Configuration 설정 모드일 경우
        elif ess.play_mode == PM.key:
            load_key_config(ess, uno, PM, FONT, saves)

        # 볼륨 설정 모드일 때
        elif ess.play_mode == PM.volume:
            load_volume_config(ess, uno, sound, PM, FONT, saves)

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
        uno.screen.blit(img.win, (0, 0))
        text = pygame.font.Font(FONT.pacifico, int(height*(40/600))).render(string, True, (255, 238, 46))
        uno.screen.blit(text, [width*(190/1000), height*(100/600)])

    # 배경음악 / 효과음 토글 버튼
    if ess.play_mode == PM.in_game:
        if music_on:
            uno.screen.blit(img.mute, (width*(60/1000), height*(10/600)))
        else:
            uno.screen.blit(img.unmute, (width*(60/1000), height*(10/600)))

    # 화면 지속적으로 갱신
    pygame.display.update()
